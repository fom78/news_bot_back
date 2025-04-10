# app/auth/schemas.py
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class RegisterSchema(Schema):
    phone_number = fields.String(
        required=True,
        validate=validate.Regexp(r'^\+\d{8,15}$', error="Formato de teléfono inválido")
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, error="La contraseña debe tener al menos 8 caracteres")
    )

class LoginSchema(Schema):
    phone_number = fields.String(required=True)
    password = fields.String(required=True)