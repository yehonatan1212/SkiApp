import datetime
from typing import Union
from flask_restx import Namespace, fields
from .. import db, flask_bcrypt
from ..config import key
import jwt

api = Namespace('user', description='user related operations')


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    ski_level = db.Column(db.String(50), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = False
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'height': fields.Float(required=True, description='user height'),
        'weight': fields.Float(required=True, description='user weight'),
        'ski_level': fields.String(required=False, description='user ski level')
    })
    user_out = api.model('user_out', {
        'id': fields.Integer(required=True, description='user id'),
        'registered_on': fields.Date(required=True, description='user created at'),
        'username': fields.String(required=True, description='user username'),
        'height': fields.Float(required=True, description='user height'),
        'weight': fields.Float(required=True, description='user weight'),
        'ski_level': fields.String(required=False, description='user ski level')
    })
    user_update = api.model('user_update', {
        'height': fields.Float(required=False, description='user height'),
        'weight': fields.Float(required=False, description='user weight'),
        'ski_level': fields.String(required=False, description='user ski level')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='The user password '),
    })
