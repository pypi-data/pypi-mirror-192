from __future__ import annotations

from typing import Any, Type

from httpx import Client, Response
from pydantic import BaseModel, parse_obj_as

from combadge.core.binder import BaseBoundService, Signature
from combadge.core.interfaces import CallServiceMethod, ProvidesBinder
from combadge.core.request import build_request
from combadge.core.typevars import ResponseT
from combadge.support.rest.request import Request


class HttpxBackend(ProvidesBinder):
    """
    Sync HTTPX backend for REST APIs.

    See Also:
        - https://www.python-httpx.org/
    """

    _client: Client
    __slots__ = ("_client",)

    def __init__(self, client: Client) -> None:  # noqa: D107
        self._client = client

    def __call__(self, request: Request, response_type: Type[ResponseT]) -> ResponseT:
        """Call the backend."""
        response: Response = self._client.request(
            request.method,
            request.path,
            json=request.body_dict(),
            params=request.query_params,
        )
        response.raise_for_status()
        return parse_obj_as(response_type, response.json())

    @staticmethod
    def bind_method(signature: Signature) -> CallServiceMethod[HttpxBackend]:  # noqa: D102
        def resolved_method(service: BaseBoundService[HttpxBackend], *args: Any, **kwargs: Any) -> BaseModel:
            request = build_request(Request, signature, service, args, kwargs)
            return service.backend(request, signature.return_type)

        return resolved_method  # type: ignore[return-value]

    binder = bind_method
