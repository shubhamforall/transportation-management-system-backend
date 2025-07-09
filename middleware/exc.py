"""
Middleware to handle exceptions globally in Django Rest Framework.
"""

# Standard Library
import logging
import traceback

# Third Party Library
from rest_framework import status
from django.utils.deprecation import MiddlewareMixin

# Local Imports
from utils.messages import error
from utils.exceptions import codes
from utils.logger.logger import log_msg
from utils.response import generate_response
from utils.ser_val_err_format import format_serializer_errors
from utils.exceptions import (
    SettingKeyError,
    CommonError,
    NoDataFoundError,
    ValidationError,
    BadRequestError,
    PermissionDenied,
)

from authentication.exception import UnauthorizedException, WrongCredentialsException


class DRFExceptionMiddleware(MiddlewareMixin):
    """
    Middleware to handle exceptions globally in Django Rest Framework.
    """

    def return_500(self):
        """
        This method returns a 500 response
        """

        return generate_response(
            errors={
                "code": codes.UNKNOWN_ERROR,
                "message": error.INTERNAL_SERVER_ERROR,
            },
            create_json_response=True,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def log_exception(self, exception):
        log_msg(
            logging.ERROR,
            traceback.format_exc(),
            ref_data=getattr(exception, "ref_data", None),
        )

    def process_exception(self, _, exception):
        """
        This method catches exceptions and returns a JSON response.
        """

        if isinstance(exception, ValidationError):
            return generate_response(
                create_json_response=True,
                status_code=exception.status_code,
                errors=format_serializer_errors(exception.message),
            )

        if isinstance(exception, (NoDataFoundError, BadRequestError, PermissionDenied)):
            return generate_response(
                create_json_response=True,
                status_code=exception.status_code,
                errors={"message": exception.message, "code": exception.code},
            )

        if isinstance(exception, (SettingKeyError, CommonError)):
            self.log_exception(exception)
            return self.return_500()

        if isinstance(exception, (UnauthorizedException, WrongCredentialsException)):
            return generate_response(
                create_json_response=True,
                status_code=exception.status_code,
                errors={"message": exception.message, "code": exception.code},
            )

        self.log_exception(exception)
        return self.return_500()
