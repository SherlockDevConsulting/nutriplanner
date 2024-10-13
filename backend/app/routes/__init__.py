
from app.routes.food_routes import FoodRoutes, food_blueprint
from app.routes.logging_routes import log_blueprint


food_route = FoodRoutes()

# Enregistre le blueprint
def register_routes(app):
    """Method to register all blueprint

    Args:
        app: The application
    """
    app.register_blueprint(log_blueprint)
    
