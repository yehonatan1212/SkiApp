from flask_restx import Api
from flask import Blueprint

# Import your namespaces
from .main.controller.ski_controller import api as ski_ns
from .main.controller.user_controller import api as user_ns
from .main.model.user import AuthDto

blueprint = Blueprint('api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='Ski Equipment',
    version='1.0',
    description='Check if your ski equipment is right for your needs!',
    authorizations=authorizations,
    security='apikey'
)

# Add namespaces
api.add_namespace(ski_ns, path='/Ski_gear')
api.add_namespace(user_ns, path='/user')
api.add_namespace(AuthDto.api)
