"""Handle server errors."""
from enum import Enum
from werkzeug import Response
from werkzeug.exceptions import InternalServerError

from source.errors.json_error import build_error_response


class ServerErrorType(Enum):
    """Error messages for server errors."""

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


def internal_server_error(error: InternalServerError) -> Response:
    """Handle 500 - Internal Server Error.

    Parameters
    ----------
    error: InternalServerError

    Returns
    -------
    Response
    """
    return build_error_response(error)
