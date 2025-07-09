"""
This module contains the views for the auth_user app.
"""

from .auth import LoginViewSet, LogoutViewSet
from .user import UserViewSet

__all__ = [
    "UserViewSet",
    "LoginViewSet",
    "LogoutViewSet",
]
