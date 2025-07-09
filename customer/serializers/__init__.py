from customer.serializers.customer import CustomerSerializer
from customer.serializers.swagger import (
    CustomerResponseSerializer,
    CustomerListResponseSerializer,
    Customer_create_success_example,
    Customer_getById_success_example,
    Customer_list_success_example,
    Customer_update_success_example,
    Customer_delete_success_example,
)

__all__ = [
    "CustomerSerializer",
    "CustomerResponseSerializer",
    "CustomerListResponseSerializer",
    "Customer_create_success_example",
    "Customer_getById_success_example",
    "Customer_list_success_example",
    "Customer_update_success_example",
    "Customer_delete_success_example",
]
