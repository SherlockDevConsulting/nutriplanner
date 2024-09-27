from flask import Flask
from config.config import Config
#from config.db import db
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # # Initialiser la base de données
    # db.init_app(app)

    # Initialiser les routes
    init_routes(app)

    return app
