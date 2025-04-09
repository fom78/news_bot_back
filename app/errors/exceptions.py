# Clase base para errores personalizados de API
class APIError(Exception):
    """Base class for API exceptions"""
    def __init__(self, message, status_code=400, error_type=None, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.error_type = error_type or self.__class__.__name__
        self.payload = payload or {}

    def to_dict(self):
        return {
            "error": {
                "type": self.error_type,
                "message": self.message,
                "details": self.payload
            }
        }

# Error para validaciones
class ValidationError(APIError):
    """Raised when data validation fails"""
    pass

# Error cuando no se encuentra un recurso
class NotFoundError(APIError):
    """Raised when a resource is not found"""
    def __init__(self, message="Recurso no encontrado", payload=None):
        super().__init__(message, status_code=404, payload=payload)

# Error de autenticación/autorización
class AuthError(APIError):
    """Raised for authentication/authorization failures"""
    def __init__(self, message="No autorizado", payload=None):
        super().__init__(message, status_code=401, payload=payload)
