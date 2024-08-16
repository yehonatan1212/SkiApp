import math
from typing import Dict
import joblib
import os

import numpy as np
import pandas as pd

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the model file
model_path = os.path.join(current_dir, 'ski_classifier_model.pkl')
# Load the model
ml_model = joblib.load(model_path)
'''C:/Users/hubhh/PycharmProjects/server/app/main/service/ski_classifier_model.pkl'''


# Validate and prepare the input data
def prepare_input_data(input_data):
    if isinstance(input_data, dict):
        input_data_list = [input_data]
    elif isinstance(input_data, list):
        input_data_list = input_data
    else:
        raise ValueError("Input data must be a dictionary or a list of dictionaries")

    input_df = pd.DataFrame(input_data_list)
    return input_df


class ModelPredictionResponse:
    def __init__(self, slope_pred, min_level_pred, max_level_pred):
        self.slope_pred = slope_pred
        self.min_level_pred = min_level_pred
        self.max_level_pred = max_level_pred


def model_predictions(input_data):
    input_df = prepare_input_data(input_data)
    print("--DF-- \n", input_df)
    predictions = ml_model.predict(input_df)

    slope_pred = np.around(predictions[0, 0], decimals=1).astype(float).tolist()
    min_level_pred = np.around(predictions[0, 1], decimals=1).astype(float).tolist()
    max_level_pred = np.around(predictions[0, 2], decimals=1).astype(float).tolist()

    response = ModelPredictionResponse(slope_pred, min_level_pred, max_level_pred)
    print("="*50)
    print(f"Response: \n {response.slope_pred, response.min_level_pred, response.max_level_pred}")
    return response


# Test sample data
ski_input = [
    {
        'height': 170,
        'radius': 14,
        'sidecut_tip': 170,
        'sidecut_waist': 68,
        'sidecut_tail': 102
    },
    {
        'height': 185,
        'radius': 18,
        'sidecut_tip': 143,
        'sidecut_waist': 109,
        'sidecut_tail': 134
    }
]

"""out = model_predictions(ski_input)
print(f"Slope: {out.slope_pred}, Min Level: {out.min_level_pred}, Max Level: {out.max_level_pred}")"""

"====================================================================================================================="
"Manual Classification Logic"


class manual_classification:
    def __init__(self, specs):
        self.height = specs.get('height')
        self.radius = specs.get('radius')
        self.sidecut_tip = specs.get('sidecut_tip')
        self.sidecut_waist = specs.get('sidecut_waist')
        self.sidecut_tail = specs.get('sidecut_tail')
        self.skier_height = specs.get('skier_height')

    def height_difference(self):
        # Height Difference = Skier's Height - Ski Length
        height_difference = self.skier_height - self.height
        return height_difference

    def contact_length(self):
        # Calculate the contact length using the radius formula from sidecut
        sidecut_depth = (self.sidecut_tip + self.sidecut_tail) / 2 - self.sidecut_waist
        contact_length = math.sqrt(2 * self.radius * sidecut_depth)
        return contact_length

    def floatation(self):
        # Floatation = sqrt(Ski Area), where Ski Area = length * (tip + waist + tail)/3
        ski_area = self.height * (self.sidecut_tip + self.sidecut_waist + self.sidecut_tail) / 3
        floatation = ski_area ** 0.5
        return floatation

    def classify(self):
        response = {
            'height_difference': round(self.height_difference(), 1),
            'contact_length': round(self.contact_length(), 1),
            'floatation': round(self.floatation(), 1)
        }
        return response


# Manual logic...
# region set params for normalize, weights and scales
# Normalization ranges with updated directions
normalization_ranges = {
    'camber_rocker': (1, 3, 5),  # min, mid, max (1-low rocker, 5-high camber)
    'length': (140, 170, 200),  # cm
    'waist': (65, 80, 120),  # mm
    'radius': (8, 14, 25),  # m
    'weight': (1, 2.5, 5),  # kg per ski
    'stiffness': (1, 3, 5),  # scale 1-5 (1-soft, 5-stiff)
}

# Weights matrix based on the updated relationships
weights = {
    'stability_vs_manoeuvrability': {'camber_rocker': 4, 'length': 2, 'waist': -2, 'radius': 0, 'weight': 4,
                                     'stiffness': 4},
    'short_vs_long_turns': {'camber_rocker': 0, 'length': 0, 'waist': 0, 'radius': 6, 'weight': 0, 'stiffness': 2}
}


def normalize(value, min_value, mid_value, max_value):
    if value is None:
        return 0  # Default to 0 if value is None
    if value <= min_value:
        return -10
    elif value >= max_value:
        return 10
    elif value == mid_value:
        return 0
    elif value < mid_value:
        return -10 + ((value - min_value) / (mid_value - min_value)) * 10
    else:
        return ((value - mid_value) / (max_value - mid_value)) * 10
# endregion


def classify_ski(ski_specs: Dict[str, float]) -> Dict[str, float]:
    scores = {'stability_vs_manoeuvrability': 0, 'short_vs_long_turns': 0}
    max_scores = {'stability_vs_manoeuvrability': 16, 'short_vs_long_turns': 8}

    for measure, weight_dict in weights.items():
        for spec, weight in weight_dict.items():
            min_value, mid_value, max_value = normalization_ranges[spec]
            normalized_value = normalize(ski_specs.get(spec), min_value, mid_value, max_value)
            scores[measure] += normalized_value * weight

    # Scale the results to -10 to 10 range
    for measure in scores:
        scores[measure] = (scores[measure] / max_scores[measure])

    return scores
