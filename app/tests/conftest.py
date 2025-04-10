import pytest
from app import create_app, db as _db
from flask_jwt_extended import create_access_token
from app.auth.models import User
from app.models import Subscription
import random

# Este hook le avisa a pytest que usamos un marker custom
def pytest_configure(config):
    config.addinivalue_line("markers", "clean_users: limpia la tabla User antes del test")

@pytest.fixture(autouse=True)
def clean_users_marker(request,db):
    if "clean_users" in request.keywords:
        # Limpiar todas las tablas relevantes
        db.session.execute(db.delete(Subscription))
        db.session.execute(db.delete(User))
        db.session.commit()

@pytest.fixture(scope="session")
def test_app():
    """Crea una instancia de la app para toda la sesión de tests."""
    app = create_app("testing")
    return app

@pytest.fixture(scope="session")
def db(test_app):
    """Crea y destruye la base de datos para los tests."""
    with test_app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope="function", autouse=True)
def session(db):
    """Rollback automático para cada test (aislamiento)."""
    db.session.begin_nested()
    yield db.session
    db.session.rollback()

@pytest.fixture(scope="function")
def test_client(test_app):
    """Cliente para hacer requests de prueba."""
    return test_app.test_client()

@pytest.fixture
def new_user(db):
    """Usuario de prueba para login, etc."""
    user = User(phone_number="+111111111", password_hash="")
    user.set_password("test123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def access_token(test_client):
    """Genera un JWT con usuario único para cada test"""
    phone = f"+1{random.randint(100000000, 999999999)}"  # Número único
    user = User(phone_number=phone)
    user.set_password("test123")
    db.session.add(user)
    db.session.commit()
    return create_access_token(identity=phone)

