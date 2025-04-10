import pytest
from app.auth.services import AuthService
from app.errors.exceptions import ValidationError, AuthError
import app.auth.services as auth_services


def test_register_user_success(mocker, test_app):
    # Simular que no hay usuario con ese número
    mock_query = mocker.patch.object(auth_services.User, "query")
    mock_query.filter_by.return_value.first.return_value = None

    # Mockear session
    mock_add = mocker.patch.object(auth_services.db.session, "add")
    mock_commit = mocker.patch.object(auth_services.db.session, "commit")

    # Ejecutar
    user = AuthService.register_user("+123456789", "password123")

    # Verificar que se llamó correctamente
    mock_add.assert_called_once()
    mock_commit.assert_called_once()


def test_register_user_existing_number(mocker):
    # Simular que ya existe un usuario con ese número
    mock_query = mocker.patch.object(auth_services.User, "query")
    # devuelvo un usuario cualquiera para simular que ya existe
    mock_query.filter_by.return_value.first.return_value = "existing_user"

    # Voy a ejecutar algo que debería lanzar un ValidationError... si no lo lanza, el test falla
    with pytest.raises(ValidationError):
        # Al ejecutar esto, debería lanzar un ValidationError porque el número ya existe
        # y no se debería llegar a la línea de abajo (donde se registra el usuario)
        AuthService.register_user("+123456789", "password123")


def test_authenticate_user_success(mocker, test_app):
    # Creamos un mock de usuario y simulamos que la contraseña es válida
    mock_user = mocker.MagicMock()
    mock_user.check_password.return_value = True

    # Mockeamos la consulta a la base de datos: User.query.filter_by(...).first()
    mock_query = mocker.patch.object(auth_services.User, "query")
    mock_query.filter_by.return_value.first.return_value = mock_user

    # Ejecutamos el método que queremos testear
    user = AuthService.authenticate_user("+123456789", "password123")

    # Verificamos que se devolvió el mock de usuario (autenticación exitosa)
    assert user == mock_user

    # Aseguramos que se llamó al método check_password con la contraseña esperada
    mock_user.check_password.assert_called_once_with("password123")

    # Validamos que se buscó en la base al usuario con el número correcto
    mock_query.filter_by.assert_called_once_with(phone_number="+123456789")

def test_authenticate_user_invalid_credentials(mocker, test_app):
    # Usuario no encontrado
    mock_query = mocker.patch.object(auth_services.User, "query")
    mock_query.filter_by.return_value.first.return_value = None

    with pytest.raises(AuthError):
        AuthService.authenticate_user("+123456789", "wrongpass")

    # Usuario encontrado pero contraseña incorrecta
    mock_user = mocker.MagicMock()
    mock_user.check_password.return_value = False
    mock_query.filter_by.return_value.first.return_value = mock_user

    with pytest.raises(AuthError):
        AuthService.authenticate_user("+123456789", "wrongpass")
