from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.subscription import SubscriptionService
from app.errors.exceptions import ValidationError, NotFoundError

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscriptions', methods=['POST'])
@jwt_required()
def create_subscription():
    try:
        current_phone = get_jwt_identity()
        data = request.get_json()

        user = SubscriptionService.get_user_by_phone(current_phone)
        subscriptions = SubscriptionService.create_subscription(user, data['categories'])

        return jsonify([{
            'category': sub.category
        } for sub in subscriptions]), 201

    except (ValidationError, NotFoundError) as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception:
        return jsonify({
            "error_type": "CreateSubscriptionError",
            "message": "Error creando suscripciones"
        }), 500

@subscription_bp.route('/subscriptions', methods=['GET'])
@jwt_required()
def get_subscriptions():
    try:
        current_phone = get_jwt_identity()
        user = SubscriptionService.get_user_by_phone(current_phone)

        return jsonify([{
            'category': sub.category
        } for sub in user.subscriptions]), 200

    except NotFoundError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception:
        return jsonify({
            "error_type": "GetSubscriptionsError",
            "message": "Error obteniendo suscripciones"
        }), 500

@subscription_bp.route('/subscriptions', methods=['PUT'])
@jwt_required()
def update_subscriptions():
    try:
        current_phone = get_jwt_identity()
        data = request.get_json()
        user = SubscriptionService.get_user_by_phone(current_phone)

        updated_subs = SubscriptionService.replace_subscriptions(user, data['categories'])
        return jsonify([{'category': sub.category} for sub in updated_subs]), 200

    except (ValidationError, NotFoundError) as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception:
        return jsonify({
            "error_type": "UpdateSubscriptionsError",
            "message": "Error actualizando suscripciones"
        }), 500

@subscription_bp.route('/subscriptions/<string:category>', methods=['DELETE'])
@jwt_required()
def delete_subscription(category):
    try:
        current_phone = get_jwt_identity()
        user = SubscriptionService.get_user_by_phone(current_phone)

        SubscriptionService.delete_subscription(user, category)
        return jsonify({
            "message": "Suscripción eliminada exitosamente",
            "category": category
        }), 200

    except NotFoundError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception:
        return jsonify({
            "error_type": "DeleteSubscriptionError",
            "message": "Error eliminando suscripción"
        }), 500
