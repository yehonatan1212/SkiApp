from flask_restplus import Resource
from flask import request
from typing import Tuple, Dict
from ..model.ski import api, SkiDto
from ..service.ski_service import new_ski_specs, delete_ski_by_id, update_ski, get_all_skis, upload_ski_picture, \
    add_rating
from ..util.decorator import token_required

"""ski_controller.py connects crud functions with api calls
GoTo ski_service.py to see basic crud functions. (put, delete, get, post)
GoTo ski.py to connect with data base"""

ski_g = SkiDto.ski_g
ski_g_out = SkiDto.ski_g_out

import logging


@api.doc('get all Skis')
@api.route('/get_all_skis')
class GetSki(Resource):
    @api.marshal_list_with(ski_g_out, envelope='data')
    @token_required
    def get(self, current_user):
        return get_all_skis(current_user['user_id']), 200


@api.doc('create a new Ski')
@api.route('/new_ski')
class CreateSki(Resource):
    @api.expect(ski_g, validate=True)
    @api.marshal_with(ski_g_out)
    @token_required
    def post(self, current_user) -> Tuple[Dict[str, str], int]:
        data = request.json
        return new_ski_specs(user_id=current_user['user_id'], data=data)


@api.route('/edit/<ski_id>')
@api.param('ski_id', 'The ski identifier')
class OneUserController(Resource):
    @api.doc('delete a Ski by ID')
    @token_required
    def delete(self, ski_id: int, current_user) -> Tuple[Dict[str, str], int]:
        response, status_code = delete_ski_by_id(current_user['user_id'], ski_id)
        return response, status_code

    @api.doc('update a Ski by ID')
    @api.expect(ski_g, validate=True)
    @api.response(201, 'Ski successfully updated.')
    @api.marshal_with(ski_g_out)
    @token_required
    def put(self, ski_id: int, current_user) -> Tuple[Dict[str, str], int]:
        data = request.json
        return update_ski(current_user['user_id'], ski_id, data)

    @api.doc('upload picture for ski')
    @api.expect(SkiDto.upload_parser, validate=True)
    @token_required
    def post(self, current_user):
        args = SkiDto.upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        ski_id = args['ski_id']
        user_id = current_user['user_id']
        url = upload_ski_picture(user_id, ski_id, uploaded_file)
        return {'url': url}

    @api.doc('rate your ski')
    @api.expect(SkiDto.rating_parser, validate=True)
    @api.marshal_with(ski_g_out)
    @token_required
    def post(self,  ski_id: int,  current_user):
        args = SkiDto.rating_parser.parse_args()
        user_id = current_user['user_id']
        rating = args['rating']
        rate = add_rating(user_id, ski_id, rating)
        return rate


@api.errorhandler(Exception)
def default_error_handler(error):
    logging.exception(error)
    return {'message': str(error)}, 500


"""@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserController(Resource):

    # Get all user skies, by user id
    @api.doc('get all Skis')
    @api.marshal_list_with(ski_g_out, envelope='data')
    @token_required
    def get(self, current_user):
        return get_all_skis(current_user['user_id']), 200

    # Create a new ski, by user id
    @api.expect(ski_g, validate=True)
    @api.response(201, 'Ski successfully created.')
    @api.marshal_with(ski_g_out)
    @api.doc('create a new Ski')
    def post(self, user_id) -> Tuple[Dict[str, str], int]:
        data = request.json
        return new_ski_specs(user_id=user_id, data=data)
"""

"""@api.route('/<user_id>/picture')
@api.param('user_id', 'The user identifier')
@api.param('ski_id', 'The ski identifier')
class PictureUserController(Resource):
    @api.doc('upload picture for ski')
    @api.expect(SkiDto.upload_parser, validate=True)
    def post(self):
        args = SkiDto.upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        ski_id = args['ski_id']
        user_id = args['user_id']
        url = upload_ski_picture(user_id, ski_id, uploaded_file)
        return {'url': url}"""
