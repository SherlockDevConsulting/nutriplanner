# pylint: disable=W0621
# pylint: disable=C0116
import pytest
from app.models.food import Food
from app.repository.food_repository import FoodRepository
from sqlalchemy.exc import IntegrityError, DatabaseError


@pytest.fixture
def mock_db(mocker):
    """Fixture to provide a mocked db"""
    mock_service = mocker.patch("app.repository.food_repository.db.session")
    return mock_service


@pytest.fixture
def mock_logger(mocker):
    """Fixture to provide a mock logger"""
    mock_logger = mocker.patch("app.repository.food_repository.logger")
    return mock_logger


@pytest.fixture
def sample_food() -> Food:
    """Fixture to provide a sample food object"""
    return Food(id=1, code="12345", name="Apple")


def test_get_all_foods_success(mock_db):
    """Unit test to get all foods from db"""

    # Given
    mock_food_1 = Food(code="12345", name="Apple")
    mock_food_2 = Food(code="9876", name="Orange")
    mock_db.query().all.return_value = [mock_food_1, mock_food_2]

    # When
    repo = FoodRepository()
    result = repo.get_all_foods()

    # Then
    assert len(result) == 2
    assert result[0].code == "12345"
    assert result[0].name == "Apple"
    assert result[1].code == "9876"
    assert result[1].name == "Orange"


def test_get_all_foods_runtime_error(mock_db, mock_logger, mocker):
    """Unit test to get all foods from db"""
    # Given
    mock_db.query().all.side_effect = Exception()

    # When
    repo = FoodRepository()
    with pytest.raises(
        RuntimeError, match="An unexpected error occurred while get all foods"
    ):
        repo.get_all_foods()

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Unexpected error while get all foods: %s", mocker.ANY
    )


def test_get_food_by_id(mock_db):
    """Unit test to get food by id"""

    # Given
    food = Food(id=1, code="12345", name="Apple")
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = food

    # When
    repo = FoodRepository()
    result = repo.get_food_by_id(1)

    # Then
    assert result is food
    assert result.code == "12345"
    assert result.name == "Apple"


def test_get_food_by_id_error(mock_db, mock_logger, mocker):
    # Given
    mock_db.query.side_effect = Exception()

    # When
    repo = FoodRepository()
    with pytest.raises(
        RuntimeError, match="An unexpected error occurred while get one food"
    ):
        repo.get_food_by_id(1)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Unexpected error while get food by id: %s", mocker.ANY
    )


def test_create_food(mock_db, sample_food):
    """Unit test to create food in the database"""

    # Given
    # When
    repo = FoodRepository()
    repo.create_food(sample_food)

    # Then
    mock_db.add.assert_called_once_with(sample_food)
    mock_db.commit.assert_called_once()


def test_create_food_integrity_error(mock_db, mock_logger, sample_food):
    # Given
    mock_db.add.side_effect = IntegrityError(
        statement="INSERT INTO food (code, name) VALUES (?, ?)",
        params=(sample_food.code, sample_food.name),
        orig="Duplicate entry",
    )

    # When
    repo = FoodRepository()
    with pytest.raises(ValueError, match="Food with this code already exists."):
        repo.create_food(sample_food)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Integrity error while creating food: %s", "Duplicate entry"
    )


def test_create_food_database_error(mock_db, mock_logger, sample_food):
    # Given
    mock_db.add.side_effect = DatabaseError(
        statement="INSERT INTO food (code, name) VALUES (?, ?)",
        params=(sample_food.code, sample_food.name),
        orig="Database error",
    )

    # When
    repo = FoodRepository()
    with pytest.raises(
        RuntimeError, match="Database error occurred while create food."
    ):
        repo.create_food(sample_food)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Database error while creating food: %s", "Database error"
    )


def test_create_food_exception_error(mock_db, mock_logger, sample_food, mocker):
    # Given
    mock_db.add.side_effect = Exception()

    # When
    repo = FoodRepository()
    with pytest.raises(
        RuntimeError, match="An unexpected error occurred during food creation."
    ):
        repo.create_food(sample_food)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Unexpected error while create food: %s", mocker.ANY
    )


def test_delete_food(mock_db):
    """Unit test to delete food from the database"""

    # Given
    food_id = 1
    mock_food = Food(id=food_id, code="12345", name="Apple")
    mock_query = mock_db.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_food

    # When
    repo = FoodRepository()
    repo.delete_food(food_id)

    # Then
    mock_db.delete.assert_called_once_with(mock_food)
    mock_db.commit.assert_called_once()


def test_delete_food_not_found(mock_db, mock_logger):
    """Unit test to delete food from the database when food not found"""

    # Given
    food_id = 1
    mock_query = mock_db.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # When
    repo = FoodRepository()
    repo.delete_food(food_id)

    # Then
    mock_logger.warning.assert_called_once_with(
        "Impossible to delete Food object because id: %d not found", food_id
    )


def test_delete_food_database_error(mock_db, mock_logger):
    # Given
    id_food = 1
    mock_db.delete.side_effect = DatabaseError(
        statement=f"DELETE from food Where id = {id_food}",
        params=(id),
        orig="Database error",
    )

    # When
    repo = FoodRepository()
    with pytest.raises(
        RuntimeError, match="Database error occurred during delete food."
    ):
        repo.delete_food(id_food)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Database error while deleting food: %s", "Database error"
    )


def test_delete_food_exception_error(mock_db, mock_logger, mocker):
    # Given
    id_food = 1
    mock_db.delete.side_effect = Exception()

    # When
    repo = FoodRepository()
    with pytest.raises(
        RuntimeError, match="An unexpected error occurred while deleting food."
    ):
        repo.delete_food(id_food)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with("Unexpected error: %s", mocker.ANY)
