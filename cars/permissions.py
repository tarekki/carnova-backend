from accounts.models import UserRole


def user_is_admin(user) -> bool:
    """Staff/superuser or explicit ADMIN role can manage all cars."""
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return getattr(user, "role", None) == UserRole.ADMIN
