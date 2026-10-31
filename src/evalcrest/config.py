from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Evalcrest's configuration, read from the environment and .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    studybuddy_url: str = "http://127.0.0.1:8000"
    studybuddy_username: str
    studybuddy_password: SecretStr
    studybuddy_document_id: int = Field(ge=1)
    studybuddy_timeout_s: float = Field(default=60.0, gt=0)
