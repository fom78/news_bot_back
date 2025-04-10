# tests/subscription/test_subscription_service.py

import pytest
from app.extensions import db
from app.auth.models import User
from app.models import Subscription
from app.services.subscription import SubscriptionService
from app.errors.exceptions import ValidationError, NotFoundError
from app.schemas.subscription_schema import VALID_CATEGORIES

def create_user(phone):
    """Helper para crear y persistir un usuario de prueba."""
    user = User(phone_number=phone)
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()
    return user

def test_get_user_by_phone_success(test_app):
    with test_app.app_context():
        user = create_user("+1000000001")
        found = SubscriptionService.get_user_by_phone(user.phone_number)
        assert found.id == user.id

def test_get_user_by_phone_not_found(test_app):
    with test_app.app_context():
        with pytest.raises(NotFoundError) as exc:
            SubscriptionService.get_user_by_phone("+0000000000")
            assert "Usuario no encontrado" in str(exc.value)

def test_validate_categories_valid():
    # No debería lanzar
    SubscriptionService.validate_categories(list(VALID_CATEGORIES))

def test_validate_categories_invalid():
    with pytest.raises(ValidationError) as exc:
        SubscriptionService.validate_categories(["invalida"])
        assert "Categorías inválidas" in str(exc.value)

def test_create_subscription_success(test_app):
    with test_app.app_context():
        user = create_user("+1000000002")
        cats = list(VALID_CATEGORIES)[:2]

        subs = SubscriptionService.create_subscription(user, cats)
        assert len(subs) == 2
        assert {s.category for s in subs} == set(cats)
        assert Subscription.query.count() == 2

def test_create_subscription_no_new(test_app):
    with test_app.app_context():
        user = create_user("+1000000003")
        cats = list(VALID_CATEGORIES)[:1]

        # Primera vez: OK
        SubscriptionService.create_subscription(user, cats)
        # Segunda vez: no hay nuevas
        with pytest.raises(ValidationError) as exc:
            SubscriptionService.create_subscription(user, cats)
            assert "No hay categorías nuevas para agregar" in str(exc.value)

def test_create_subscription_invalid_category(test_app):
    with test_app.app_context():
        user = create_user("+1000000004")
        with pytest.raises(ValidationError) as exc:
            SubscriptionService.create_subscription(user, ["invalid"])
            assert "Categorías inválidas" in str(exc.value)

def test_replace_subscriptions_success(test_app):
    with test_app.app_context():
        user = create_user("+1000000005")
        cats1 = list(VALID_CATEGORIES)[:2]
        cats2 = list(VALID_CATEGORIES)[2:4]

        SubscriptionService.create_subscription(user, cats1)
        new_subs = SubscriptionService.replace_subscriptions(user, cats2)

        assert len(new_subs) == 2
        assert {s.category for s in new_subs} == set(cats2)

def test_replace_subscriptions_invalid_category(test_app):
    with test_app.app_context():
        user = create_user("+1000000006")
        with pytest.raises(ValidationError):
            SubscriptionService.replace_subscriptions(user, ["otra"])

def test_delete_subscription_not_found(test_app):
    with test_app.app_context():
        user = create_user("+1000000008")
        with pytest.raises(NotFoundError):
            SubscriptionService.delete_subscription(user, "no-existe")
