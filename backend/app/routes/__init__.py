from flask import Blueprint
from .food_routes import food_bp
# from .meal_item_routes import meal_item_bp
# from .meal_routes import meal_bp

def init_routes(app):
    # Enregistrement des blueprints (chacun représentant un ensemble de routes)
    app.register_blueprint(food_bp, url_prefix='/api/food')
    # app.register_blueprint(meal_item_bp, url_prefix='/api/meal-item')
    # app.register_blueprint(meal_bp, url_prefix='/api/meal')
