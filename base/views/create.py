from django.db import models
from rest_framework import status, serializers

from base import constants
from base.db_access import Manager

from utils.messages import success
from utils.response import generate_response
from utils.exceptions import ValidationError
from utils import functions as common_functions


class CreateView:
    """
    A base view class for handling create operations using the Manager class.
    This class provides a standard implementation for object creation,
    including validation, data processing, and database persistence.

    Attributes:
        many (bool): Indicates whether the operation handles multiple objects at once.
        manager (Manager): An instance responsible for handling database interactions.
        serializer_class (serializers.Serializer): The serializer used to validate input data.
    """

    many = False
    manager: Manager = None
    is_common_data_needed = True
    serializer_class: serializers.Serializer = None

    @classmethod
    def get_method_view_mapping(cls):
        return {constants.POST: "create"}

    def post_save(self, obj: models.Model, **kwargs):
        """
        A hook executed after the object is saved in the database.
        This method allows additional modifications or operations on the saved object.

        Args:
            obj (models.Model): The saved object instance.
            **kwargs: Additional keyword arguments.

        Returns:
            models.Model: The modified object after post-save operations.
        """
        return generate_response(
            data=obj.to_dict(),
            status_code=status.HTTP_201_CREATED,
            messages={"message": success.CREATED_SUCCESSFULLY},
        )

    def pre_save(self, data: dict | list, **kwargs):
        """
        A hook executed before saving the object.
        This method allows preprocessing of data, such as adding default values.

        Args:
            data (dict | list): The validated input data.
            **kwargs: Additional keyword arguments.

        Returns:
            dict | list: The processed data before saving.
        """
        return data

    def add_common_data(
        self,
        data: dict | list,
        request,
        many=False,
    ):
        """
        Adds common metadata fields to the object, such as `created_by` and `updated_by`.

        Args:
            data (dict | list): The input data to be updated with common metadata.
            request (Request): The HTTP request containing user information.
            many (bool): Determines if multiple objects are being processed.

        Returns:
            dict | list: The updated data with additional metadata fields.
        """
        user_id = request.user.user_id


        if many:
            data_list = []
            for item in data:
                item["created_by"] = user_id
                item["updated_by"] = user_id

                data_list.append(item)

            return data_list

        data["created_by"] = user_id
        data["updated_by"] = user_id


        return data

    def create(self, request):
        """
        Handles the object creation process, including validation, data enrichment,
        database persistence, and response generation.

        Args:
            request (Request): The HTTP request containing input data.

        Returns:
            Response: A success response with the created object(s) or an error message if validation fails.
        """
        serializer_obj: serializers.Serializer = self.serializer_class(
            data=request.data, many=self.many
        )

        is_valid = serializer_obj.is_valid()

        if not is_valid:
            raise ValidationError(serializer_obj.errors)

        data = serializer_obj.validated_data

        if self.is_common_data_needed:
            data = self.add_common_data(data=data, request=request, many=self.many)

        data = self.pre_save(data=data, request=request)

        obj = self.manager.create(data, many=self.many)

        return self.post_save(obj=obj, data=data, request=request)
