import logging
from typing import List
from app.repository.food_repository import FoodRepository
from app.models.food import Food

logger = logging.getLogger(__name__)


class FoodService:
    def __init__(self):
        self.repository = FoodRepository()

    def fetch_all_foods(self) -> List[Food]:
        """Get all food from the repository"""
        logger.debug("Fetching all food in %s", self.fetch_all_foods.__name__)
        foods = self.repository.get_all_foods()
        print(foods[0].code)
        return foods

    def fetch_food_by_id(self, id_food: int) -> Food:
        """Get Food by id

        Args:
            id_food (int): the id of food searched

        Raises:
            ValueError: Raise if food not found

        Returns:
            Food: The object food
        """
        logger.debug("Fetch on food in %s", self.fetch_food_by_id.__name__)
        food = self.repository.get_food_by_id(id_food)

        if food is None:
            logger.error("Food with id %d not found", id_food)
            raise ValueError(f"Food with id {id_food} not found")

        return food

    def create_food(self, food: Food) -> Food:
        """Create a Food object

        Args:
            food (Food): food object
        """
        logger.debug("%s", self.create_food.__name__)
        return self.repository.create_food(food)

    def delete_food(self, food_id: int) -> bool:
        """Delete Food with id

        Args:
            food_id (int): the id of food

        Raises:
            ValueError: raise if food not found
        """
        logger.debug("%s", self.delete_food.__name__)
        result = self.repository.delete_food(food_id)
        if not result:
            raise ValueError(f"Food with id {food_id} not found to delete")

        return True
