"""
This is the model BaseManager class which is used to perform CRUD operations on the models.
"""

from typing import Union, TypeVar, Generic, overload, List, Dict

from rest_framework import status
from django.db.models import Q, F, Model
from django.db.models.query import QuerySet

from utils.messages import error
from utils.pagination import Pagination
from utils.exceptions import CommonError


T = TypeVar("T", bound=Model)


class QueryBuilder:
    """
    Recursively converts a dictionary into a Django Q object for complex query filtering.

    This function dynamically constructs Django ORM queries using AND (&), OR (|), and NOT (~) conditions.

    Supported Features:
    - **Basic Key-Value Queries:** `{"first_name": "John"}`
    - **AND Condition:** `{"AND": [{"first_name": "John"}, {"age": 30}]}`
    - **OR Condition:** `{"OR": [{"last_name": "Doe"}, {"city": "New York"}]}`
    - **Nested Conditions:** `{"AND": [{"first_name": "Alice"}, {"OR": [{"age__gte": 25}, {"city": "Boston"}]}]}`
    - **NOT Conditions:** `{"NOT": {"last_name": "Smith"}}` → `~Q(last_name="Smith")`
    - **Direct Django ORM Lookups:** You can pass field lookups directly, e.g., `{"age__gte": 18}`.

    Args:
        query (dict): A dictionary representing query conditions.

    Returns:
        Q: A Django Q object that can be used in ORM queries.

    Example Usage:
    ```
    python
        query = {
            "AND": [
                {"first_name__icontains": "alice"},
                {"age__gte": 25},
                {
                    "OR": [
                        {"NOT": {"last_name": "Smith"}},
                        {"city": "Los Angeles"},
                        {"score__gt": {"F": "high_score"}}
                    ]
                }
            ]
        }

        query_builder = QueryBuilder()
        q_filter = query_builder.build_query(query)

        results = MyModel.objects.filter(q_filter)
    ```
    """

    def build_query(self, query):
        """
        Recursively converts a dictionary into a Django Q object for complex query filtering.

        Supports:
        - Nested logical operations: AND, OR, NOT
        - All Django field lookups: __icontains, __gte, etc.
        - Field-to-field comparisons using {'F': 'other_field'}

        Example input:
        query = {
            "AND": [
                {"first_name__icontains": "alice"},
                {"age__gte": 25},
                {
                    "OR": [
                        {"NOT": {"last_name": "Smith"}},
                        {"city": "Los Angeles"},
                        {"score__gt": {"F": "high_score"}}
                    ]
                }
            ]
        }

        Output: Django Q object that can be used in filter(), exclude(), etc.
        """
        q_object = Q()

        for key, value in query.items():
            if key == "OR" and isinstance(value, list):
                or_query = Q()
                for sub_query in value:
                    or_query |= self.build_query(sub_query)
                q_object &= or_query

            elif key == "AND" and isinstance(value, list):
                and_query = Q()
                for sub_query in value:
                    and_query &= self.build_query(sub_query)
                q_object &= and_query

            elif isinstance(value, dict) and "NOT" in value:
                q_object &= ~Q(**{key: value["NOT"]})

            elif isinstance(value, dict) and "F" in value:
                q_object &= Q(**{key: F(value["F"])})

            else:
                q_object &= Q(**{key: value})

        return q_object


