"""Module to handle json errors."""
import json
import logging
from enum import Enum
from flask import jsonify
from typing import Tuple, Union


class CauseTypeError(Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DATA_VIOLATION_ERROR = "DATA_VIOLATION"
    TOKEN_ERROR = "TOKEN_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"


def error_dict(code: int, name: str, cause: Union[str, dict]) -> dict:
    """Base error dict.

    Parameters
    ----------
    code: int
    name: str
    cause: Union[str, dict]

    Returns
    -------
    dict
    """
    return {
        "code": code,
        "name": name,
        "cause": cause,
    }


def build_error_response(error):
    """Build json error response.

    Parameters
    ----------
    error
    type

    Returns
    -------
    Response
    """
    try:
        logging.error(str(error))
        response = error.get_response()
        response.content_type = "application/json"

        response.data = json.dumps(error_dict(error.code, error.name, error.description))
    except AttributeError:
        return str(error), 500

    return response


def jwt_error(cause_data: str) -> Tuple[str, int]:
    """Base JWT error dict response.

    Parameters
    ----------
    cause: str

    Return
    ------
    Tuple[str, int]
    """
    return (
        jsonify(
            error_dict(
                401, "Unauthorized", {"type": CauseTypeError.TOKEN_ERROR.value, "data": cause_data}
            )
        ),
        401,
    )
