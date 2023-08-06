"""Testcases for aiozabbix."""
from typing import List
from dataclasses import dataclass

from aiohttp import web
import pytest

from aiozabbix import ZabbixAPI, ZabbixAPIException


async def mock_jsonrpc(request):
    """Mock RPC server that mostly replies with nonsense json."""
    request.app["state"].requests.append(request)

    request_json = await request.json()
    assert request_json["jsonrpc"] == "2.0"
    assert "params" in request_json
    assert "id" in request_json

    result = None

    method = request_json["method"]
    if ZabbixAPI.method_needs_auth(method):
        if not request.app["state"].logged_in:
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": "Invalid params.",
                        "data": "Not authorised.",
                    },
                    "id": request_json["id"],
                }
            )

    if method == "user.login":
        request.app["state"].logged_in = True
        result = f"mock auth token {request.app['state'].next_auth_token}"
        request.app["state"].next_auth_token += 1

    if result is None:
        result = f"mock response for {method}"

    return web.json_response(
        {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_json["id"],
        }
    )


@dataclass
class AppState:
    """State for the test app."""

    requests: List
    logged_in: bool
    next_auth_token: int


@pytest.fixture(name="mock_server_app")
def fixture_mock_server_app():
    """Web server fixture."""
    app = web.Application()
    app.router.add_post("/api_jsonrpc.php", mock_jsonrpc)
    app["state"] = AppState(requests=[], logged_in=False, next_auth_token=1)
    return app


@pytest.fixture(name="client_session")
async def fixture_client_session(aiohttp_client, mock_server_app):
    """Client session fixture."""
    return await aiohttp_client(mock_server_app)


@pytest.fixture(name="zapi")
async def fixture_zapi(client_session, mock_server_app):
    """Zabbix API fixture."""
    assert mock_server_app
    return ZabbixAPI(server="", client_session=client_session)


async def test_unauthenticated_calls_should_work(mock_server_app, zapi):
    """Test that unauth calls work."""
    await zapi.apiinfo.version()

    requests = [await r.json() for r in mock_server_app["state"].requests]
    assert len(requests) == 1
    assert requests[0]["method"] == "apiinfo.version"


async def test_authenticated_mock_calls_should_fail_before_login(zapi):
    """Login should be required."""
    with pytest.raises(ZabbixAPIException):
        await zapi.hostgroup.get()


async def test_login_should_work(mock_server_app, zapi):
    """Login should work."""
    await zapi.login(user="Admin", password="zabbix")

    requests = [await r.json() for r in mock_server_app["state"].requests]
    assert len(requests) == 1
    assert requests[0]["method"] == "user.login"
    assert requests[0]["params"] == {"user": "Admin", "password": "zabbix"}


async def test_authenticated_mock_calls_should_succeed_after_login(zapi):
    """Login should work."""
    await zapi.login(user="Admin", password="zabbix")
    response = await zapi.hostgroup.get()
    assert "error" not in response


async def test_auth_token_should_be_sent(mock_server_app, zapi):
    """Login auth token should be passed on."""
    await zapi.login(user="Admin", password="zabbix")
    await zapi.hostgroup.get()

    requests = [await r.json() for r in mock_server_app["state"].requests]

    assert "auth" not in requests[0]
    assert requests[1]["auth"] == "mock auth token 1"


async def test_auth_error_should_cause_auto_relogin(mock_server_app, zapi):
    """Login error should be transparent."""
    await zapi.login(user="Admin", password="zabbix")
    await zapi.hostgroup.get()

    mock_server_app["state"].logged_in = False

    await zapi.hostgroup.get()

    requests = [await r.json() for r in mock_server_app["state"].requests]
    assert len(requests) == 5
    assert requests[0]["method"] == "user.login"
    assert requests[1]["method"] == "hostgroup.get"
    # Second hostgroup.get that fails due to being logged out
    assert requests[2]["method"] == "hostgroup.get"
    assert requests[2]["auth"] == "mock auth token 1"
    # Auto login
    assert requests[3]["method"] == "user.login"
    # Retry of hostgroup.get
    assert requests[4]["method"] == "hostgroup.get"
    assert requests[4]["auth"] == "mock auth token 2"


