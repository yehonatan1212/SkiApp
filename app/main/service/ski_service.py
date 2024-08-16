import datetime
import logging
from app.main import db
from app.main.model.ski import Ski
from typing import Dict, Tuple
from app.main.service.class_logic import model_predictions, manual_classification
from app.main.model.user import User
from app.main.service.aws_service import create_presigned_url, upload_file
from app.main.service.user_service import user_specs_for_calc

"""ski_service.py holds the basic crud functions. (put, delete, get, post)
GoTo ski_controller.py to connect crud functions to api.
GoTo ski.py to connect with data base"""


# add the new ski to the database
def new_ski_specs(user_id, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(id=user_id).first()
    if user:
        new_ski = Ski(
            user_id=user_id,
            created_at=datetime.datetime.utcnow(),
            name=data['name'],
            length=data['length'],
            radius=data['radius'],
            weight=data['weight'],
            camber_rocker=data['camber_rocker'],
            tip=data['tip'],
            waist=data['waist'],
            tail=data['tail'],
            stiffness=data['stiffness']
        )
        saved_ski = save_changes(new_ski)
        classified_ski = classify_and_update_ski(saved_ski, user_id)
        save_changes(classified_ski)
        return classified_ski, 201
    else:
        return {"message": "User not found"}, 404


# delete an existing ski
def delete_ski_by_id(user_id: int, ski_id: int) -> Tuple[Dict[str, str], int]:
    # Fetch ski by ski_id and user_id to ensure it belongs to the correct user
    ski = Ski.query.filter_by(id=ski_id, user_id=user_id).first()
    if ski:
        db.session.delete(ski)
        db.session.commit()
        return {"message": "Ski successfully deleted"}, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Ski not found'
        }
        return response_object, 404


# update an existing ski, & calculate new measures
def update_ski(user_id: int, ski_id: int, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    ski = Ski.query.filter_by(id=ski_id, user_id=user_id).first()
    if not ski:
        return {"message": "Ski not found"}, 404
    else:
        ski.name = data.get('name', ski.name)
        ski.length = data.get('length', ski.length)
        ski.radius = data.get('radius', ski.radius)
        ski.weight = data.get('weight', ski.weight)
        ski.camber_rocker = data.get('camber_rocker', ski.camber_rocker)
        ski.tip = data.get('tip', ski.tip)
        ski.waist = data.get('waist', ski.waist)
        ski.tail = data.get('tail', ski.tail)
        ski.stiffness = data.get('stiffness', ski.stiffness)

        saved_ski = save_changes(ski)
        classified_ski = classify_and_update_ski(saved_ski, user_id)
        save_changes(classified_ski)
        return classified_ski, 200


# get all skis of a user
def get_all_skis(user_id) -> tuple[dict[str, str], int]:
    return Ski.query.filter(Ski.user_id == user_id).all()


# classify(calculate) measures
def classify_and_update_ski(ski: Ski, user_id) -> Ski:
    model_specs = {
        'height': ski.length,
        'radius': ski.radius,
        'sidecut_tip': ski.tip,
        'sidecut_waist': ski.waist,
        'sidecut_tail': ski.tail
    }
    user = user_specs_for_calc(user_id)
    Manual_specs = {
        'height': ski.length,
        'radius': ski.radius,
        'sidecut_tip': ski.tip,
        'sidecut_waist': ski.waist,
        'sidecut_tail': ski.tail,
        'skier_height': user['height']
    }
    # logic for classification (model & manual)
    model_classification = model_predictions(model_specs)
    classification = manual_classification(Manual_specs)
    manual = classification.classify()

    slope_pred_value = model_classification.slope_pred
    ski.on_piste_vs_off_piste = float(slope_pred_value)  # Ensure this is a float
    ski.ski_level_min = model_classification.min_level_pred
    ski.ski_level_max = model_classification.max_level_pred

    ski.contact_length = manual['contact_length']
    ski.floatation = manual['floatation']
    ski.height_difference = manual['height_difference']

    return save_changes(ski)


# save the changes to the database and refresh
def save_changes(data: Ski) -> Ski:
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)
    return data


def upload_ski_picture(user_id, ski_id, uploaded_file):
    logging.info(f"Uploading ski picture for user {user_id}, ski {ski_id}")
    ski = Ski.query.filter_by(id=ski_id, user_id=user_id).first()
    if ski:
        # Generate a unique filename using user_id and ski_id
        filename = f"user_{user_id}_ski_{ski_id}.png"
        ski.picture = f"ski_photo's/{filename}"
        upload_file(uploaded_file, ski.picture)
        db.session.commit()
        return {"message": "Photo Successfully Uploaded"}, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'uploading picture failed'
        }
        return response_object, 404


def add_rating(user_id, ski_id, rating):
    ski = Ski.query.filter_by(id=ski_id, user_id=user_id).first()
    if ski:
        ski.rating = rating
        save_changes(ski)
        return ski, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Ratting failed'
        }
        return response_object, 404


def get_one_ski(user_id, ski_id):
    ski = Ski.query.filter_by(id=ski_id, user_id=user_id).first()
    if ski.picture:
        ski.picture = create_presigned_url(ski.picture)
    return ski
