# pylint: disable=W0621
import pytest

from app.models.food import Food
from app.services.food_service import FoodService


@pytest.fixture
def mock_food_repository(mocker):
    """Fixture to provide a mocked repository session"""
    mock_repository = mocker.patch("app.services.food_service.FoodRepository")
    return mock_repository


@pytest.fixture
def sample_food() -> Food:
    """Fixture to provide a sample food object"""
    return Food(id=1, code="12345", name="Apple")


def configure_mock_repository(mock_food_repo, method: str, value) -> None:
    """Utility function to configure the mock with the method and value"""
    getattr(mock_food_repo.return_value, method).return_value = value


def test_fetch_all_foods(mock_food_repository, sample_food):
    """Unit test to get all foods from repository"""
    # Given
    configure_mock_repository(
        mock_food_repository, "get_all_foods", [sample_food, sample_food]
    )

    # When
    service = FoodService()
    result = service.fetch_all_foods()

    # Then
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].code == "12345"
    assert result[0].name == "Apple"


def test_fetch_food_by_id(mock_food_repository, sample_food):
    """Unit test to get one food by id"""
    # Given
    configure_mock_repository(mock_food_repository, "get_food_by_id", sample_food)
    id_food = 1
    # When
    service = FoodService()
    result = service.fetch_food_by_id(id_food)

    # Then
    assert result is sample_food
    assert result.id == 1
    assert result.code == "12345"
    assert result.name == "Apple"


def test_fetch_food_with_wrong_id(mock_food_repository):
    """Unit test to catch error when food not exit"""
    # Given
    configure_mock_repository(mock_food_repository, "get_food_by_id", None)
    id_food = 1

    # When / Then
    service = FoodService()
    with pytest.raises(ValueError) as exc_info:
        service.fetch_food_by_id(id_food)

    assert str(exc_info.value) == f"Food with id {id_food} not found"


def test_create_food(mock_food_repository, sample_food):
    """Unit test to create a food"""
    # Given
    configure_mock_repository(mock_food_repository, "create_food", sample_food)

    # When
    service = FoodService()
    result = service.create_food(sample_food)

    assert result is sample_food
    assert result.id == 1
    assert result.code == "12345"
    assert result.name == "Apple"


def test_delete_food_success(mock_food_repository):
    """Unit test to delete food with success"""
    # Given
    configure_mock_repository(mock_food_repository, "delete_food", True)
    id_food = 1

    # When
    service = FoodService()
    result = service.delete_food(id_food)

    assert result is True


def test_delete_food_fail(mock_food_repository):
    """Unit test to delete food with fail"""
    # Given
    configure_mock_repository(mock_food_repository, "delete_food", False)
    id_food = 1

    # When / Then
    service = FoodService()
    with pytest.raises(ValueError) as exc_info:
        service.delete_food(id_food)

    assert str(exc_info.value) == f"Food with id {id_food} not found to delete"
