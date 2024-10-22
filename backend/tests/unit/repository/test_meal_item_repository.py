# pylint: disable=W0621
# pylint: disable=C0116
import pytest
from app.models.meal_item import MealItem
from app.models.food import Food
from app.models.meal import Meal
from app.repository.meal_item_repository import MealItemRepository
from sqlalchemy.exc import IntegrityError, DatabaseError


@pytest.fixture
def mock_db(mocker):
    """Fixture to provide a mocked db"""
    mock_db = mocker.patch("app.repository.meal_item_repository.db.session")
    return mock_db


@pytest.fixture
def mock_logger(mocker):
    """Fixture to provide a mock logger"""
    mock_logger = mocker.patch("app.repository.meal_item_repository.logger")
    return mock_logger


@pytest.fixture
def sample_meal_item() -> MealItem:
    """Fixture to provide a sample food object"""
    food = Food(id=1, code="12345", name="Apple")
    meal = Meal(id=1, name="meal_test")
    return MealItem(id=1, name="meal_item_test", unit="5", food=food, meals=[meal])


def test_get_all_meal_items_success(mock_db, sample_meal_item):
    # Given
    mock_db.query().all.return_value = [sample_meal_item, sample_meal_item]

    # When
    repo = MealItemRepository()
    result = repo.get_all_meal_items()

    # Then
    assert len(result) == 2
    assert result[0] is sample_meal_item
    assert result[0] == sample_meal_item


def test_get_all_meal_items_runtime_error(mock_db, mock_logger, mocker):
    # Given
    mock_db.query().all.side_effect = Exception()

    # When
    repo = MealItemRepository()
    with pytest.raises(RuntimeError, match="Unexpected error while get all meal items"):
        repo.get_all_meal_items()

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Error while get all meal items: %s", mocker.ANY
    )


def test_get_meal_item_by_id(mock_db, sample_meal_item):
    # Given
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = sample_meal_item

    # When
    repo = MealItemRepository()
    result = repo.get_meal_item_by_id(1)

    # Then
    assert result is sample_meal_item
    assert result == sample_meal_item


def test_get_meal_item_by_id_error(mock_db, mock_logger, mocker):
    # Given
    mock_db.query.side_effect = Exception()

    # When
    repo = MealItemRepository()
    with pytest.raises(RuntimeError, match="Unexpected error while get a meal item"):
        repo.get_meal_item_by_id(1)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Error while get a meal item: %s", mocker.ANY
    )


def test_create_meal_item_success(mock_db, sample_meal_item):
    # When
    repo = MealItemRepository()
    repo.create_meal_item(sample_meal_item)

    # Then
    mock_db.add.assert_called_once_with(sample_meal_item)
    mock_db.commit.assert_called_once()


def test_create_meal_item_integrity_error(mock_db, mock_logger, sample_meal_item):
    # Given
    mock_db.add.side_effect = IntegrityError(
        statement="INSERT INTO meal_item ...",
        params=(sample_meal_item.id, sample_meal_item.name),
        orig="Duplicate entry",
    )

    # When
    repo = MealItemRepository()
    with pytest.raises(ValueError, match="Meal item with this name already exists."):
        repo.create_meal_item(sample_meal_item)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Integrity error while creating meal item: %s", "Duplicate entry"
    )


def test_create_meal_item_database_error(mock_db, mock_logger, sample_meal_item):
    # Given
    mock_db.add.side_effect = DatabaseError(
        statement="INSERT INTO ...",
        params=(sample_meal_item.id, sample_meal_item.name),
        orig="Database error",
    )

    # When
    repo = MealItemRepository()
    with pytest.raises(
        RuntimeError, match="Database error occurred while create meal item."
    ):
        repo.create_meal_item(sample_meal_item)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Database error while creating meal item: %s", "Database error"
    )


def test_create_meal_item_exception_error(
    mock_db, mock_logger, sample_meal_item, mocker
):
    # Given
    mock_db.add.side_effect = Exception()

    # When
    repo = MealItemRepository()
    with pytest.raises(
        RuntimeError, match="An unexpected error occurred during meal item creation."
    ):
        repo.create_meal_item(sample_meal_item)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Unexpected error while create meal item: %s", mocker.ANY
    )


def test_update_meal_item_success(mock_db, sample_meal_item):
    # Given
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = sample_meal_item
    sample_meal_item.name = "new_name"

    # When
    repo = MealItemRepository()
    result = repo.update_meal_item(sample_meal_item)

    # Then
    assert result.name == "new_name"


def test_update_meal_item_value_error(mock_db, sample_meal_item):
    # Given
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = None

    # When / Then
    repo = MealItemRepository()
    with pytest.raises(
        ValueError, match=f"MealItem with id: {sample_meal_item.id} not food"
    ):
        repo.update_meal_item(sample_meal_item)


def test_update_meal_item_exception(mock_db, sample_meal_item, mock_logger, mocker):
    # Given
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = sample_meal_item
    mock_db.commit.side_effect = Exception()

    # When / Then
    repo = MealItemRepository()
    with pytest.raises(RuntimeError, match="Error updating meal item"):
        repo.update_meal_item(sample_meal_item)

    mock_logger.error.assert_called_once_with(
        "Unexpected error while updating meal item: %s", mocker.ANY
    )


def test_delete_meal_item_success(mock_db, sample_meal_item):
    # Given
    item_id = 1
    mock_query = mock_db.query.return_value
    mock_query.filter_by.return_value.first.return_value = sample_meal_item

    # When
    repo = MealItemRepository()
    repo.delete_meal_item(item_id)

    # Then
    mock_db.delete.assert_called_once_with(sample_meal_item)
    mock_db.commit.assert_called_once()


def test_delete_meal_item_not_found(mock_db, mock_logger):
    # Given
    item_id = 1
    mock_query = mock_db.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    # When
    repo = MealItemRepository()
    repo.delete_meal_item(item_id)

    # Then
    mock_logger.warning.assert_called_once_with(
        "Impossible to delete meal item object because id: %d not found", item_id
    )


def test_delete_meal_item_database_error(mock_db, mock_logger):
    # Given
    id_item = 1
    mock_db.delete.side_effect = DatabaseError(
        statement="DELETE from ...",
        params=(id_item),
        orig="Database error",
    )

    # When
    repo = MealItemRepository()
    with pytest.raises(
        RuntimeError, match="Database error occurred during delete meal item."
    ):
        repo.delete_meal_item(id_item)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Database error while deleting meal item: %s", "Database error"
    )


def test_delete_meal_item_exception_error(mock_db, mock_logger, mocker):
    # Given
    id_item = 1
    mock_db.delete.side_effect = Exception()

    # When
    repo = MealItemRepository()
    with pytest.raises(
        RuntimeError, match="An unexpected error while deleting meal item."
    ):
        repo.delete_meal_item(id_item)

    # Then
    mock_db.rollback.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Unexpected error while deleting meal item: %s", mocker.ANY
    )
