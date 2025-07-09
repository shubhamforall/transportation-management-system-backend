"""
This module contains the models for the authentication system.
It includes the User, Role, Token, Permission, UserRoleMapping,
and RolePermissionMapping models.
"""

from .token import Token

__all__ = ["Token"]
