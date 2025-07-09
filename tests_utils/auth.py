from django.test import Client


def get_auth_token():
    client = Client()

    response = client.post(
        "/api/auth/login",
        data={"username": "test.user@example.com", "password": "TestUser@123"},
        content_type="application/json",
    )

    return response.json()["data"]["token"]
