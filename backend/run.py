from flask import Blueprint
from app.models.food import Food
from app.models.meal_item import MealItem
from app.models.meal import Meal
import logging

from app import create_app, db

# app = Flask(__name__)
app = create_app()

sample_data_bp = Blueprint('sample_data', __name__)

@sample_data_bp.route('/create_sample_data')
def create_sample_data():
    with app.app_context():
        logger = logging.getLogger(__name__)
        logger.info("Coucou")

        food_1 = Food(code="code_food_1", name="food_1")
        food_2 = Food(code="code_food_2", name="food_2")
        meal_item_1 = MealItem(quantity=100, unit='g', food=food_1)
        meal_item_2 = MealItem(quantity=50, unit="g", food=food_2)
        meal_1 = Meal(name="hey", meal_items=[meal_item_1, meal_item_2])

        # Ajouter les objets a la base de donnees
        db.session.add(food_1)
        db.session.add(food_2)
        db.session.add(meal_item_1)
        db.session.add(meal_item_2)
        db.session.add(meal_1)
        db.session.commit()

    return "Sample data created!", 200

app.register_blueprint(sample_data_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
