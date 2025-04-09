from flask import jsonify
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
    Forbidden,
    MethodNotAllowed,
    UnprocessableEntity
)
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from .exceptions import APIError


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return jsonify({
            'error_type': 'BadRequest',
            'message': 'La solicitud no es válida',
            "details": {}
        }), 400

    @app.errorhandler(401)
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(error):
        return jsonify({
            'error_type': 'Unauthorized',
            'message': 'No estás autorizado para acceder a este recurso',
            "details": {}
        }), 401

    @app.errorhandler(403)
    @app.errorhandler(Forbidden)
    def handle_forbidden(error):
        return jsonify({
            'error_type': 'Forbidden',
            'message': 'Acceso prohibido',
            "details": {}
        }), 403

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            'error_type': 'NotFound',
            'message': 'El recurso solicitado no existe',
            "details": {}
        }), 404

    @app.errorhandler(405)
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        return jsonify({
            'error_type': 'MethodNotAllowed',
            'message': 'Método HTTP no permitido para este recurso',
            "details": {}
        }), 405

    @app.errorhandler(422)
    @app.errorhandler(UnprocessableEntity)
    def handle_unprocessable_entity(error):
        return jsonify({
            'error_type': 'UnprocessableEntity',
            'message': 'Los datos proporcionados no son válidos',
            "details": {}
        }), 422

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({
            'error_type': 'InternalServerError',
            'message': 'Ocurrió un error interno en el servidor',
            "details": {}
        }), 500

    @app.errorhandler(IntegrityError)
    def handle_db_integrity_error(error):
        db.session.rollback()
        return jsonify({
            'error_type': 'DatabaseError',
            'message': 'Violación de restricción de base de datos',
            "details": {}
        }), 400


"""
🔧 ¿Cómo probarlos?
BadRequest → Mandá un JSON inválido

Unauthorized → Intentá acceder sin token

Forbidden → Bloqueá por roles o permisos

MethodNotAllowed → Mandá un PUT donde solo aceptás GET

422 → Mandá datos que no cumplen la validación del esquema
"""