from enum import StrEnum
from typing import Any, Optional
import logging
import aiohttp

from my_service.utils.logger import setup_logger
from my_service.config.config import settings

logger = setup_logger()


class ObjectKind(StrEnum):
    PROJECTS = "projects"
    APPLICATIONS = "applications"


class ArgocdClient:
    def __init__(
        self,
        token: str,
        server_url: Optional[str] = None,
        ignore_server_error: bool = False,
        allow_insecure: bool = False,
    ):
        self.token = token
        self.api_url = f"https://{server_url or settings.ARGOCD_URL}/api/v1"
        self.ignore_server_error = ignore_server_error or settings.IGNORE_SERVER_ERROR
        self.allow_insecure = allow_insecure or settings.ALLOW_INSECURE
        self.api_auth_header = {"Authorization": f"Bearer {self.token}"}
        self.session: Optional[aiohttp.ClientSession] = None

        if self.allow_insecure:
            # Warning: Disabling SSL verification is not recommended for production
            logger.warning(
                "Insecure mode is enabled. SSL verification for the ArgoCD API client is disabled."
            )

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers=self.api_auth_header,
            connector=aiohttp.TCPConnector(ssl=not self.allow_insecure),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _send_api_request(
        self,
        url: str,
        method: str = "GET",
        query_params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        logger.info(f"Sending request to ArgoCD API: {method} {url}")
        try:
            async with self.session.request(
                method=method,
                url=url,
                params=query_params,
                json=json_data,
            ) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientResponseError as e:
            logger.error(f"HTTP error: status {e.status} with message: {e.message}")
            if self.ignore_server_error:
                return {}
            raise
        except aiohttp.ClientError as e:
            logger.error(
                f"Client error {e} during request {method} {url} with params {query_params}"
            )
            if self.ignore_server_error:
                return {}
            raise

    async def get_resources(self, resource_kind: str) -> list[dict[str, Any]]:
        url = f"{self.api_url}/{resource_kind}"
        try:
            response_data = await self._send_api_request(url=url)
            return response_data.get("items", [])
        except Exception as e:
            logger.error(f"Failed to fetch resources of kind {resource_kind}: {e}")
            if self.ignore_server_error:
                return []
            raise
