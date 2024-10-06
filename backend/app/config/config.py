import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret'

    #App
    APP_DEBUG = os.environ.get('APP_DEBUG')

    # Database
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #'postgresql://nutriplanner:pass@localhost:5431/nutriplanner'
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        raise ValueError("Some database environment variables are missing!")

    # Api
    OPENFOODFACTS_API_URL = os.environ.get('OPENFOODFACTS_API_URL')


    
