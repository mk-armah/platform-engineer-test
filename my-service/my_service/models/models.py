from pydantic import BaseModel
from enum import StrEnum
from typing import Dict, List, Any
from pydantic import BaseModel, root_validator


class HealthCheckResponse(BaseModel):
    status_code: int
    message: str


class ArgoCDCreds(BaseModel):
    username: str
    password: str


class ObjectKind(StrEnum):
    PROJECTS = "projects"
    APPLICATIONS = "applications"


class ApplicationResponse(BaseModel):
    application_name: str
    status: str

    @root_validator(pre=True)
    def extract_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        name = values.get("metadata", {}).get("name")
        sync_status = values.get("status", {}).get("sync", {}).get("status")
        return {"application_name": name, "status": sync_status}


class ListApplicationResponse(BaseModel):
    applications: List[ApplicationResponse]


class ProjectResponse(BaseModel):
    project_name: str
    namespace: str

    @root_validator(pre=True)
    def extract_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        metadata = values.get("metadata", {})
        name = metadata.get("name", "")
        namespace = metadata.get("namespace", "")
        return {"project_name": name, "namespace": namespace}


class ListProjectResponse(BaseModel):
    projects: List[ProjectResponse]
