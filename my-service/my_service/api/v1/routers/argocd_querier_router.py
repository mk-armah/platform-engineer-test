from fastapi import APIRouter, Depends

from my_service.clients.argocd_client import ArgocdClient
from my_service.dependencies import get_token
from my_service.models.models import (
    ListApplicationResponse,
    ListProjectResponse,
    ObjectKind,
)
from my_service.utils.logger import setup_logger

router = APIRouter(
    prefix="/argocd",
    tags=["argocd"],
)


logger = setup_logger()


@router.get("/application_status")
async def application_status(token: str = Depends(get_token)):
    """Fetches all ArgoCD applications statuses

    Args:
        token (str, optional): _description_. Defaults to Depends(get_token).

    Returns:
        applications_data_conscise: concise application metadata json strucure
    """
    async with ArgocdClient(
        token=token,
    ) as client:
        apps = await client.get_resources(ObjectKind.APPLICATIONS)
        return ListApplicationResponse(applications=apps)


@router.get("/list_projects")
async def list_projects(token: str = Depends(get_token)):
    """Fetches all argocd projects names and namespaces to which they are configured

    Args:
        token (str, optional): _description_. Defaults to Depends(get_token).
    Returns:
        projects_data_conscise: concise argocd projects metadata json strucure
    """

    async with ArgocdClient(
        token=token,
    ) as client:
        projects = await client.get_resources(ObjectKind.PROJECTS)

        return ListProjectResponse(projects=projects)
