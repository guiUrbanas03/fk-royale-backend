"""Handle client errors."""
from enum import Enum
from werkzeug import Response
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized, UnprocessableEntity


class ClientErrorType(Enum):
    """Error messages for client errors."""

    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    NOT_FOUND = "NOT_FOUND"
    UNPROCESSABLE_ENTITY = "UNPROCESSABE_ENTITY"
    CONFLICT = "CONFLICT"


def bad_request(error: BadRequest) -> Response:
    """Handle 400 - Bad Request error.

    Parameters
    ----------
    error: BadRequest

    Returns
    -------
    Response
    """
    return error


def unauthorized(error: Unauthorized) -> Response:
    """Handle 401 - Unauthorized error.

    Parameters
    ----------
    error: Unauthorized

    Returns
    -------
    Response
    """
    return error


def not_found(error: NotFound) -> Response:
    """Handle 404 - Not Found error.

    Parameters
    ----------
    error: NotFound

    Returns
    -------
    Response
    """
    return error


def conflict(error: Conflict) -> Response:
    """Handle 409 - Conflict error.

    Parameters
    ----------
    error: Conflict

    Returns
    -------
    Response
    """
    return error


def unprocessable_entity(error: UnprocessableEntity) -> Response:
    """Handle 422 - Unprocessable Entity error.

    Parameters
    ----------
    error: UnprocessableEntity

    Returns
    -------
    Response
    """
    return error
