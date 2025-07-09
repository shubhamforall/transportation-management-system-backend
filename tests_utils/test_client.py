from django.test import Client
from tests_utils.auth import get_auth_token
from utils import functions


class TestClient:
    def __init__(self, set_default_token: bool = True, token_type: str = "Bearer"):
        self.client = Client()
        self.http_host = "localhost"
        self.token_type = token_type
        self.token = None

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if set_default_token:
            token = get_auth_token()
            self.set_auth_header(token)

    def set_auth_header(self, token: str):
        self.token = token
        self.client.defaults["HTTP_AUTHORIZATION"] = f"{self.token_type} {token}"

    def _prepare_url(self, endpoint: str) -> str:
        return functions.create_end_point(endpoint)

    def post(self, endpoint: str, data=None, **kwargs):
        url = self._prepare_url(endpoint)
        return self.client.post(
            url,
            data=data,
            **kwargs,
        )

    def get(self, endpoint: str, **kwargs):
        url = self._prepare_url(endpoint)
        return self.client.get(
            url,
            **kwargs,
        )

    def put(self, endpoint: str, data=None, **kwargs):
        url = self._prepare_url(endpoint)
        return self.client.put(
            url,
            content_type=self.headers["Content-Type"],
            data=data,
            **kwargs,
        )

    def patch(self, endpoint: str, data=None, **kwargs):
        url = self._prepare_url(endpoint)
        return self.client.patch(
            url,
            content_type=self.headers["Content-Type"],
            data=data,
            **kwargs,
        )

    def delete(self, endpoint: str, **kwargs):
        url = self._prepare_url(endpoint)
        return self.client.delete(
            url,
            **kwargs,
        )
