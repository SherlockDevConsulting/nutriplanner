# pylint: disable=C0116
import logging
import pytest
from flask import Flask
from app.routes.logging_routes import log_blueprint


# Crée un client Flask pour les tests
@pytest.fixture
def app():
    """Fixture to create app"""
    app = Flask(__name__)
    app.register_blueprint(log_blueprint, url_prefix="/")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


def test_set_log_level_valid(app, mocker):
    """Test valid log level changes."""
    # Given
    client = app.test_client()
    mock_logger = mocker.patch("app.routes.logging_routes.logger")

    # When
    response = client.post("/set_log_level/INFO")

    # Then
    assert response.status_code == 200
    assert response.get_json()["message"] == "Log level changed to INFO"
    mock_logger.setLevel.assert_called_once_with(logging.INFO)


def test_set_log_level_invalid(app):
    """Test invalid log level."""
    # Given
    client = app.test_client()

    # When
    response = client.post("/set_log_level/INVALID")

    # Then
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid log level INVALID"
