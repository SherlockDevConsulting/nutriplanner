import logging
from dotenv import load_dotenv
from app import create_app

load_dotenv()
app = create_app()
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Start")
    app.run(host="0.0.0.0", port=5000, debug=True)
