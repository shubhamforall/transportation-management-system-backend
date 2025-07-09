"""
Common error message constants used throughout platform.
"""

# ERROR
BAD_REQUEST: str = "Invalid data."
ALREADY_EXIST: str = "Already Exist."
NO_DATA_FOUND: str = "No Data Found."
WRONG_CREDENTIALS: str = "Wrong Credentials."
PERMISSION_DENIED: str = "Permission Denied."
ALREADY_IN_USED: str = "The record is being used."
UNAUTHORIZED_ACCESS: str = "Unauthorized Access."
DATA_NOT_PROVIDED: str = "Please provide the data."
INTERNAL_SERVER_ERROR: str = "Internal Server Error."
DELETE_WITHOUT_QUERY: str = "Provide the Query To delete the records."
PRINT_FUNCTION_IS_DISABLE: str = (
    "print() function is disabled please remove the use of it instead use the [log_msg]. "
    "Change the DISABLE_PRINT:True in the config file to False to enable the print function. "
)
