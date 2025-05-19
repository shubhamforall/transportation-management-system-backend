"""
User ViewSet for handling user endpoints.
"""

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from utils.response import generate_response
from base.views import BaseView, RetrieveView
from authentication import get_authentication_classes

from utils.swagger import (
    responses_400,
    responses_404,
    responses_401,
    responses_400_example,
    responses_404_example,
    responses_401_example,
)

from ..serializers import UserSerializer
from ..db_access import (
    user_manager
)
from ..swagger import (
    UserResponseSerializer,
    UserListResponseSerializer,
    user_create_success_example,
    user_list_success_example,
    user_get_by_id_success_example,
    user_update_success_example,
    user_delete_success_example,
)


class UserViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling user endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = user_manager
    serializer_class = UserSerializer
    lookup_field = "user_id"

    @extend_schema(
        responses={201: UserResponseSerializer, **responses_400, **responses_401},
        examples=[
            user_create_success_example,
            responses_400_example,
            responses_401_example,
        ],
        tags=["User"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={200: UserListResponseSerializer, **responses_404, **responses_401},
        examples=[
            user_list_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=["User"],
    )
    def list_all(self, request, *args, **kwargs):
        return super().list_all(request, *args, **kwargs)

    @extend_schema(
        responses={200: UserResponseSerializer, **responses_404, **responses_401},
        examples=[
            user_get_by_id_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=["User"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={200: UserResponseSerializer, **responses_404, **responses_401},
        examples=[
            user_update_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=["User"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses={204: UserResponseSerializer, **responses_404, **responses_401},
        examples=[
            user_delete_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=["User"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UserProfileViewSet(RetrieveView, viewsets.ViewSet):
    """
    ViewSet for handling user profile endpoints.
    """

    authentication_classes = get_authentication_classes()

    def retrieve(self, request, *args, **kwargs):

        return generate_response(
            data={
                **request.user.to_dict(),
                "roles": [
                    role.to_dict()
                    for role in role_manager.list(
                        {
                            "role_id__in": [
                                role.role_id
                                for role in user_role_mapping_manager.list(
                                    {"user_id": request.user.user_id}
                                )
                            ]
                        }
                    )
                ],
            }
        )
