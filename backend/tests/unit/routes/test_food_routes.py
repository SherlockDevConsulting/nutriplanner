# pylint: disable=W0621
# pylint: disable=C0116
from unittest.mock import patch
from jsonschema import SchemaError, ValidationError
import pytest

from app.models.food import Food
from app.routes.food_routes import FoodRoutes
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_food_service(mocker):
    """Fixture to provide a mocked service session"""
    mock_service = mocker.patch("app.routes.food_routes.FoodService")
    return mock_service


@pytest.fixture
def sample_food() -> Food:
    """Fixture to provide a sample food object"""
    return Food(id=1, code="12345", name="Apple")


@pytest.fixture
def sample_food_json():
    """Fixture to provide a sample food json data"""
    return {"id": 1, "code": "12345", "name": "Apple"}


def configure_mock_service(service_mock, method: str, value) -> None:
    """Utility function to configure the mock with the method and value"""
    getattr(service_mock.return_value, method).return_value = value


def test_get_foods(app, mock_food_service, sample_food):
    # Given
    configure_mock_service(
        mock_food_service, "fetch_all_foods", [sample_food, sample_food]
    )

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.get_foods()
        response_data = result[0].json

        # Then
        assert isinstance(response_data, list)
        assert len(response_data) == 2
        assert response_data[0]["code"] == "12345"
        assert response_data[1]["name"] == "Apple"
        assert result[0] == 200
        assert result[1] == 200


def test_get_foods_runtime_error(app, mock_food_service):

    # configure_mock_service(mock_food_service, "fetch_all_foods.side_effect", RuntimeError())
    mock_food_service.return_value.fetch_all_foods.side_effect = RuntimeError(
        "Test Runtime Error"
    )

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.get_foods()
        response_data = result[0]

        # Then
        assert result[1] == 500
        assert response_data["error"] == "Internal Error"


def test_get_food_by_id_success(app, mock_food_service, sample_food):
    # Given
    configure_mock_service(mock_food_service, "fetch_food_by_id", sample_food)

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.get_food_by_id(1)
        response_data = result[0].json
        # Then
        assert result[0] == 200
        assert response_data["code"] == "12345"
        assert response_data["name"] == "Apple"
        assert result[1] == 200


def test_get_food_by_id_value_error(app, mock_food_service):
    # Given
    mock_food_service.return_value.fetch_food_by_id.side_effect = ValueError()

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.get_food_by_id(1)
        response_data = result[0]

        # Then
        assert result[1] == 404
        assert response_data["error"] == "Food not found"


def test_get_food_by_id_runtime_error(app, mock_food_service):
    # Given
    mock_food_service.return_value.fetch_food_by_id.side_effect = RuntimeError()

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.get_food_by_id(1)
        response_data = result[0]

        # Then
        assert result[1] == 500
        assert response_data["error"] == "Internal Error"


@patch("app.routes.food_routes.request")
@patch("app.routes.food_routes.validate")
def test_create_food_success(
    mock_validate, mock_request, app, mock_food_service, sample_food, sample_food_json
):
    # Given
    configure_mock_service(mock_food_service, "create_food", sample_food)
    mock_request.return_value.get_json.return_value = sample_food_json
    mock_validate.return_value = None

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.create_food()
        response_data = result[0]

        # Then
        assert result[1] == 201
        assert response_data["success"] == "food created"


@patch("app.routes.food_routes.request")
@patch("app.routes.food_routes.validate")
def test_create_food_validation_error(
    mock_validate, mock_request, app, sample_food_json, sample_food, mock_food_service
):
    # Given
    configure_mock_service(mock_food_service, "create_food", sample_food)
    mock_request.return_value.get_json.return_value = sample_food_json
    mock_validate.side_effect = ValidationError("Invalid schema")

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.create_food()
        response_data = result[0]

        # Then
        assert result[1] == 400
        assert response_data["error"] == "json invalid"


@patch("app.routes.food_routes.request")
@patch("app.routes.food_routes.validate")
def test_create_food_schema_error(
    mock_validate, mock_request, app, sample_food_json, sample_food, mock_food_service
):
    # Given
    configure_mock_service(mock_food_service, "create_food", sample_food)
    mock_request.get_json.return_value = sample_food_json
    mock_validate.side_effect = SchemaError("Invalid schema")

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.create_food()
        response_data = result[0]

        # Then
        assert result[1] == 400
        assert response_data["error"] == "json invalid"


@patch("app.routes.food_routes.request")
@patch("app.routes.food_routes.validate")
def test_create_food_value_error(
    mock_validate, mock_request, app, sample_food_json, mock_food_service
):
    # Given
    mock_food_service.return_value.create_food.side_effect = ValueError()
    mock_request.get_json.return_value = sample_food_json
    mock_validate.return_value = None

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.create_food()
        response_data = result[0]

        # Then
        assert result[1] == 400
        assert response_data["error"] == "Food already exist"


@patch("app.routes.food_routes.request")
@patch("app.routes.food_routes.validate")
def test_create_food_runtime_error(
    mock_validate, mock_request, app, sample_food_json, mock_food_service
):
    # Given
    mock_food_service.return_value.create_food.side_effect = RuntimeError()
    mock_request.get_json.return_value = sample_food_json
    mock_validate.return_value = None

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.create_food()
        response_data = result[0]

        # Then
        assert result[1] == 500
        assert response_data["error"] == "Internal error while creating food"


@patch("app.routes.food_routes.request")
@patch("app.routes.food_routes.validate")
def test_create_food_exception_error(
    mock_validate, mock_request, app, sample_food_json, mock_food_service
):
    # Given
    mock_food_service.return_value.create_food.side_effect = Exception()
    mock_request.get_json.return_value = sample_food_json
    mock_validate.return_value = None

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.create_food()
        response_data = result[0]

        # Then
        assert result[1] == 500
        assert response_data["error"] == "Failed to create food"


def test_delete_food_success(app, mock_food_service):
    # Given
    configure_mock_service(mock_food_service, "delete_food", True)

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.delete_food(1)

        # Then
        assert result[1] == 204


def test_delete_food_value_error(app, mock_food_service):
    # Given
    mock_food_service.return_value.delete_food.side_effect = ValueError()

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.delete_food(1)
        response_data = result[0]

        # Then
        assert result[1] == 404
        assert response_data["error"] == "food to delete not found"


def test_delete_food_runtime_error(app, mock_food_service):
    # Given
    mock_food_service.return_value.delete_food.side_effect = RuntimeError()

    with app.app_context():
        # When
        route = FoodRoutes()
        result = route.delete_food(1)
        response_data = result[0]

        # Then
        assert result[1] == 500
        assert response_data["error"] == "Internal error while deleting food"
