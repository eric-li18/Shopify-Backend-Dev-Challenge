from api import util


class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InvalidRequestException(APIException):
    code = 422
    description = "Invalid request."


class ResourceNotFoundException(APIException):
    code = 404
    description = "Resource not found."


def handle_exception(e):
    """ Handle all raised exceptions with common response structure. """

    return util.response({"error": f"{e.description} {e.message}"}, e.code)


def handle_server_error(e):
    """Handle all responses resulting from internal server error
    (status code is 500)."""
    return util.response(
        {
            "error": "Internal server error. Please contact support if behaviour is unexpected."
        },
        500,
    )
