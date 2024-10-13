import logging
import logging.config

def setup_logging(log_level=logging.INFO):
    """Configure global logging for the application."""
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': log_level,
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': 'app.log',
                'level': log_level,
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': log_level,
        },
    }

    # Configure the logger with the above settings
    logging.config.dictConfig(logging_config)
