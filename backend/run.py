import threading
import time
from flask import Flask
from app.models.food import Food
from app.models.meal_item import MealItem
from app.models.meal import Meal
import logging

from app import create_app


# app = Flask(__name__)
app = create_app()
app.config['DEBUG'] = True
logger = logging.getLogger(__name__)

def log_debug_loop():
    while True:
        logging.debug("Ceci est un message de debug")
        time.sleep(10)

def create_sample_data():
    logger.info("Coucou")
    logger.debug("DEEBUUUUUUUUUUUUUUUG")
    # Créer des macronutriments
    food_1 = Food(code="code_food_1", name="food_1")
    food_2 = Food(code="code_food_2", name="food_2")
    meal_item_1 = MealItem(quantity=100, unit='g', food=food_1)
    meal_item_2 = MealItem(quantity=50, unit="g", food=food_2)
    meal_1 = Meal(name="hey", meal_items=[meal_item_1, meal_item_2])

    print(food_1)
    print(food_1.id)
    print(meal_item_1.food)
    print(meal_item_1.quantity)
    print(meal_1.meal_items[1].quantity)

if __name__ == '__main__':

    log_thread = threading.Thread(target=log_debug_loop, daemon=True)
    log_thread.start()
    
    with app.app_context():
        create_sample_data()
        app.run(host='0.0.0.0', port=5000, debug=True)
