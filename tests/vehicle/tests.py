"""
Test cases for the Vehicle API endpoints.

This module includes integration tests for the VehicleViewSet, covering CRUD operations:
- Creating a new vehicle
- Retrieving a vehicle by ID
- Listing all vehicles
- Updating a vehicle
- Deleting a vehicle
"""

from tests_utils.base_test import BaseTest


class VehicleTestCase(BaseTest):
    """
    TestCase for Vehicle API endpoints.
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.vehicle_url = "/vehicle"
        self.test_vehicle = {
            "vehicle_name": "Toyota Corolla",
            "vehicle_type": "Sedan",
            "vehicle_number": "KA01AB1234",
            "vehicle_model": "2021",
            "vehicle_color": "White",
        }

    def _create_vehicle(self, data=None):
        response = self.client.post(
            self.vehicle_url,
            data=data or self.test_vehicle,
        )
        self.assertIn(response.status_code, [200, 201], msg=response.content)
        return response.json()["data"]["vehicle_id"]

    def test_create_vehicle(self):
        vehicle_id = self._create_vehicle()

        response = self.client.get(f"{self.vehicle_url}/{vehicle_id}")
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        self.assertEqual(data["vehicle_name"], self.test_vehicle["vehicle_name"])
        self.assertEqual(data["vehicle_type"], self.test_vehicle["vehicle_type"])
        self.assertEqual(data["vehicle_number"], self.test_vehicle["vehicle_number"])
        self.assertEqual(data["vehicle_model"], self.test_vehicle["vehicle_model"])
        self.assertEqual(data["vehicle_color"], self.test_vehicle["vehicle_color"])
        self.assertEqual(data["vehicle_id"], vehicle_id)

    def test_create_vehicle_with_existing_number(self):
        self._create_vehicle()
        response = self.client.post(self.vehicle_url, data=self.test_vehicle)
        self.assertEqual(response.status_code, 400, msg=response.content)

        errors = response.json()["errors"]
        error_dict = {err["field"]: (err["code"], err["message"]) for err in errors}
        self.assertIn("vehicle_number", error_dict)
        self.assertEqual(error_dict["vehicle_number"][0], "DUPLICATE_ENTRY")

    def test_get_vehicle_by_id(self):
        vehicle_id = self._create_vehicle()
        response = self.client.get(f"{self.vehicle_url}/{vehicle_id}")

        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        self.assertEqual(data["vehicle_id"], vehicle_id)
        self.assertEqual(data["vehicle_name"], self.test_vehicle["vehicle_name"])
        self.assertEqual(data["vehicle_type"], self.test_vehicle["vehicle_type"])
        self.assertEqual(data["vehicle_number"], self.test_vehicle["vehicle_number"])
        self.assertEqual(data["vehicle_model"], self.test_vehicle["vehicle_model"])
        self.assertEqual(data["vehicle_color"], self.test_vehicle["vehicle_color"])

    def test_get_vehicle_with_invalid_id(self):
        response = self.client.get(
            f"{self.vehicle_url}/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")

    def test_list_vehicles(self):
        self._create_vehicle()
        response = self.client.get(f"{self.vehicle_url}")
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        vehicle_list = data["list"]
        pagination = data["pagination"]

        self.assertEqual(len(vehicle_list), 1)

        vehicle = vehicle_list[0]
        self.assertEqual(vehicle["vehicle_name"], self.test_vehicle["vehicle_name"])
        self.assertEqual(vehicle["vehicle_type"], self.test_vehicle["vehicle_type"])
        self.assertEqual(vehicle["vehicle_number"], self.test_vehicle["vehicle_number"])
        self.assertEqual(vehicle["vehicle_model"], self.test_vehicle["vehicle_model"])
        self.assertEqual(vehicle["vehicle_color"], self.test_vehicle["vehicle_color"])
        self.assertTrue("vehicle_id" in vehicle)

        self.assertEqual(pagination["count"], 1)
        self.assertEqual(pagination["page_size"], 10)
        self.assertEqual(pagination["current_page"], 1)
        self.assertEqual(pagination["total_pages"], 1)

    def test_update_vehicle(self):
        vehicle_id = self._create_vehicle()
        update_data = {
            "vehicle_name": "Honda City",
            "vehicle_type": "Sedan",
            "vehicle_number": "KA01XY9876",
            "vehicle_model": "2022",
            "vehicle_color": "Black",
        }

        response = self.client.put(f"{self.vehicle_url}/{vehicle_id}", data=update_data)
        self.assertEqual(response.status_code, 200, msg=response.content)

        data = response.json()["data"]
        self.assertEqual(data["vehicle_id"], vehicle_id)
        self.assertEqual(data["vehicle_name"], update_data["vehicle_name"])
        self.assertEqual(data["vehicle_type"], update_data["vehicle_type"])
        self.assertEqual(data["vehicle_number"], update_data["vehicle_number"])
        self.assertEqual(data["vehicle_model"], update_data["vehicle_model"])
        self.assertEqual(data["vehicle_color"], update_data["vehicle_color"])

    def test_update_vehicle_with_invalid_id(self):
        update_data = {
            "vehicle_name": "Fake Car",
            "vehicle_type": "Hatchback",
            "vehicle_number": "INVALID1234",
            "vehicle_model": "1999",
            "vehicle_color": "Invisible",
        }

        response = self.client.put(
            f"{self.vehicle_url}/00000000-0000-0000-0000-000000000000", data=update_data
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")

    def test_delete_vehicle(self):
        vehicle_id = self._create_vehicle()
        response = self.client.delete(f"{self.vehicle_url}/{vehicle_id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_vehicle_with_invalid_id(self):
        response = self.client.delete(
            f"{self.vehicle_url}/00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 404)

        errors = response.json()["errors"]
        self.assertEqual(errors["code"], "NO_DATA_FOUND")
        self.assertEqual(errors["message"], "No Data Found.")