async def test_import_underscore_attr_should_be_rewritten(mock_server_app, zapi):
    """Method call with the underscore."""
    await zapi.login(user="Admin", password="zabbix")
    await zapi.confimport(
        confformat="xml", rules={}, source="<zabbix_export>...</zabbix_export>"
    )

    requests = [await r.json() for r in mock_server_app["state"].requests]
    assert len(requests) == 2
    assert requests[1]["method"] == "configuration.import"
    assert requests[1]["params"] == {
        "format": "xml",
        "rules": {},
        "source": "<zabbix_export>...</zabbix_export>",
    }


async def test_custom_headers_should_be_sent(mock_server_app, client_session):
    """Method call with custom headers."""
    zapi = ZabbixAPI(
        server="", client_session=client_session, headers={"User-Agent": "zabbixapp"}
    )

    await zapi.apiinfo.version()

    requests = mock_server_app["state"].requests
    assert len(requests) == 1
    assert requests[0].headers["User-Agent"] == "zabbixapp"


async def test_zabbix_api_copies_should_share_state_correctly(
    mock_server_app, client_session
):
    """Method call with shared state."""
    zapi = ZabbixAPI(
        server="", client_session=client_session, headers={"User-Agent": "zabbixapp"}
    )

    await zapi.apiinfo.version()

    zapi_with_extra_header = zapi.with_headers({"X-Extra-Header": "Yes"})
    await zapi_with_extra_header.apiinfo.version()

    await zapi.apiinfo.version()

    requests = mock_server_app["state"].requests
    assert len(requests) == 3

    assert requests[0].headers["User-Agent"] == "zabbixapp"
    assert "X-Extra-Header" not in requests[0].headers

    assert requests[1].headers["User-Agent"] == "zabbixapp"
    assert requests[1].headers["X-Extra-Header"] == "Yes"

    assert requests[2].headers["User-Agent"] == "zabbixapp"
    assert "X-Extra-Header" not in requests[2].headers

    request_ids = [(await r.json())["id"] for r in mock_server_app["state"].requests]
    assert request_ids == [0, 1, 2]


async def test_zabbix_api_object_copies_should_relogin_correctly(mock_server_app, zapi):
    """Method call with a copy should relogin."""
    await zapi.login(user="Admin", password="zabbix")
    await zapi.hostgroup.get()

    mock_server_app["state"].logged_in = False
    zapi_with_extra_header = zapi.with_headers({"X-Extra-Header": "Yes"})

    await zapi_with_extra_header.hostgroup.get()

    requests = [await r.json() for r in mock_server_app["state"].requests]
    assert len(requests) == 5
    assert requests[0]["method"] == "user.login"
    assert requests[1]["method"] == "hostgroup.get"
    # Second hostgroup.get that fails due to being logged out
    assert requests[2]["method"] == "hostgroup.get"
    assert requests[2]["auth"] == "mock auth token 1"
    # Auto login
    assert requests[3]["method"] == "user.login"
    # Retry of hostgroup.get
    assert requests[4]["method"] == "hostgroup.get"
    assert requests[4]["auth"] == "mock auth token 2"


async def test_zabbix_api_args_and_kwargs(mock_server_app, zapi):
    """Method call arg and kwarg mix."""
    await zapi.login(user="Admin", password="zabbix")
    # Should work with args
    await zapi.sub.method("arg1", "arg2")
    # should work with kwargs
    await zapi.sub.method(kwarg1="kwarg", kwarg2="kwargier")
    # login + two requests should be performed
    assert len(mock_server_app["state"].requests) == 3
    # should fail with mix of args + kwargs
    with pytest.raises(TypeError):
        await zapi.sub.method("arg", kwarg1="kwarg", kwarg2="kwargier")
    # no request should have gone to the server.
    assert len(mock_server_app["state"].requests) == 3


async def error_not_json(request):
    """Simple server that returns non-json data."""
    request.app["state"].requests.append(request)
    await request.json()
    return web.Response(
        text="This is not JSON?  Why would a server send something other than JSON?"
    )


async def test_odd_http_error_should_raise(aiohttp_client):
    """Set up a web server that returns HTTP data rather than JSON."""
    app = web.Application()
    app.router.add_post("/api_jsonrpc.php", error_not_json)
    app["state"] = AppState(requests=[], logged_in=False, next_auth_token=1)
    client_session = await aiohttp_client(app)
    zapi = ZabbixAPI(server="", client_session=client_session)

    with pytest.raises(ZabbixAPIException):
        await zapi.apiinfo.version()
