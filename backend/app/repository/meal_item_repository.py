import logging
from typing import List
from sqlalchemy.exc import IntegrityError, DatabaseError
from app.models.meal_item import MealItem
from app.config.db import db


logger = logging.getLogger(__name__)


class MealItemRepository:
    def __init__(self) -> None:
        """init the class"""

    def get_all_meal_items(self) -> List[MealItem]:
        """Get all meal items from database

        Raises:
            RuntimeError: error raised if database problem

        Returns:
            List[MealItem]: the list of meal items
        """
        try:
            return db.session.query(MealItem).all()
        except Exception as e:
            logger.error("Error while get all meal items: %s", e)
            db.session.rollback()
            raise RuntimeError("Unexpected error while get all meal items") from e

    def get_meal_item_by_id(self, item_id: int) -> MealItem:
        """Get one meal item by the id

        Args:
            item_id (int): the id of item

        Raises:
            RuntimeError: error raised if database problem

        Returns:
            MealItem: The object returned
        """
        try:
            return db.session.query(MealItem).filter_by(id=item_id).first()
        except Exception as e:
            logger.error("Error while get a meal item: %s", e)
            db.session.rollback()
            raise RuntimeError("Unexpected error while get a meal item") from e

    def create_meal_item(self, item: MealItem) -> MealItem:
        """Create Meal item in database

        Args:
            item (MealItem): Meal item object

        Raises:
            ValueError: if meal item with the same name already exist
            RuntimeError: if any problem with database

        Returns:
            MealItem: The object
        """
        try:
            db.session.add(item)
            db.session.commit()
            return item
        except IntegrityError as e:
            logger.error("Integrity error while creating meal item: %s", e.orig)
            db.session.rollback()
            raise ValueError("Meal item with this name already exists.") from e
        except DatabaseError as e:
            logger.error("Database error while creating meal item: %s", e.orig)
            db.session.rollback()
            raise RuntimeError("Database error occurred while create meal item.") from e
        except Exception as e:
            logger.error("Unexpected error while create meal item: %s", e)
            db.session.rollback()
            raise RuntimeError(
                "An unexpected error occurred during meal item creation."
            ) from e

    def update_meal_item(self, meal_item: MealItem) -> MealItem:
        """Update meal item in database

        Args:
            meal_item (MealItem): the new meal item

        Raises:
            ValueError: if meal item to update not exist
            RuntimeError: if problem with database

        Returns:
            MealItem: the new object
        """
        existing_item = self.get_meal_item_by_id(meal_item.id)

        if not existing_item:
            raise ValueError(f"MealItem with id: {meal_item.id} not food")

        try:
            existing_item.quantity = meal_item.quantity
            existing_item.name = meal_item.name
            existing_item.unit = meal_item.unit
            existing_item.note = meal_item.note
            existing_item.food = meal_item.food
            existing_item.meals = meal_item.meals
            db.session.commit()
            return existing_item
        except Exception as e:
            logger.error("Unexpected error while updating meal item: %s", e)
            db.session.rollback()
            raise RuntimeError("Error updating meal item") from e

    def delete_meal_item(self, item_id: int) -> bool:
        """Delete meal item in database

        Args:
            item_id (int): the id of meal item to delete

        Raises:
            RuntimeError: raise error if any problem with database

        Returns:
            bool: true if delete is ok, false if meal item not found
        """
        item = db.session.query(MealItem).filter_by(id=item_id).first()
        if not item:
            logger.warning(
                "Impossible to delete meal item object because id: %d not found",
                item_id,
            )
            return False
        try:
            db.session.delete(item)
            db.session.commit()
            return True
        except DatabaseError as e:
            logger.error("Database error while deleting meal item: %s", e.orig)
            db.session.rollback()
            raise RuntimeError(
                "Database error occurred during delete meal item."
            ) from e
        except Exception as e:
            logger.error("Unexpected error while deleting meal item: %s", e)
            db.session.rollback()
            raise RuntimeError("An unexpected error while deleting meal item.") from e
