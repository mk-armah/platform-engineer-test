import pytest
from aioresponses import aioresponses

from my_service.clients.argocd_client import ArgocdClient

pytestmark = pytest.mark.asyncio

TEST_SERVER_URL = "test-server"


@pytest.mark.asyncio
async def test_get_resources_success():
    """Test that the client can fetch resources successfully."""
    token = "testtoken"
    resource_kind = "applications"
    api_url = f"https://{TEST_SERVER_URL}/api/v1"
    url = f"{api_url}/{resource_kind}"

    expected_payload = {
        "items": [{"metadata": {"name": "app1"}}, {"metadata": {"name": "app2"}}]
    }

    client = ArgocdClient(
        token=token,
        server_url=TEST_SERVER_URL,
        ignore_server_error=False,
        allow_insecure=True,  # For testing, allow insecure connections
    )

    with aioresponses() as mocked:
        mocked.get(url, payload=expected_payload)
        async with client as ac:
            items = await ac.get_resources(resource_kind)
            assert items == expected_payload["items"]


@pytest.mark.asyncio
async def test_get_resources_ignore_error():
    token = "testtoken"
    resource_kind = "applications"
    api_url = f"https://{TEST_SERVER_URL}/api/v1"
    url = f"{api_url}/{resource_kind}"

    # Set ignore_server_error to True so errors are swallowed and an empty list is returned.
    client = ArgocdClient(
        token=token,
        server_url=TEST_SERVER_URL,
        ignore_server_error=True,
        allow_insecure=True,
    )

    with aioresponses() as mocked:
        # Simulate a 500 Internal Server Error response.
        mocked.get(url, status=500)
        async with client as ac:
            items = await ac.get_resources(resource_kind)
            # Since ignore_server_error is True, we expect an empty list.
            assert items == []


@pytest.mark.asyncio
async def test_aenter_aexit_session():
    """Verify that the client session is created and then closed."""

    token = "testtoken"
    client = ArgocdClient(
        token=token,
        server_url=TEST_SERVER_URL,
        ignore_server_error=False,
        allow_insecure=True,
    )

    async with client as ac:
        # Ensure that a session exists during the context.
        assert ac.session is not None
        # Check that the Authorization header is set correctly.
        assert ac.session.headers.get("Authorization") == f"Bearer {token}"
    # After the context manager, the session is closed (no error was raised).
