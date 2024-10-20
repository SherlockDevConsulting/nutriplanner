import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from jsonschema import SchemaError, ValidationError, validate

from app.services.food_service import FoodService
from app.schemas import food_schema

logger = logging.getLogger(__name__)
URL = "/foods"


class FoodRoutes:
    def __init__(self):
        self.service = FoodService()
        self.food_bp = Blueprint("food", __name__)
        self.food_bp.add_url_rule(URL, view_func=self.get_foods, methods=["GET"])
        self.food_bp.add_url_rule(
            f"{URL}/<int:food_id>", view_func=self.get_food_by_id, methods=["GET"]
        )
        self.food_bp.add_url_rule(URL, view_func=self.create_food, methods=["POST"])
        self.food_bp.add_url_rule(
            f"{URL}/<int:food_id>", view_func=self.delete_food, methods=["DELETE"]
        )

    def get_foods(self):
        """Endpoint to get all food in database /foods

        Returns:
            200: Food returned
            500: Internal Error
        """
        try:
            foods = self.service.fetch_all_foods()
            return jsonify([food.to_dict() for food in foods]), HTTPStatus.OK
        except RuntimeError as e:
            print(e)
            return {"error": "Internal Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_food_by_id(self, food_id: int):
        """Get one food by the id /foods/<int:food_id>

        Args:
            food_id (int): the id of food

        Returns:
            200: Food returned
            404: Food not found
            500: Internal Error
        """
        try:
            food = self.service.fetch_food_by_id(food_id)
            return jsonify(food.to_dict()), HTTPStatus.OK
        except ValueError:
            return {"error": "Food not found"}, HTTPStatus.NOT_FOUND
        except RuntimeError:
            return {"error": "Internal Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def create_food(self):
        """Endpoint to create food

        Returns:
            201: Food created
            400: Schema invalid or code food already exist
            500: Internal Error
        """
        try:
            data = request.get_json()
            validate(instance=data, schema=food_schema.food_schema)
            self.service.create_food(data)

            return {"success": "food created", "data": data}, HTTPStatus.CREATED

        except ValidationError as e:
            logger.error("Validation schema food error: %s", e.message)
            return {"error": "json invalid"}, HTTPStatus.BAD_REQUEST
        except SchemaError as e:
            logger.error("Food Schema invalid: %s", e.message)
            return {"error": "json invalid"}, HTTPStatus.BAD_REQUEST
        except ValueError:
            return {
                "error": "Food already exist"
            }, HTTPStatus.BAD_REQUEST
        except RuntimeError:
            return {
                "error": "Internal error while creating food"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            logger.error(e)
            return {"error": "Failed to create food"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_food(self, food_id: int):
        """Endpoint to delete food

        Args:
            food_id (int): the id of food to delete

        Returns:
            204: Food deleted
            404: Food to delete not found
            500: Internal error
        """
        try:
            self.service.delete_food(food_id)
            return {}, HTTPStatus.NO_CONTENT
        except ValueError as e:
            logger.error("Impossible to delete food for id: %d. %s", food_id, e)
            return {"error": "food to delete not found"}, HTTPStatus.NOT_FOUND
        except RuntimeError:
            return {
                "error": "Internal error while deleting food"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
