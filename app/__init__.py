from flask import Flask, request, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.extensions import db, migrate, jwt, swagger
from config import config
from app.schemas.swagger_definitions import swagger_config, swagger_template
from app.errors.handlers import register_error_handlers

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  

    # Swagger UI config
    app.config['SWAGGER'] = {
        **swagger_config,
        **swagger_template
    }

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)

    # DB temporal si se accede desde Swagger
    @app.before_request
    def switch_to_swagger_db():
        if request.headers.get("X-Demo-ModeDespues") == "true":
            if not hasattr(app, 'swagger_engine'):
                app.swagger_engine = create_engine('sqlite:///db_swagger.db')
                app.swagger_session = scoped_session(sessionmaker(bind=app.swagger_engine))

            g.original_session = db.session
            db.session = app.swagger_session

    @app.teardown_request
    def restore_db_session(exception=None):
        if hasattr(g, 'original_session'):
            db.session.remove()
            db.session = g.original_session

    @app.after_request
    def inject_swagger_interceptor(response):
        if request.path == "/swagger/" and response.content_type.startswith("text/html"):
            content = response.get_data(as_text=True)
            interceptor_script = """
            <script>
            window.onload = function () {
                const ui = SwaggerUIBundle({
                    url: '/apispec.json',
                    dom_id: '#swagger-ui',
                    presets: [SwaggerUIBundle.presets.apis],
                    layout: "BaseLayout",
                    requestInterceptor: function (req) {
                        req.headers['X-Demo-Mode'] = 'true';
                        return req;
                    }
                });
            }
            </script>
            """
            content = content.replace('</body>', interceptor_script + '</body>')
            response.set_data(content)
        return response

    # Registrar blueprints
    from app.routes.home import home_bp
    from app.routes.subscription import subscription_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(subscription_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(home_bp)

    # Manejadores de errores
    register_error_handlers(app)
    
    return app
