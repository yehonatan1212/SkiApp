from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize extensions
    db.init_app(app)
    flask_bcrypt.init_app(app)
    from .. import blueprint
    app.register_blueprint(blueprint)
    return app
