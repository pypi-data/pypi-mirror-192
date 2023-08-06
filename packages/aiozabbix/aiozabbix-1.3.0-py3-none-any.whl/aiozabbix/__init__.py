"""aiozabbix - Asynchronous Zabbix API Python Library."""
#
# Original Ruby Library is Copyright (C) 2009 Andrew Nelson nelsonab(at)red-tux(dot)net
# Original Python Library is Copyright (C) 2009 Brett Lentz brett.lentz(at)gmail(dot)com
#
# Copyright (C) 2011-2018 Luke Cyca me(at)lukecyca(dot)com
# Copyright (C) 2018-2021 Modio AB
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

from urllib.parse import urlparse
from typing import Optional, Dict, Any, Callable, Awaitable
import aiohttp
from aiohttp.client_exceptions import ContentTypeError
from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.util.types import Attributes

tracer = trace.get_tracer(__name__)

__all__ = [
    "ZabbixAPIException",
    "ZabbixAPI",
    "ZabbixAPIObjectClass",
]

# Type alias for Json-style data both to and from server.
JsonType = Any


class ZabbixAPIException(Exception):
    """Some kind of API exception."""


class ZabbixAPI:
    """Class representing the zabbix API."""

    # pylint: disable=too-many-instance-attributes

    DEFAULT_HEADERS = {"Content-Type": "application/json-rpc"}

    LOGIN_METHODS = ("user.login", "user.authenticate")
    UNAUTHENTICATED_METHODS = (
        "apiinfo.version",
        "user.checkAuthentication",
    ) + LOGIN_METHODS
    AUTH_ERROR_FRAGMENTS = (
        "authori",  # From CLocalApiClient::authenticate
        "permission",  # From CUser::checkAuthentication
        "re-login",  # From many places
    )

    def __init__(
        self,
        server: str = "http://localhost/zabbix",
        *,
        timeout: Optional[float] = None,
        client_session: Optional[aiohttp.ClientSession] = None,
        headers: Optional[dict[str, str]] = None,
    ):
        """Set up the zabbix api."""
        self.url = server + "/api_jsonrpc.php"

        if client_session is None:
            self.client_session = aiohttp.ClientSession()
        else:
            self.client_session = client_session

        self.timeout = timeout

        self.auth = ""
        self.shared_state = {"next_jsonrpc_id": 0}
        self.do_login: Optional[Callable[..., Awaitable[None]]] = None

        self.headers = self.DEFAULT_HEADERS.copy()
        if headers is not None:
            self.headers.update(headers)

    def with_headers(self, headers: Dict[str, str]) -> "ZabbixAPI":
        """Make a copy of the ZabbixAPI object which sets extra HTTP headers."""
        result = ZabbixAPI.__new__(ZabbixAPI)
        result.url = self.url
        result.client_session = self.client_session
        result.timeout = self.timeout
        result.auth = self.auth
        result.shared_state = self.shared_state
        result.do_login = self.do_login
        result.headers = self.headers.copy()
        result.headers.update(headers)
        return result

    async def do_request(
        self, method: str, params: Optional[JsonType] = None, auth_retries: int = 1
    ) -> JsonType:
        """Perform a request for the method with params."""
        rpc_id = self.shared_state["next_jsonrpc_id"]
        request_json = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": rpc_id,
        }
        attributes: Attributes = {
            SpanAttributes.NET_PEER_NAME: str(urlparse(self.url).hostname),
            SpanAttributes.RPC_SYSTEM: "jsonrpc",
            SpanAttributes.RPC_JSONRPC_VERSION: 2.0,
            SpanAttributes.RPC_METHOD: method,
            SpanAttributes.RPC_JSONRPC_REQUEST_ID: rpc_id,
        }

        with tracer.start_as_current_span("aiohttp.do_request", attributes=attributes):
            self.shared_state["next_jsonrpc_id"] += 1

            if method in self.UNAUTHENTICATED_METHODS:
                return await self.post_request(request_json)

            request_json["auth"] = self.auth

            try:
                return await self.post_request(request_json)
            except ZabbixAPIException as exc:
                if auth_retries > 0 and self.do_login and self.is_auth_error(exc):
                    await self.do_login(self)
                    return await self.do_request(
                        method, params, auth_retries=auth_retries - 1
                    )
                raise

    async def post_request(self, request_json: JsonType) -> JsonType:
        """Post a json request to the server."""
        response = await self.client_session.post(
            self.url, json=request_json, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()

        try:
            response_json = await response.json()
        except (ValueError, ContentTypeError) as exc:
            text = await response.text()
            raise ZabbixAPIException(f"Unable to parse JSON: {text}") from exc

        if "error" in response_json:
            # Workaround for ZBX-9340, some errors don't contain 'data':
            if "data" not in response_json["error"]:
                response_json["error"]["data"] = "ZBX-9340: No data"

            err = response_json["error"]
            code = err["code"]
            msg = f"Error {code}: {err['message']}, {err['data']}"
            attributes = {
                SpanAttributes.RPC_JSONRPC_ERROR_CODE: code,
                SpanAttributes.RPC_JSONRPC_ERROR_MESSAGE: msg,
            }
            trace.get_current_span().set_attributes(attributes)
            raise ZabbixAPIException(msg, code)

        return response_json

    @classmethod
    def method_needs_auth(cls, method: str) -> bool:
        """Check if a method needs authentication."""
        return method not in cls.UNAUTHENTICATED_METHODS

    @classmethod
    def is_auth_error(cls, exc: Exception) -> bool:
        """Determine if an error is an authorization error.

        This makes a best effort attempt to recognize authentication
        or authorization errors. Unfortunately the general JSON-RPC
        error code -32602 (Invalid params) and the generic Zabbix
        error -32500 are used for these types of errors.

        The error messages may also be localized which could make this
        check fail.
        """

        err = str(exc).lower()
        return any(x in err for x in cls.AUTH_ERROR_FRAGMENTS)

    async def login(self, user: str = "", password: str = "") -> None:
        """Wrapper to log-in ot the remote server."""

        async def do_login(self: "ZabbixAPI") -> None:
            # Provide the self argument explicitly instead of taking
            # it from the surrounding closure. The self from the
            # closure will not be correct if this do_login is called
            # from a copy of the ZabbixAPI object created by the
            # with_headers method.

            # We create a new instance to not set the "auth" cookie to
            # something invalid while we are logging in.
            sub = self.with_headers({})
            sub.auth = ""
            self.auth = await sub.user.login(user=user, password=password)

        self.do_login = do_login
        assert self.do_login is not None
        await self.do_login(self)

    async def confimport(
        self, confformat: str = "", source: str = "", rules: str = ""
    ) -> JsonType:
        """Compatibility function."""
        return await self.configuration.import_(
            format=confformat, source=source, rules=rules
        )

    def __getattr__(self, attr: str) -> "ZabbixAPIObjectClass":
        return ZabbixAPIObjectClass(name=attr, parent=self)


class ZabbixAPIObjectClass:
    """Method wrapper on the zabbix api."""

    # pylint: disable=too-few-public-methods

    def __init__(self, *, name: str, parent: ZabbixAPI) -> None:
        """Class instantiation for the method wrapper."""
        self.name = name
        self.parent = parent

    def __getattr__(self, attr: str) -> Callable[..., JsonType]:
        """Used to resolve methods dynamically."""
        if attr == "import_":
            attr = "import"
        method_name = f"{self.name}.{attr}"

        async def method(*args: JsonType, **kwargs: JsonType) -> JsonType:
            """JSON-rpc method wrapper for ZabbixApi."""
            if args and kwargs:
                raise TypeError(
                    "Method may be called with positional arguments or "
                    "keyword arguments, but not both at the same time"
                )
            response = await self.parent.do_request(method_name, args or kwargs)
            result = response["result"]
            return result

        return method
