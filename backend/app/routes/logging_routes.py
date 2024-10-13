import logging
from flask import Blueprint, jsonify


log_blueprint = Blueprint('log', __name__)
logger = logging.getLogger()


@log_blueprint.route('/set_log_level/<level>', methods=['POST'])
def set_log_level(level):
    """Endpoint to dynamically change the logging level."""
    level = level.upper()
    if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        logger.setLevel(getattr(logging, level))
        return jsonify({"message": f"Log level changed to {level}"}), 200
    
    return jsonify({"error": f"Invalid log level {level}"}), 400
