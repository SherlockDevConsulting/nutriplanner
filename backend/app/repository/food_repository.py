import logging
from typing import List
from sqlalchemy.exc import IntegrityError, DatabaseError
from app.models.food import Food
from app.config.db import db

logger = logging.getLogger(__name__)


class FoodRepository:

    def __init__(self):
        """Init The class"""

    def get_all_foods(self) -> List[Food]:
        """Get all food from database

        Returns:
            List[Food]: the list of food elements
        """
        try:
            return db.session.query(Food).all()
        except Exception as e:
            logger.error("Unexpected error while get all foods: %s", e)
            db.session.rollback()
            raise RuntimeError(
                "An unexpected error occurred while get all foods"
            ) from e

    def get_food_by_id(self, food_id: int) -> Food:
        """Get one food by the id

        Args:
            food_id (int): the id of food

        Returns:
            Food: The object food
        """
        try:
            return db.session.query(Food).filter_by(id=food_id).first()
        except Exception as e:
            logger.error("Unexpected error while get food by id: %s", e)
            db.session.rollback()
            raise RuntimeError("An unexpected error occurred while get one food") from e

    def create_food(self, food: Food) -> Food:
        """Create Food in database

        Args:
            food (Food): Food object
        """
        try:
            db.session.add(food)
            db.session.commit()
            return food
        except IntegrityError as e:
            logger.error("Integrity error while creating food: %s", e.orig)
            db.session.rollback()
            raise ValueError("Food with this code already exists.") from e
        except DatabaseError as e:
            logger.error("Database error while creating food: %s", e.orig)
            db.session.rollback()
            raise RuntimeError("Database error occurred while create food.") from e
        except Exception as e:
            logger.error("Unexpected error while create food: %s", e)
            db.session.rollback()
            raise RuntimeError(
                "An unexpected error occurred during food creation."
            ) from e

    def delete_food(self, food_id: int) -> bool:
        """delete food in database

        Args:
            food_id (int): the id of food
         Returns:
            boolean depends if food exist
        """
        food = db.session.query(Food).filter_by(id=food_id).first()
        if not food:
            logger.warning(
                "Impossible to delete Food object because id: %d not found", food_id
            )
            return False
        try:
            db.session.delete(food)
            db.session.commit()
            return True
        except DatabaseError as e:
            logger.error("Database error while deleting food: %s", e.orig)
            db.session.rollback()
            raise RuntimeError("Database error occurred during delete food.") from e
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            db.session.rollback()
            raise RuntimeError(
                "An unexpected error occurred while deleting food."
            ) from e
