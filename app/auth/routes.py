from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .services import AuthService
from app.errors.exceptions import ValidationError, AuthError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user = AuthService.register_user(
            data['phone_number'],
            data['password']
        )
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "phone_number": user.phone_number
        }), 201
    
    except ValidationError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            "error_type": "RegistrationError",
            "message": "Error en el registro"
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
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
    
    except AuthError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            "error_type": "AuthenticationError",
            "message": "Error en el login"
        }), 500