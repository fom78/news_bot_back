from flask import Flask
from app.extensions import db, migrate, jwt, swagger
from config import config
from app.schemas.swagger_definitions import swagger_config, swagger_template
from app.errors.handlers import register_error_handlers

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  

    # Configuración Swagger
    app.config['SWAGGER'] = {
        **swagger_config,
        **swagger_template
    }

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)

    # Registrar Blueprints
    from app.routes.home import home_bp
    from app.routes.subscription import subscription_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(subscription_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(home_bp)


    # Registrar manejadores de errores
    register_error_handlers(app)
    return app
