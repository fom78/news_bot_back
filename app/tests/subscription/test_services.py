# tests/subscription/test_services.py
import pytest
from app.services.subscription import SubscriptionService
from app.auth.models import User
from app.models import Subscription
from app.errors.exceptions import ValidationError, NotFoundError
from app.extensions import db

@pytest.mark.clean_users
def test_create_subscription(test_app):
    with test_app.app_context():
        # Setup
        user = User(phone_number="+123456789")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()

        # Test creación válida
        valid_categories = ["deportes", "tecnología"]
        subs = SubscriptionService.create_subscription(user, valid_categories)
        
        assert len(subs) == 2
        assert {s.category for s in subs} == set(valid_categories)
        assert Subscription.query.count() == 2

        # Test categorías duplicadas
        with pytest.raises(ValidationError) as exc:
            SubscriptionService.create_subscription(user, valid_categories)
            assert "No hay categorías nuevas" in str(exc.value)

        # Test categorías inválidas
        with pytest.raises(ValidationError):
            SubscriptionService.create_subscription(user, ["categoria_falsa"])

@pytest.mark.clean_users
def test_replace_subscriptions(test_app):
    db.session.close()
    with test_app.app_context():
        # Setup con usuario único
        user = User(phone_number="+987654321")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        
        # Forzar generación de ID
        db.session.refresh(user)
        
        # Crear suscripciones iniciales
        initial_categories = ["deportes", "tecnología"]
        SubscriptionService.create_subscription(user, initial_categories)
        
        # Forzar limpieza de caché
        db.session.expire_all()

        # Test reemplazo válido
        new_categories = ["economía", "cultura"]
        new_subs = SubscriptionService.replace_subscriptions(user, new_categories)
        
        assert len(new_subs) == 2
        assert {s.category for s in new_subs} == set(new_categories)
        assert Subscription.query.count() == 2

        # Verificar que las antiguas fueron eliminadas
        remaining_categories = [s.category for s in user.subscriptions]
        assert "deportes" not in remaining_categories
        assert "tecnología" not in remaining_categories

@pytest.mark.clean_users
def test_delete_subscription(test_app):
    with test_app.app_context():
        # Setup
        user = User(phone_number="+555555555")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        
        # Crear suscripción
        SubscriptionService.create_subscription(user, ["deportes"])
        assert Subscription.query.count() == 1

        # Test eliminación exitosa
        SubscriptionService.delete_subscription(user, "deportes")
        assert Subscription.query.count() == 0

        # Test eliminar inexistente
        with pytest.raises(NotFoundError):
            SubscriptionService.delete_subscription(user, "deportes")

@pytest.mark.clean_users
def test_get_user_by_phone(test_app):
    with test_app.app_context():
        # Setup
        user = User(phone_number="+999999999")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()

        # Test búsqueda exitosa
        found_user = SubscriptionService.get_user_by_phone("+999999999")
        assert found_user.id == user.id

        # Test usuario no encontrado
        with pytest.raises(NotFoundError):
            SubscriptionService.get_user_by_phone("+000000000")