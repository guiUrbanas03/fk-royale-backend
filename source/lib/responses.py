"""Module to handle http responses utilities."""
from flask import jsonify


class BaseResponse:
    """Base http response."""

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code

    def json(self):
        return (
            jsonify(
                {
                    "message": self.message,
                }
            ),
            self.status_code,
        )


class DataResponse(BaseResponse):
    """Response to send data."""

    def __init__(self, message: str, status_code: int = 200, data: dict = {}) -> None:
        super().__init__(message, status_code)
        self.data = data

    def json(self):
        """Return json data response."""
        return (
            jsonify(
                {
                    "message": self.message,
                    **self.data,
                }
            ),
            self.status_code,
        )
