# app/schemas/swagger_definitions.py

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
    "openapi": "3.0.3",  # Solo esta línea es crítica
}

swagger_template =  {
    "openapi": "3.0.3",
    "info": {
        "title": "News Bot API",
        "description": "API para gestión de suscripciones",
        "version": "1.0.0"
    },
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        },
        "schemas": {
            "Register": {
                "type": "object",
                "required": ["phone_number", "password"],
                "properties": {
                    "phone_number": {
                        "type": "string",
                        "pattern": "^\\+\\d{8,15}$",
                        "example": "+549123456789"
                    },
                    "password": {
                        "type": "string",
                        "minLength": 8,
                        "example": "SecurePass123"
                    }
                }
            },
            "Login": {
                "type": "object",
                "required": ["phone_number", "password"],
                "properties": {
                    "phone_number": {
                        "$ref": "#/components/schemas/Register/properties/phone_number"
                    },
                    "password": {
                        "type": "string",
                        "example": "SecurePass123"
                    }
                }
            },
            "SubscriptionRequest": {
                "type": "object",
                "required": ["categories"],
                "properties": {
                    "categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["deportes", "tecnología", "economía", "cultura"]
                        },
                        "example": ["deportes", "tecnología"]
                    }
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "error_type": {"type": "string"},
                    "message": {"type": "string"},
                    "details": {"type": "object"}
                }
            }
        }
    }
}