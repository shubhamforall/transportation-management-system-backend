"""
User Serializer for Swagger Documentation
"""

from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample

from utils.messages import success
from utils.swagger import PaginationSerializer


class UserSerializer(serializers.Serializer):
    """
    Serializer for both creating and updating a user.
    """

    email = serializers.EmailField(
        required=True,
        help_text="User's email address."
    )
    profile_photo = serializers.CharField(
        required=False,
        help_text="URL or path to the user's profile photo.",
        allow_blank=True
    )
    phone_number = serializers.IntegerField(
        required=True,
        help_text="User's phone number."
    )
    last_name = serializers.CharField(
        required=True,
        max_length=16,
        help_text="User's last name."
    )
    first_name = serializers.CharField(
        required=True,
        max_length=16,
        help_text="User's first name."
    )


class UserResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of user-related endpoints.
    """

    data = UserSerializer(help_text="User details.")
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


class UserListDataSerializer(serializers.Serializer):
    """
    Serializer for the data field in user list response.
    """

    list = UserSerializer(many=True, help_text="List of user records.")
    pagination = PaginationSerializer(
        help_text="Pagination information for the list of users."
    )


class UserListResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the user list endpoint.
    """

    data = UserListDataSerializer(help_text="Users and pagination.")
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


# Swagger Examples

user_create_success_example = OpenApiExample(
    name="Create User - Success",
    value={
        "data": {
            "email": "user@example.com",
            "user_id": "9d018a56-abd9-4dfd-b606-80ce3ba8f53f",
            "profile_photo": "https://cdn.example.com/photos/user.jpg",
            "phone_number": 9876543210,
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe"
        },
        "errors": None,
        "messages": success.CREATED_SUCCESSFULLY,
        "status_code": 201,
        "is_success": True
    },
    response_only=True,
    status_codes=["201"]
)

user_list_success_example = OpenApiExample(
    name="List Users - Success",
    value={
        "data": {
            "list": [
                {
                    "email": "alice@example.com",
                    "user_id": "12345678-abcd-efgh-ijkl-1234567890ab",
                    "profile_photo": "",
                    "phone_number": 1234567890,
                    "first_name": "Alice",
                    "last_name": "Smith",
                    "full_name": "Alice Smith"
                },
                {
                    "email": "bob@example.com",
                    "user_id": "23456789-abcd-efgh-ijkl-1234567890ab",
                    "profile_photo": "https://cdn.example.com/photos/bob.jpg",
                    "phone_number": 9988776655,
                    "first_name": "Bob",
                    "last_name": "Brown",
                    "full_name": "Bob Brown"
                }
            ],
            "pagination": {
                "count": 2,
                "page_size": 10,
                "current_page": 1,
                "total_pages": 1
            }
        },
        "errors": None,
        "messages": None,
        "status_code": 200,
        "is_success": True
    },
    response_only=True,
    status_codes=["200"]
)

user_get_by_id_success_example = OpenApiExample(
    name="Get User by Id - Success",
    value={
        "data": {
            "email": "user@example.com",
            "user_id": "9d018a56-abd9-4dfd-b606-80ce3ba8f53f",
            "profile_photo": "https://cdn.example.com/photos/user.jpg",
            "phone_number": 9876543210,
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe"
        },
        "errors": None,
        "messages": None,
        "status_code": 200,
        "is_success": True
    },
    response_only=True,
    status_codes=["200"]
)

user_update_success_example = OpenApiExample(
    name="Update User - Success",
    value={
        "data": {
            "email": "user@example.com",
            "user_id": "9d018a56-abd9-4dfd-b606-80ce3ba8f53f",
            "profile_photo": "https://cdn.example.com/photos/user_updated.jpg",
            "phone_number": 9123456780,
            "first_name": "Johnny",
            "last_name": "Doe",
            "full_name": "Johnny Doe"
        },
        "errors": None,
        "messages": success.UPDATED_SUCCESSFULLY,
        "status_code": 200,
        "is_success": True
    },
    response_only=True,
    status_codes=["200"]
)

user_delete_success_example = OpenApiExample(
    name="Delete User - Success",
    value={
        "data": None,
        "errors": None,
        "messages": success.DELETED_SUCCESSFULLY,
        "status_code": 204,
        "is_success": True
    },
    response_only=True,
    status_codes=["204"]
)
