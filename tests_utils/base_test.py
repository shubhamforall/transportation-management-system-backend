from tests_utils.load_data import load_test_data
from tests_utils.test_client import TestClient
from django.test import TestCase


class BaseTest(TestCase):
    def setUp(self):
        load_test_data()
        self.client: TestClient = TestClient()
