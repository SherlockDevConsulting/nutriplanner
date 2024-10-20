from flask import Flask
from app.config.config import Config
from app.config.logging_config import setup_logging
from app.config.db import db


def create_app():
    """Setup the flask application"""
    app = Flask(__name__)

    # Init Configuration Object in app
    app.config.from_object(Config)

    db.init_app(app)

    # pylint: disable=C0415
    from app.routes import register_routes

    register_routes(app)

    setup_logging()

    return app
