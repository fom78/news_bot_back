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
    """
    Registro de nuevo usuario
    ---
    tags:
      - Autenticación
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Register'
    responses:
      201:
        description: Usuario registrado exitosamente
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Usuario registrado exitosamente
                phone_number:
                  type: string
                  example: +549123456789
      400:
        description: Error de validación
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
      500:
        description: Error interno del servidor
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
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
    """
    Autenticación de usuario
    ---
    tags:
      - Autenticación
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Login'
    responses:
      200:
        description: Login exitoso
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                user:
                  type: object
                  properties:
                    phone_number:
                      $ref: '#/components/schemas/Register/properties/phone_number'
      401:
        description: Credenciales inválidas
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
      500:
        description: Error interno
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
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