import logging
from typing import List
from app import db
from app.models.food import Food

logger = logging.getLogger(__name__)


class FoodRepository:

    def __init__(self):
        """Init The class"""

    def get_all_foods(self) -> List[Food]:
        """Get all food from database

        Returns:
            List[Food]: the list of food elements
        """
        return db.session.query(Food).all()

    def get_food_by_id(self, food_id: int) -> Food:
        """Get one food by the id

        Args:
            food_id (int): the id of food

        Returns:
            Food: The object food
        """
        return (
            db.session.query(Food).filter_by(id=food_id).first()
        )

    def create_food(self, food: Food) -> Food:
        """Create Food in database

        Args:
            food (Food): Food object
        """
        db.session.add(food)
        db.session.commit()
        return Food

    def delete_food(self, food_id: int) -> bool:
        """delete food in database

        Args:
            food_id (int): the id of food
         Returns:
            boolean depends if food exist
        """
        food = db.session.query(Food).filter_by(id=food_id).first()
        if food:
            db.session.delete(food)
            db.session.commit()
            return True
        else:
            logger.warning(
                "Impossible to delete Food object because id: %d not found", food_id
            )
            return False
