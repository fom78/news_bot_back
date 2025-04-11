import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secreto')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///news_bot1.db')
    DEBUG = bool(os.getenv('FLASK_DEBUG', False))

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
class DemoConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'demo-secret'
class SwaggerConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_SWAGGER_URL', 'sqlite:///db_swagger1.db')
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'swagger': SwaggerConfig,
    'default': DevelopmentConfig
}