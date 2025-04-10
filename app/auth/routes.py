# app/auth/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError as MarshmallowValidationError

from app.auth.services import AuthService
from app.auth.schemas import RegisterSchema, LoginSchema
from app.errors.exceptions import ValidationError, AuthError

auth_bp = Blueprint('auth', __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = register_schema.load(request.get_json())
        user = AuthService.register_user(
            data['phone_number'],
            data['password']
        )

        return jsonify({
            "message": "Usuario registrado exitosamente",
            "phone_number": user.phone_number
        }), 201

    except MarshmallowValidationError as err:
        # return jsonify({"errors": err.messages}), 400
        raise ValidationError("Datos inválidos", payload=err.messages)
    except ValidationError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as error:
        return jsonify({
            "error": {
                "type": "AuthenticationError",
                "message": "Error en el registro",
                "details": {}
            }
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.get_json())
        user = AuthService.authenticate_user(
            data['phone_number'],
            data['password']
        )

        access_token = create_access_token(identity=user.phone_number)
        return jsonify({
            "access_token": access_token,
            "user": {
                "phone_number": user.phone_number
            }
        }), 200

    except MarshmallowValidationError as err:
        raise ValidationError("Datos inválidos", payload=err.messages)
    except AuthError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception:
        return jsonify({
            "error": {
                "type": "AuthenticationError",
                "message": "Error en el login",
                "details": {}
            }
        }), 500