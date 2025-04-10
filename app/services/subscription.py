from sqlalchemy.exc import SQLAlchemyError
from app.models import Subscription
from app.auth.models import User
from app.extensions import db
from app.errors.exceptions import ValidationError, NotFoundError
from app.schemas.subscription_schema import SubscriptionSchema
from marshmallow import ValidationError as MarshmallowValidationError

class SubscriptionService:
    @classmethod
    def get_user_by_phone(cls, phone_number):
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            raise NotFoundError("Usuario no encontrado")
        return user

    @classmethod
    def validate_categories(cls, categories):
        try:
            schema = SubscriptionSchema()
            schema.load({'categories': categories})
        except MarshmallowValidationError as e:
            raise ValidationError(", ".join(e.messages.get('categories', [])))

    @classmethod
    def create_subscription(cls, user, categories):
        cls.validate_categories(categories)

        new_subscriptions = []
        existing_categories = {sub.category for sub in user.subscriptions}

        try:
            for category in set(categories):
                if category not in existing_categories:
                    sub = Subscription(category=category, user_id=user.id)
                    db.session.add(sub)
                    new_subscriptions.append(sub)

            if not new_subscriptions:
                raise ValidationError("No hay categorías nuevas para agregar")

            db.session.commit()
            return new_subscriptions

        except SQLAlchemyError:
            db.session.rollback()
            raise

    @classmethod
    def replace_subscriptions(cls, user, categories):
        cls.validate_categories(categories)

        try:
            # Eliminar todas las suscripciones existentes
            Subscription.query.filter_by(user_id=user.id).delete()
            
            # Crear nuevas suscripciones
            new_subs = []
            for category in set(categories):
                sub = Subscription(category=category, user_id=user.id)
                db.session.add(sub)
                new_subs.append(sub)

            db.session.commit()
            return new_subs

        except SQLAlchemyError:
            db.session.rollback()
            raise

    @classmethod
    def delete_subscription(cls, user, category):
        sub = Subscription.query.filter_by(
            user_id=user.id,
            category=category
        ).first()

        if not sub:
            raise NotFoundError("Suscripción no encontrada")

        try:
            db.session.delete(sub)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
