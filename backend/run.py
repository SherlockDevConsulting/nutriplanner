from flask import Flask
from app.models.food import Food
from app.models.meal_item import MealItem
from app.models.meal import Meal


app = Flask(__name__)

def create_sample_data():
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
    print(meal_1)
    print(meal_1.meal_items[1].quantity)

if __name__ == '__main__':
    with app.app_context():
        create_sample_data()
