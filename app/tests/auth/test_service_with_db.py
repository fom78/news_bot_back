# tests/auth/test_service_with_db.py
import pytest
from app.auth.services import AuthService
from app.auth.models import User
from app.errors.exceptions import ValidationError, AuthError
from app.extensions import db

def test_register_user_with_real_db(test_app):
    with test_app.app_context():
        # Asegurarse que la tabla está vacía al comenzar
        assert User.query.count() == 0

        # Registrar usuario válido
        user = AuthService.register_user("+123456789", "password123")

        # Verificar que el usuario fue creado y guardado en la DB
        assert user.id is not None
        assert user.phone_number == "+123456789"
        assert user.check_password("password123")
        assert User.query.count() == 1

        # Intentar registrar el mismo número → debe lanzar ValidationError
        with pytest.raises(ValidationError):
            AuthService.register_user("+123456789", "otro_pass")
        

        
        


def test_authenticate_user_with_real_db(test_app):
    with test_app.app_context():
        # Creamos un usuario manualmente
        user = User(phone_number="+987654321")
        user.set_password("supersecret")
        db.session.add(user)
        db.session.commit()

        # Autenticación correcta
        authenticated_user = AuthService.authenticate_user("+987654321", "supersecret")
        assert authenticated_user.id == user.id

        # Número correcto, contraseña incorrecta
        with pytest.raises(AuthError):
            AuthService.authenticate_user("+987654321", "wrongpassword")

        # Número no registrado
        with pytest.raises(AuthError):
            AuthService.authenticate_user("+000000000", "whatever")
