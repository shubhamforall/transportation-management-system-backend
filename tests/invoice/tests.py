"""
Test cases for the Invoice API endpoints.

This module includes integration tests for the InvoiceViewSet, covering CRUD operations:
- Creating a new invoice
- Retrieving an invoice by ID
- Listing all invoices
- Updating an invoice
- Deleting an invoice
"""

from tests_utils.base_test import BaseTest


class InvoiceTestCase(BaseTest):
    """
    TestCase for Invoice API endpoints.
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.invoice_url = "/invoice"
        self.customer_url = "/customer"
        self.vehicle_url = "/vehicle"

        self.test_customer = {
            "customer_type": "BUSINESS",
            "company_name": "test",
            "first_name": "Test",
            "last_name": "TestName",
            "mobile_number": "9876543210",
            "email": "test@example.com",
            "address": "1234 MG Road, Pune, Maharashtra",
        }

        self.test_vehicle = {
            "vehicle_name": "Toyota Corolla",
            "vehicle_type": "Sedan",
            "vehicle_number": "KA01AB1234",
            "vehicle_model": "2021",
            "vehicle_color": "White",
        }

    def _create_customer(self):
        response = self.client.post(self.customer_url, data=self.test_customer)
        self.assertIn(response.status_code, [200, 201], msg=response.content)
        return response.json()["data"]["customer_id"]

    def _create_vehicle(self):
        response = self.client.post(self.vehicle_url, data=self.test_vehicle)
        self.assertIn(response.status_code, [200, 201], msg=response.content)
        return response.json()["data"]["vehicle_id"]

    def _create_invoice(self, data=None):
        customer_id = self._create_customer()
        vehicle_id = self._create_vehicle()

        invoice_data = data or {
            "customer_id": customer_id,
            "vehicle_id": vehicle_id,
            "date": "2024-05-15",
            "loading_address": "Warehouse A, Industrial Area",
            "delivery_address": "Retail Store B, City Center",
            "weight": 12250.50,
            "rate": 8.75,
            "total": 10941.88,
            "status": "PAID",
        }

        response = self.client.post(self.invoice_url, data=invoice_data)
        self.assertIn(response.status_code, [200, 201], msg=response.content)
        return response.json()["data"]["invoice_id"], invoice_data

    def test_create_invoice(self):
        invoice_id, invoice_data = self._create_invoice()

        response = self.client.get(f"{self.invoice_url}/{invoice_id}")
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        self.assertEqual(data["customer"], invoice_data["customer_id"])
        self.assertEqual(data["vehicle"], invoice_data["vehicle_id"])
        self.assertEqual(data["date"], invoice_data["date"])
        self.assertEqual(data["loading_address"], invoice_data["loading_address"])
        self.assertEqual(data["delivery_address"], invoice_data["delivery_address"])
        self.assertEqual(data["weight"], invoice_data["weight"])
        self.assertEqual(data["rate"], invoice_data["rate"])
        self.assertEqual(data["total"], invoice_data["total"])
        self.assertEqual(data["status"], invoice_data["status"])

    def test_get_invoice_with_invalid_id(self):
        response = self.client.get(
            f"{self.invoice_url}/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")

    def test_list_invoices(self):
        self._create_invoice()

        response = self.client.get(self.invoice_url)
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        invoice_list = data["list"]
        pagination = data["pagination"]

        self.assertEqual(len(invoice_list), 1)
        invoice = invoice_list[0]

        self.assertTrue("invoice_id" in invoice)
        self.assertEqual(pagination["count"], 1)
        self.assertEqual(pagination["page_size"], 10)
        self.assertEqual(pagination["current_page"], 1)
        self.assertEqual(pagination["total_pages"], 1)

    def test_update_invoice(self):
        invoice_id, invoice_data = self._create_invoice()

        updated_data = {
            "customer_id": invoice_data["customer_id"],
            "vehicle_id": invoice_data["vehicle_id"],
            "date": "2024-06-01",
            "loading_address": "Updated Warehouse",
            "delivery_address": "Updated Retail Store",
            "weight": 15000,
            "rate": 9.50,
            "total": 14250.00,
            "status": "UNPAID",
        }

        response = self.client.put(
            f"{self.invoice_url}/{invoice_id}", data=updated_data
        )
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        self.assertEqual(data["date"], updated_data["date"])
        self.assertEqual(data["loading_address"], updated_data["loading_address"])
        self.assertEqual(data["delivery_address"], updated_data["delivery_address"])
        self.assertEqual(data["weight"], updated_data["weight"])
        self.assertEqual(data["rate"], updated_data["rate"])
        self.assertEqual(data["total"], updated_data["total"])
        self.assertEqual(data["status"], updated_data["status"])

    def test_update_invoice_with_invalid_id(self):
        fake_id = "00000000-0000-0000-0000-000000000000"
        update_data = {
            "customer_id": "some-id",
            "vehicle_id": "another-id",
            "date": "2024-06-01",
            "loading_address": "Invalid Warehouse",
            "delivery_address": "Invalid Destination",
            "weight": 10000,
            "rate": 7.50,
            "total": 7500,
            "status": "PENDING",
        }

        response = self.client.put(f"{self.invoice_url}/{fake_id}", data=update_data)
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")

    def test_delete_invoice(self):
        invoice_id, _ = self._create_invoice()
        response = self.client.delete(f"{self.invoice_url}/{invoice_id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_invoice_with_invalid_id(self):
        response = self.client.delete(
            f"{self.invoice_url}/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")
