from app.routes.food_routes import FoodRoutes
from app.routes.logging_routes import log_blueprint


food_route = FoodRoutes()


# Enregistre le blueprint
def register_routes(app):
    """Method to register all blueprint

    Args:
        app: The application
    """
    app.register_blueprint(log_blueprint)
    app.register_blueprint(food_route.food_bp)
