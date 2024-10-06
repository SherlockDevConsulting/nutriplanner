import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI #"postgresql://nutriplanner:pass@localhost:5431/nutriplanner"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['DEBUG'] = Config.APP_DEBUG

    
    
    # Configuration du logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler('app.log')])

    # Utiliser le logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Niveau de log par defaut
    logger.info("HEYYYYYYYYYYYYYYYY")

    db.init_app(app)

    @app.route('/set_log_level/<level>')
    def set_log_level(level):
        """Endpoint pour changer dynamiquement le niveau de log."""
        level = level.upper()
        if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            logger.setLevel(getattr(logging, level))
            return f"Niveau de log change  {level}", 200
        return f"Niveau de log {level} invalide", 400

    return app
