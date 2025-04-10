import pytest
from app import create_app, db

@pytest.fixture(scope="module")
def test_app():
    # Usamos la configuración de testing que apunta a SQLite en memoria
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def test_client(test_app):
    return test_app.test_client()
