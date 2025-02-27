from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BACKEND_ORIGINS: List[AnyHttpUrl] = []
    FASTAPI_PROJECT_NAME: str = "my-service"
    LOG_LEVEL: str = "DEBUG"
    ENVIRONMENT: str = "development"

    # ArgoCD Config defaults
    ARGOCD_SERVER: str = "localhost"
    ARGOCD_PORT: str = "<ARGOCD_PORT>"
    ARGOCD_URL: str = f"{ARGOCD_SERVER}:{ARGOCD_PORT}"
    ARGOCD_PASSWORD: str = "<ARGOCD_ADMIN_USER_PASSWORD>"
    ARGOCD_USERNAME: str = "admin"  # default argocd user
    TOKEN_CACHE_TTL: int = 600
    IGNORE_SERVER_ERROR: bool = False
    ALLOW_INSECURE: bool = True

    model_config = SettingsConfigDict(env_nested_delimiter="__")


settings = Settings(_env_file=".env")  # type: ignore
