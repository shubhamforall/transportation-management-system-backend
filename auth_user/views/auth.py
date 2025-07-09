"""
Login and Logout ViewSets for handling user authentication.
"""

import secrets

from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema

from base.views import CreateView, DeleteView

from authentication import get_authentication_classes
from authentication.exception import WrongCredentialsException

from utils.cache import cache
from utils.response.response import generate_response
from utils.swagger import (
    responses_400,
    responses_401,
    responses_400_example,
)


from ..serializers import LoginSerializer
from ..db_access import token_manager, user_manager
from ..serializers.swagger import (
    LoginResponseSerializer,
    LogoutResponseSerializer,
    login_success_example,
    logout_success_example,
    responses_401_example,
)


class LoginViewSet(CreateView, viewsets.ViewSet):
    """
    ViewSet for handling login endpoints.
    """

    manager = token_manager
    authentication_classes = []
    is_common_data_needed = False
    serializer_class = LoginSerializer

    def pre_save(self, data: dict, **kwargs):
        """
        Handle user login by validating credentials and generating a token.
        """
        user_obj = user_manager.get(
            {"email": data["username"], "password": data["password"]}
        )

        if not user_obj:
            raise WrongCredentialsException()

        self.manager.delete({"user": user_obj}, soft_delete=False)

        token = secrets.token_hex(16).upper()

        cache.set(f"user_token:{user_obj.user_id}", token)
        print("Token set in cache:", cache.get(f"user_token:{user_obj.user_id}"))

        return {"user": user_obj, "token": secrets.token_hex(16).upper()}

    def post_save(self, obj, **kwargs):
        """
        Handle post-save actions after user login.
        """
        data = obj.to_dict()
        user = obj.user

        full_name = f"{user.first_name} {user.last_name}".strip()

        data.update(
            {
                "full_name": full_name,
            }
        )

        return generate_response(
            data=data,
            status_code=status.HTTP_201_CREATED,
            messages={"message": "Logged in successful."},
        )

    @extend_schema(
        request=LoginSerializer,
        responses={201: LoginResponseSerializer, **responses_401, **responses_400},
        examples=[login_success_example, responses_401_example, responses_400_example],
        tags=["Authentication"],
    )
    def create(self, request, *args, **kwargs):
        """Handle user login by validating credentials and generating a token."""

        return super().create(request, *args, **kwargs)


class LogoutViewSet(DeleteView, viewsets.ViewSet):
    """
    ViewSet for handling logout related endpoints.
    """

    manager = token_manager

    authentication_classes = get_authentication_classes()

    @extend_schema(
        request=LogoutResponseSerializer,
        responses={204: LogoutResponseSerializer, **responses_401},
        examples=[logout_success_example, responses_401_example],
        tags=["Authentication"],
    )
    def destroy(self, request, **kwargs):
        """
        Handle user logout by deleting the token associated with the user.
        """

        self.manager.delete({"user": request.user}, soft_delete=False)

        cache.delete(f"user_token:{request.user.id}")

        return generate_response(
            data=None,
            messages={"message": "Logged out successfully."},
            status_code=status.HTTP_204_NO_CONTENT,
        )
