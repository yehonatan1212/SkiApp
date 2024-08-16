from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage
from .. import db

"""ski.py connect with data base
GoTo ski_service.py to see basic crud functions. (put, delete, get, post)
GoTo ski_controller.py connect crud functions with api calls"""

api = Namespace('Ski_gear', description='Ski_gear related operations')


# set table name and fields in DB
class Ski(db.Model):
    __tablename__ = "Ski_gear"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    length = db.Column(db.Float, nullable=True)
    radius = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    camber_rocker = db.Column(db.Float, nullable=True)
    tip = db.Column(db.Float, nullable=True)
    waist = db.Column(db.Float, nullable=True)
    tail = db.Column(db.Float, nullable=True)
    stiffness = db.Column(db.Float, nullable=True)
    picture = db.Column(db.String(300), unique=False, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    stability_vs_manoeuvrability = db.Column(db.Float, nullable=True)  # delete?
    short_vs_long_turns = db.Column(db.Float, nullable=True)  # delete?
    on_piste_vs_off_piste = db.Column(db.Float, nullable=True)
    ski_level_min = db.Column(db.Float, nullable=True)
    ski_level_max = db.Column(db.Float, nullable=True)
    height_difference = db.Column(db.Float, nullable=True)
    contact_length = db.Column(db.Float, nullable=True)
    floatation = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "<Ski_gear '{}'>".format(self.name)


# POST new ski   (Dto - data transfer object)
class SkiDto:
    # parser params to post picture
    upload_parser = api.parser()
    upload_parser.add_argument('ski_id', type=int, help='ski id', location='args')
    upload_parser.add_argument('file', type=FileStorage, location='files')
    rating_parser = api.parser()
    rating_parser.add_argument('rating', type=int, help='rating', location='args')

    # post input
    ski_g = api.model('ski_g', {
        'name': fields.String(required=True, description='ski name'),
        'length': fields.Float(description='ski length'),
        'radius': fields.Float(description='Turn Radius'),
        'weight': fields.Float(description='ski Weight'),
        'camber_rocker': fields.Float(description='Scale 1-5 (1-low rocker, 5-high camber)'),
        'tip': fields.Float(description='tip width'),
        'waist': fields.Float(description='ski waist width (underfoot)'),
        'tail': fields.Float(description='tail width'),
        'stiffness': fields.Float(description='ski stiffness: Scale 1-5 (1-soft, 5-stiff)')
    })
    # post output
    ski_g_out = api.model('ski_g_out', {
        'id': fields.Integer(required=True, description='ski id'),
        'created_at': fields.Date(required=True, description='ski created at'),
        'user_id': fields.String(description='user_name'),
        'name': fields.String(required=True, description='ski name'),
        'length': fields.Float(description='ski length'),
        'radius': fields.Float(description='ski radius'),
        'weight': fields.Float(description='ski weight'),
        'picture': fields.String(description='picture'),
        'rating': fields.Integer(description='rating'),
        'camber_rocker': fields.Float(description='Scale 1-5 (1-low rocker, 5-high camber)'),
        'tip': fields.Float(description='tip width'),
        'waist': fields.Float(description='ski waist width (underfoot)'),
        'tail': fields.Float(description='tail width'),
        'stiffness': fields.Float(description='ski stiffness: Scale 1-5 (1-soft, 5-stiff)'),
        'stability_vs_manoeuvrability': fields.Float(description='stability vs manoeuvrability '
                                                                 '|scale -10 to 10 | 10 is stable'),
        'short_vs_long_turns': fields.Float(description='short vs long turns'
                                                        '|scale -10 to 10 | 10 is long turns'),
        'on_piste_vs_off_piste': fields.Float(description='on-piste vs off-piste'
                                                          '|scale 0-10 | 10 is on-piste'),
        'ski_level_min': fields.Float(description='ski level min | 0-beginner, 10-expert'),
        'ski_level_max': fields.Float(description='ski level max | 0-beginner, 10-expert'),
        'height_difference': fields.Float(description='height difference'),
        'contact_length': fields.Float(description='contact length'),
        'floatation': fields.Float(description='floatation')
    })
