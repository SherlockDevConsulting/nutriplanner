import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///nutriplanner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/api/v0/product"