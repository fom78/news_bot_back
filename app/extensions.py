from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from app.schemas.swagger_definitions import swagger_template

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
# swagger = Swagger()
swagger = Swagger(template=swagger_template)