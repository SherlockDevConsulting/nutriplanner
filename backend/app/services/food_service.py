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
        try:
            foods = self.repository.get_all_foods()
        except RuntimeError as e:
            raise RuntimeError() from e

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
        try:
            food = self.repository.get_food_by_id(id_food)
            if food is None:
                logger.error("Food with id %d not found", id_food)
                raise ValueError(f"Food with id {id_food} not found")

            return food

        except RuntimeError as e:
            raise RuntimeError() from e

    def create_food(self, data: dict) -> Food:
        """Create a Food object

        Args:
            food (dict): json
        """
        logger.debug("%s", self.create_food.__name__)
        try:
            food = Food(
                code=data["code"],
                name=data["name"],
                brands=data.get("brands"),
                serving_quantity=data.get("serving_quantity"),
                unit=data.get("unit"),
                raw=data.get("raw"),
                energy_serving=data.get("energy_serving"),
                energy_100g=data.get("energy_100g"),
                fiber_serving=data.get("fiber_serving"),
                fiber_100g=data.get("fiber_100g"),
                salt_serving=data.get("salt_serving"),
                salt_100g=data.get("salt_100g"),
                carbohydrates_100g=data.get("carbohydrates_100g"),
                carbohydrates_serving=data.get("carbohydrates_serving"),
                fat_100g=data.get("fat_100g"),
                fat_serving=data.get("fat_serving"),
                proteins_100g=data.get("proteins_100g"),
                proteins_serving=data.get("proteins_serving"),
            )

            return self.repository.create_food(food)
        except ValueError as e:
            raise ValueError from e
        except RuntimeError as e:
            raise RuntimeError from e
        except Exception as e:
            logger.error(e)
            raise RuntimeError from e

    def delete_food(self, food_id: int) -> bool:
        """Delete Food with id

        Args:
            food_id (int): the id of food

        Raises:
            ValueError: raise if food not found
        """
        logger.debug("%s", self.delete_food.__name__)
        try:
            result = self.repository.delete_food(food_id)
            if not result:
                raise ValueError(f"Food with id {food_id} not found to delete")

            return True
        except RuntimeError as e:
            raise RuntimeError from e
