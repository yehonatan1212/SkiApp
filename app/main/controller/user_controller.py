from flask import request
from flask_restx import Resource, abort

from app.main.util.decorator import admin_token_required, token_required
from ..model.user import UserDto, AuthDto
from ..service.auth_helper import Auth
from ..service.user_service import save_new_user, get_all_users, get_a_user, edit_user
from typing import Dict, Tuple

api = UserDto.api
_user = UserDto.user
_user_out = UserDto.user_out
_user_auth = AuthDto.user_auth
_user_update = UserDto.user_update


@api.route('/get all users')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    @token_required   # change to admin_token_required
    def get(self):
        """List all registered users"""
        return get_all_users()


@api.route('/register')
class Register(Resource):
    @api.expect(UserDto.user, validate=True)
    def post(self):
        """Register a new user"""
        data = request.json
        return save_new_user(data)


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(_user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user_out)
    @token_required
    def get(self, public_id, current_user):
        """get a user given its identifier"""
        user = get_a_user(public_id, current_user)
        if not user:
            api.abort(404)
        else:
            return user


@api.route('/adit_user')
@api.expect(_user_update, validate=True)
@api.response(201, 'user successfully updated.')
class User(Resource):
    @api.doc('edit user')
    @api.marshal_with(_user_out)
    @token_required
    def put(self, current_user):
        data = request.json
        update_user = edit_user(current_user, data)
        return update_user
