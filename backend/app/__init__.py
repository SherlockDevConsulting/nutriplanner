import logging
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    
    # Configuration du logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler('app.log')])

    # Utiliser le logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Niveau de log par défaut

    @app.route('/set_log_level/<level>')
    def set_log_level(level):
        """Endpoint pour changer dynamiquement le niveau de log."""
        level = level.upper()
        if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            logger.setLevel(getattr(logging, level))
            return f"Niveau de log changé à {level}", 200
        return f"Niveau de log {level} invalide", 400

    return app
