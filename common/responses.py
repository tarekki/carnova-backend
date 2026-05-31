"""
Standard API response envelope.

Every response follows the same shape (camelCase via DRF camel-case renderer):

Success:
    {
        "result":    "success",
        "data":      <dict | list | None>,
        "message":   "<human-readable>",
        "requestId": "<uuid>"          # injected when a RequestId is in scope
    }

Error:
    {
        "result":    "error",
        "code":      "<MACHINE_CODE>",  # see common.error_codes
        "data":      {"errors": <{field: [msgs]} | None>},
        "message":   "<human-readable>",
        "requestId": "<uuid>"
    }

Use `success_response` / `error_response` from views; the custom exception
handler (common.exceptions.custom_exception_handler) wraps errors raised by
DRF/Django automatically and adds the `code` field.

Frontends should branch on `code` (machine-readable, stable) — never on
`message` (human-readable, may be localized later).
"""
from __future__ import annotations

from typing import Any

from rest_framework import status as http_status
from rest_framework.response import Response

from . import error_codes as codes
from .request_context import get_request_id

RESULT_SUCCESS = "success"
RESULT_ERROR = "error"


def _envelope(base: dict) -> dict:
    rid = get_request_id()
    if rid:
        base["request_id"] = rid
    return base


def success_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    status_code: int = http_status.HTTP_200_OK,
) -> Response:
    return Response(
        _envelope({"result": RESULT_SUCCESS, "data": data, "message": message}),
        status=status_code,
    )


def error_response(
    message: str = "Something went wrong",
    errors: Any = None,
    code: str = codes.REQUEST_FAILED,
    status_code: int = http_status.HTTP_400_BAD_REQUEST,
) -> Response:
    """`errors` is a dict of {field: [messages]} or None for non-validation errors.

    `code` must be one of the constants in `common.error_codes` so frontend
    clients can branch on it reliably.
    """
    return Response(
        _envelope(
            {
                "result": RESULT_ERROR,
                "code": code,
                "data": {"errors": errors},
                "message": message,
            }
        ),
        status=status_code,
    )
