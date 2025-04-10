from marshmallow import Schema, fields, validates, ValidationError

VALID_CATEGORIES = {"deportes", "tecnología", "economía", "cultura"}

class SubscriptionSchema(Schema):
    categories = fields.List(fields.Str(), required=True)

    @validates('categories')
    def validate_categories(self, categories):
        invalid = set(categories) - VALID_CATEGORIES
        if invalid:
            raise ValidationError(f"Categorías inválidas: {', '.join(invalid)}")
