from werkzeug.security import generate_password_hash
from app.extensions import db
from app.errors.exceptions import ValidationError, AuthError
from .models import User

class AuthService:
    @staticmethod
    def validate_password_complexity(password):
        """Valida la complejidad de la contraseña (personalizable)"""
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        # Agregar más validaciones 

    @classmethod
    def register_user(cls, phone_number, password):
        # Validar formato de teléfono
        if not User.validate_phone(phone_number):
            raise ValidationError("Formato de teléfono inválido")
        
        # Validar contraseña
        cls.validate_password_complexity(password)
        
        # Verificar existencia de usuario
        if User.query.filter_by(phone_number=phone_number).first():
            raise ValidationError("El número ya está registrado")
        
        # Crear usuario
        user = User(phone_number=phone_number)
        user.set_password(password)
        
        # Persistir en DB
        db.session.add(user)
        db.session.commit()
        
        return user

    @staticmethod
    def authenticate_user(phone_number, password):
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if not user or not user.check_password(password):
            raise AuthError("Credenciales inválidas")
        
        return user