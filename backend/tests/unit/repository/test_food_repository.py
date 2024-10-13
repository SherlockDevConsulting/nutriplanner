from app.models.food import Food
from app.repository.food_repository import FoodRepository


def test_get_all_foods(mocker):
    """Unit test to get all foods from db"""

    # Given
    mock_session = mocker.patch("app.repository.food_repository.db.session")
    mock_food_1 = Food(code="12345", name="Apple")
    mock_food_2 = Food(code="9876", name="Orange")
    mock_session.query().all.return_value = [mock_food_1, mock_food_2]

    # When
    repo = FoodRepository()
    result = repo.get_all_foods()

    # Then
    assert len(result) == 2
    assert result[0].code == "12345"
    assert result[0].name == "Apple"
    assert result[1].code == "9876"
    assert result[1].name == "Orange"


def test_get_food_by_id(mocker):
    """Unit test to get food by id"""

    # Given
    mock_session = mocker.patch("app.repository.food_repository.db.session")
    mock_food = Food(id=1, code="12345", name="Apple")
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = mock_food

    # When
    repo = FoodRepository()
    result = repo.get_food_by_id(1)

    # Then
    assert result is mock_food
    assert result.code == "12345"
    assert result.name == "Apple"


def test_create_food(mocker):
    """Unit test to create food in the database"""

    # Given
    mock_session = mocker.patch("app.repository.food_repository.db.session")
    food = Food(code="12345", name="Apple")

    # When
    repo = FoodRepository()
    repo.create_food(food)

    # Then
    mock_session.add.assert_called_once_with(food)
    mock_session.commit.assert_called_once()


def test_delete_food(mocker):
    """Unit test to delete food from the database"""

    # Given
    mock_session = mocker.patch("app.repository.food_repository.db.session")
    food_id = 1
    mock_food = Food(id=food_id, code="12345", name="Apple")
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_food

    # When
    repo = FoodRepository()
    repo.delete_food(food_id)

    # Then
    mock_session.delete.assert_called_once_with(mock_food)
    mock_session.commit.assert_called_once()


def test_delete_food_not_found(mocker):
    """Unit test to delete food from the database when food not found"""

    # Given
    mock_session = mocker.patch("app.repository.food_repository.db.session")
    food_id = 1
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None
    mock_logger = mocker.patch("app.repository.food_repository.logger")

    # When
    repo = FoodRepository()
    repo.delete_food(food_id)

    # Then
    mock_logger.warning.assert_called_once_with(
        "Impossible to delete Food object because id: %d not found", food_id
    )
