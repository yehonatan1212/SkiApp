import uuid
import datetime
from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            height=data['height'],
            weight=data['weight'],
            ski_level=data['ski_level'],
            registered_on=datetime.datetime.utcnow()
        )
        # Use the password setter
        new_user.password = data['password']
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


# change for manager Authorization
def get_a_user(public_id, current_user):
    user = User.query.filter_by(id=current_user['user_id']).first()
    if not user:
        response_object = {
            'status': 'Authorization Error',
            'message': 'You do not have permission to access this users information'
        }
        return response_object, 403
    return User.query.filter_by(public_id=public_id).first()


def edit_user(current_user, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(id=current_user['user_id']).first()
    if not user:
        response_object = {
            'message': 'Authorization Error'
        }
        return response_object, 404
    if 'height' in data:
        user.height = data['height']
    if 'weight' in data:
        user.weight = data['weight']
    if 'ski_level' in data:
        user.ski_level = data['ski_level']
    save_changes(user)
    return user, 200


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()


def user_specs_for_calc(user_id):
    # Query the database for the user with the given user_id
    user = User.query.filter_by(id=user_id).first()

    if not user:
        raise ValueError(f"User with id {user_id} not found.")

    # Extract the height, weight, and ski level from the user object
    response = {'height': user.height,
                'weight': user.weight,
                'ski_level': user.ski_level
                }
    return response
