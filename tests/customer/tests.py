"""
Test cases for the Customer API endpoints.

This module includes integration tests for the CustomerViewSet, covering CRUD operations:
- Creating a new customer
- Retrieving a customer by ID
- Listing all customers
- Updating a customer
- Deleting a customer
"""

from tests_utils.base_test import BaseTest


class CustomerTestCase(BaseTest):
    """
    TestCase for Customer API endpoints.
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.customer_url = "/customer"
        self.test_customer = {
            "customer_type": "BUSINESS",
            "company_name": "test",
            "first_name": "Test",
            "last_name": "TestName",
            "mobile_number": "9876543210",
            "email": "test@example.com",
            "address": "1234 MG Road, Pune, Maharashtra",
        }

    def _create_customer(self, data=None):
        response = self.client.post(
            self.customer_url,
            data=data or self.test_customer,
        )

        self.assertIn(response.status_code, [200, 201], msg=response.content)
        return response.json()["data"]["customer_id"]

    def test_create_customer(self):
        customer_id = self._create_customer()

        response = self.client.get(f"{self.customer_url}/{customer_id}")
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        self.assertEqual(data["email"], self.test_customer["email"])
        self.assertEqual(data["first_name"], self.test_customer["first_name"])
        self.assertEqual(data["last_name"], self.test_customer["last_name"])
        self.assertEqual(data["mobile_number"], self.test_customer["mobile_number"])
        self.assertEqual(data["company_name"], self.test_customer["company_name"])
        self.assertEqual(data["address"], self.test_customer["address"])
        self.assertEqual(data["customer_type"], self.test_customer["customer_type"])
        self.assertEqual(data["customer_id"], customer_id)

    def test_create_customer_with_existing_email(self):
        self._create_customer()

        response = self.client.post(self.customer_url, data=self.test_customer)
        self.assertEqual(response.status_code, 400, msg=response.content)

        errors = response.json()["errors"]
        error_dict = {err["field"]: (err["code"], err["message"]) for err in errors}

        self.assertIn("email", error_dict)
        self.assertEqual(error_dict["email"][0], "DUPLICATE_ENTRY")

    def test_get_customer_by_id(self):
        customer_id = self._create_customer()
        response = self.client.get(f"{self.customer_url}/{customer_id}")

        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]

        self.assertEqual(data["customer_id"], customer_id)
        self.assertEqual(data["customer_type"], self.test_customer["customer_type"])
        self.assertEqual(data["company_name"], self.test_customer["company_name"])
        self.assertEqual(data["first_name"], self.test_customer["first_name"])
        self.assertEqual(data["last_name"], self.test_customer["last_name"])
        self.assertEqual(data["mobile_number"], self.test_customer["mobile_number"])
        self.assertEqual(data["email"], self.test_customer["email"])
        self.assertEqual(data["address"], self.test_customer["address"])

    def test_get_customer_with_invalid_id(self):
        response = self.client.get(
            f"{self.customer_url}/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")

    def test_list_customers(self):
        self._create_customer()

        response = self.client.get(f"{self.customer_url}")

        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        customer_list = data["list"]
        pagination = data["pagination"]

        self.assertEqual(len(customer_list), 1)

        customer = customer_list[0]

        self.assertEqual(customer["customer_type"], self.test_customer["customer_type"])
        self.assertEqual(customer["company_name"], self.test_customer["company_name"])
        self.assertEqual(customer["first_name"], self.test_customer["first_name"])
        self.assertEqual(customer["last_name"], self.test_customer["last_name"])
        self.assertEqual(customer["mobile_number"], self.test_customer["mobile_number"])
        self.assertEqual(customer["email"], self.test_customer["email"])
        self.assertEqual(customer["address"], self.test_customer["address"])
        self.assertTrue("customer_id" in customer)

        self.assertEqual(pagination["count"], 1)
        self.assertEqual(pagination["page_size"], 10)
        self.assertEqual(pagination["current_page"], 1)
        self.assertEqual(pagination["total_pages"], 1)

    def test_update_customer(self):
        customer_id = self._create_customer()
        update_data = {
            "customer_type": "BUSINESS",
            "company_name": "NewCo",
            "first_name": "Jane",
            "last_name": "Doe",
            "mobile_number": "1122334455",
            "email": "jane.doe@example.com",
            "address": "789 New Street, Mumbai",
        }

        response = self.client.put(
            f"{self.customer_url}/{customer_id}",
            data=update_data,
        )
        self.assertEqual(response.status_code, 200, msg=response.content)
        response_data = response.json()["data"]

        self.assertEqual(response_data["customer_id"], customer_id)
        self.assertEqual(response_data["customer_type"], update_data["customer_type"])
        self.assertEqual(response_data["company_name"], update_data["company_name"])
        self.assertEqual(response_data["first_name"], update_data["first_name"])
        self.assertEqual(response_data["last_name"], update_data["last_name"])
        self.assertEqual(
            response_data["full_name"],
            f"{update_data['first_name']} {update_data['last_name']}",
        )
        self.assertEqual(response_data["mobile_number"], update_data["mobile_number"])
        self.assertEqual(response_data["email"], update_data["email"])
        self.assertEqual(response_data["address"], update_data["address"])

    def test_update_customer_with_invalid_id(self):
        update_data = {
            "customer_type": "INDIVIDUAL",
            "company_name": "GhostCorp",
            "first_name": "Ghost",
            "last_name": "User",
            "mobile_number": "0000000000",
            "email": "ghost@example.com",
            "address": "Unknown",
        }

        response = self.client.put(
            f"{self.customer_url}/00000000-0000-0000-0000-000000000000",
            data=update_data,
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")

    def test_delete_customer(self):
        customer_id = self._create_customer()
        response = self.client.delete(f"{self.customer_url}/{customer_id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_customer_with_invalid_id(self):
        response = self.client.delete(
            f"{self.customer_url}/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")
