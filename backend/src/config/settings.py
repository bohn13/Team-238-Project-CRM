from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    APP_TITLE: str = "Clinic CRM"
    APP_DESCRIPTION: str = "Clinic patient booking and management service"
    APP_VERSION: str = "0.1.0"
    FRONTEND_BASE_URL: str = "http://localhost:3000"

    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_HOST: str = "db"
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: str = "clinic_db"

    SECRET_KEY_ACCESS: str = "change-me-access"
    SECRET_KEY_REFRESH: str = "change-me-refresh"
    JWT_SIGNING_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LOGIN_TIME_DAYS: int = 7

    PATH_TO_EMAIL_TEMPLATES_DIR: str = str(BASE_DIR / "notifications" / "templates")
    ACTIVATION_EMAIL_TEMPLATE_NAME: str = "activation_request.html"
    ACTIVATION_COMPLETE_EMAIL_TEMPLATE_NAME: str = "activation_complete.html"
    PASSWORD_RESET_TEMPLATE_NAME: str = "password_reset_request.html"
    PASSWORD_RESET_COMPLETE_TEMPLATE_NAME: str = "password_reset_complete.html"

    EMAIL_HOST: str = "mailhog"
    EMAIL_PORT: int = 1025
    EMAIL_HOST_USER: str = "clinic@mail.com"
    EMAIL_HOST_PASSWORD: str = ""
    EMAIL_USE_TLS: bool = False
    EMAIL_FROM: str = "clinic@mail.com"

    S3_STORAGE_URL: str = "http://minio:9000"
    S3_STORAGE_ACCESS_KEY: str = "minio_admin"
    S3_STORAGE_SECRET_KEY: str = "minio_password"
    S3_BUCKET_NAME: str = "clinic-storage"
    REGION: str = "auto"

    PGADMIN_DEFAULT_EMAIL: str = "admin@example.com"
    PGADMIN_DEFAULT_PASSWORD: str = "admin"
    MAILHOG_USER: str = "clinic"
    MAILHOG_PASSWORD: str = "clinic"
    MINIO_ROOT_USER: str = "minio_admin"
    MINIO_ROOT_PASSWORD: str = "minio_password"
    MINIO_STORAGE: str = "clinic-storage"
    MINIO_URL: str = "http://minio:9000"

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def sync_database_url(self) -> str:
        return self.async_database_url.replace(
            "postgresql+asyncpg", "postgresql+psycopg"
        )

    @property
    def s3_storage_endpoint(self) -> str:
        return self.S3_STORAGE_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()
