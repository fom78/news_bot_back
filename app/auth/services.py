# app/auth/services.py
from app.extensions import db
from app.errors.exceptions import ValidationError, AuthError
from .models import User

class AuthService:
    @classmethod
    def register_user(cls, phone_number, password):
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            raise ValidationError("El número está registrado")


        user = User(phone_number=phone_number)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def authenticate_user(phone_number, password):
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user or not user.check_password(password):
            raise AuthError("Credenciales inválidas")
        return user