class Manager(Generic[T]):
    """
    A base manager class for handling common database operations in Django models.
    This class provides a standardized interface for performing CRUD (Create, Read, Update, Delete)
    operations on Django models. It includes methods for querying, creating, updating, and deleting
    model instances with support for both single and bulk operations.
    Attributes:
        model (Model): The Django model class that this manager operates on. Must be set by subclasses.
    Methods:
        get: Retrieve a single object based on query parameters.
        list: Retrieve multiple objects based on query parameters.
        create: Create one or multiple new model instances.
        update: Update existing model instances.
        upsert: Update existing instance or create new if not found.
        delete: Delete (soft or hard) model instances.
        class UserManager(Manager):
            model = User
        user_manager = UserManager()
        # Create a user
        user = user_manager.create({'name': 'John', 'email': 'john@example.com'})
        # List users
        users = user_manager.list({'is_active': True})
        # Update user
        updated_user = user_manager.update({'name': 'John Doe'}, {'id': 1})
        # Delete user
        user_manager.delete({'id': 1}, soft_delete=True)
    """

    model: Model = None
    check_is_deleted: bool = True
    query_builder = QueryBuilder()

    def __parse_query(self, query, is_deleted=False) -> QuerySet[T]:
        """
        Parse and process query parameters for database filtering.
        This method handles query parsing and filtering for database operations.
        Args:
            query (dict): The main query filter. Can be either a dictionary of field lookups.
            is_deleted (bool, default=False): Filter flag for soft-deleted records.
        Returns:
            QuerySet: The filtered queryset after applying all query conditions.
        Example:
            # Using dict query
            query = {'name': 'John', 'age__gte': 18}
            result = model_manager.__parse_query(query)
        """

        query = query or dict()

        if self.check_is_deleted:
            query["is_deleted"] = is_deleted

        objects = self.model.objects.filter(self.query_builder.build_query(query))

        return objects

    def get(self, query) -> T | None:
        """
        Get the object based on the query.
        Args:
            query (dict): The main query dictionary for filtering objects. If None, an empty dict is used.
        Returns:
            object: The first object that matches the query criteria. Returns None if no match is found.

        """
        return self.__parse_query(query=query).first()

    def get_objects_mapping(
        self,
        query: dict,
        only: list = None,
        order_by: list = None,
        mapping_by: str = "pk",
    ) -> Dict[str, T]:

        objects = self.list(query=query, only=only, order_by=order_by)

        return {getattr(obj, mapping_by): obj for obj in objects}

    def list(
        self,
        query,
        only: list = None,
        order_by: list = None,
    ) -> QuerySet[T]:
        """
        Returns a list of objects based on the provided query parameters.
        Args:
            query (dict, optional): Primary query dictionary for filtering objects. Defaults to None.
            only (list, optional): List of fields to include in the result. Defaults to None.
            order_by (list, optional): List of fields to order the result by. Defaults to None.
        Returns:
            list: A list of objects that match the query criteria after parsing.
        Example:
            model_mgr.list({'status': 'active'})
        """

        objects = self.__parse_query(query=query)

        if only:
            objects = objects.only(*only)

        if order_by:
            objects = objects.order_by(*order_by)

        return objects

    def count(self, query: dict) -> int:
        """
        Count the number of objects based on the provided query.
        Args:
            query (dict, optional): The main query dictionary for filtering objects. If None, an empty dict is used.
        Returns:
            int: The count of objects that match the query criteria.
        Example:
            model_mgr.count({'status': 'active'})
        """
        return self.__parse_query(query=query).count()

    def exists(self, query: dict) -> bool:
        """
        Check if any objects exist based on the provided query.
        Args:
            query (dict, optional): The main query dictionary for filtering objects. If None, an empty dict is used.
        Returns:
            bool: True if any objects match the query criteria, False otherwise.
        Example:
            model_mgr.exists({'status': 'active'})
        """
        return self.__parse_query(query=query).exists()

    def list_with_pagination(
        self,
        query: dict,
        only: list = None,
        order_by: list = None,
        pagination: dict = None,
    ) -> tuple[QuerySet[T], dict[str, int]]:
        objects = self.list(query=query, only=only, order_by=order_by)

        page_number: int = pagination["page"]
        page_size = pagination.get("page_size", None)

        pagination_obj = Pagination(
            page_size=page_size,
            count=objects.count(),
            current_page=page_number,
        )
        return pagination_obj.get_current_page_objs(objects), {
            "count": pagination_obj.count,
            "page_size": pagination_obj.page_size,
            "current_page": pagination_obj.current_page,
            "total_pages": pagination_obj.get_total_page_count(),
        }

    def delete(
        self,
        query=None,
        data=None,
        soft_delete=True,
        force_delete=False,
    ):
        """
        Delete records from the database based on the provided query.
        This method supports both soft deletion (marking records as deleted) and hard deletion
        (removing records from the database).
        Args:
            query (Q, optional): Django Q object containing the query conditions. Required unless force_delete is True.
            data (dict, optional): Additional data to update when performing soft delete.
            soft_delete (bool, optional): If True, marks records as deleted instead of removing them. Defaults to True.
            force_delete (bool, optional): If True, allows deletion without query parameter. Defaults to False.
        Raises:
            CommonError: If no query is provided and force_delete is False.
        Returns:
            None
        Note:
            - For soft delete, the method updates the 'is_deleted' field to True
            - For hard delete, the method permanently removes the records from database
        """

        if not query and not force_delete:
            raise CommonError(
                error.DELETE_WITHOUT_QUERY,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        objects = self.__parse_query(query=query)

        if self.check_is_deleted:
            if soft_delete:
                data = data or dict()
                data["is_deleted"] = True
                return objects.update(**data)

        return objects.delete()

    @overload
    def create(self, data: dict, many: False = False) -> T: ...

    @overload
    def create(self, data: List[dict], many: True = True) -> QuerySet[T]: ...

    def create(self, data, many=False) -> Union[T, QuerySet[T]]:
        """
        Create one or multiple instances of the model.
        Args:
            data (dict or list): The data to create the model instance(s) with.
                If many=True, should be a list of dictionaries.
                If many=False, should be a single dictionary.
            many (bool, optional): Whether to create multiple instances. Defaults to False.
        Returns:
            Model instance or list: The created model instance(s).
                If many=True, returns a list of created model instances.
                If many=False, returns a single created model instance.
        Examples:
            # Create single instance
            manager.create({'name': 'Test', 'value': 123})
            # Create multiple instances
            manager.create([
                {'name': 'Test1', 'value': 123},
                {'name': 'Test2', 'value': 456}
            ], many=True)
        """

        if many:
            return self.model.objects.bulk_create([self.model(**obj) for obj in data])

        return self.model.objects.create(**data)

    def update(self, data, query) -> T | None:
        """
        Update an existing object in the database based on the provided data and query.
        Args:
            data (dict): Dictionary containing the fields and values to update.
            query (dict): Query parameters to find the object to update.
        Returns:
            object: Updated object if successful, None if object not found.
        Example:
            >>> manager.update({'name': 'new_name'}, {'id': 1})
            <Updated object with id=1>
        """

        obj = self.get(query)
        if not obj:
            return None

        return self.__update(obj, data)

    def __update(self, obj, data: dict):
        """
        Updates an object's attributes with the provided data dictionary and saves it.
        Args:
            obj: The object to be updated
            data (dict): Dictionary containing attribute names as keys and new values to set
        Returns:
            obj: The updated and saved object
        Example:
            >>> user = User.objects.get(id=1)
            >>> data = {'name': 'John', 'age': 25}
            >>> updated_user = __update_obj(user, data)
        """

        data = data or dict()
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def upsert(self, data, query) -> T:
        """
        Update an existing object or create a new one based on query conditions.
        This function attempts to find an object using the provided query parameters. If the object
        exists, it updates it with the new data. If no object is found, it creates a new one.
        Args:
            data (dict): Dictionary containing the data to update or create the object with
            query (dict): Primary query conditions to find the object
        Returns:
            object: The updated or newly created object
        Example:
            >>> data = {'name': 'John', 'age': 30}
            >>> query = {'id': 1}
            >>> model_manager.update_or_create(data, query)
        """

        obj = self.get(query=query)
        if not obj:
            return self.create(data)
        return self.__update(obj, data)
