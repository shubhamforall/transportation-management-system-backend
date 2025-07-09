"""
This file contains the common functions which are used in the project.
"""

# Standard Library Imports
import sys
import uuid

# Third Party Imports
from django.utils import timezone

# Local Imports
from utils import constants, settings


def get_uuid():
    """
    It's used to generate the UUID.
    """
    return str(uuid.uuid4())


def is_env(env: str):
    """
    Check if the current env is given env or not.
    """
    return env == c_env()


def is_local():
    """
    return true of the current env is LOCAL.
    """
    return is_env(constants.LOCAL)


def is_dev():
    """
    return true of the current env is DEV.
    """
    return is_env(constants.DEV)


def is_qa():
    """
    return true of the current env is QA.
    """
    return is_env(constants.QA)


def is_uat():
    """
    return true of the current env is UAT.
    """
    return is_env(constants.UAT)


def is_prod():
    """
    return true of the current env is PROD.
    """
    return is_env(constants.PROD)


# current env
def c_env():
    """
    Return the env which app is running.
    """
    return settings.read("ENV").upper()


def is_linux():
    """
    Check if the app is running on linux or not.
    """
    return "linux" in sys.platform


def get_current_datetime():
    """
    Return the current datetime. With system timezone.
    """
    return timezone.now()


def create_end_point(end_point: str):
    """
    Creates a complete endpoint URL by appending the given endpoint path to the base path.
    """

    if not end_point.startswith("/"):
        end_point = f"/{end_point}"

    return constants.BASE_PATH + end_point


def is_management_command():
    """
    Check if the current command is a management command.
    """
    return any(
        cmd in sys.argv
        for cmd in [
            "makemigrations",
            "migrate",
            "collectstatic",
            "test",
            "createsuperuser",
            "check",
            "inspectdb",
            "ver"
        ]
    )


def get_client_info(request):
    """
    Get the real client IP address, supporting proxies and Docker.
    Get the user agent from the request headers.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Can contain multiple IPs: client, proxy1, proxy2...
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    user_agent = request.META.get("HTTP_USER_AGENT", "")

    return {"client_ip": ip, "client_user_agent": user_agent}
