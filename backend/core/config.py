import os
import secrets
import sys
from pathlib import Path

import toml
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Quiz"
    API_V1_STR: str = "/api/v1"
    VERSION: str = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
    SECRET_KEY: str = ""
    SERVER_HOST: str = "http://localhost:8000"

    try:
        path = Path(__file__).resolve().parent
        sys.path.append(str(path))
        from backend.core.secret_key import SECRET_KEY  # noqa

        SECRET_KEY = SECRET_KEY
    except ImportError:
        with open(os.path.join(path, "secret_key.py"), "w") as f:
            secret_key = secrets.token_urlsafe(50)
            f.write(f"SECRET_KEY = '{secret_key}'\n")
        SECRET_KEY = secret_key

    # 60 minutes * 24 hours * 1 day = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    TOKEN_TYPE: str = "bearer"

    # Redis
    REDIS_URI: str = os.getenv("REDIS_URI", "redis://localhost:6379")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)

    # Database
    ENV_STATE: str = os.getenv("ENV_STATE", "dev")
    _DATABASE_URI: str = os.getenv(
        "DATABASE_URI", "postgresql+asyncpg://postgres:postgres@localhost/"
    )

    @property
    def DATABASE_URI(self) -> str:
        if self.ENV_STATE == "test":
            DATABASE_URI = self._DATABASE_URI + "test_db"
        elif self.ENV_STATE == "prod":
            DATABASE_URI = self._DATABASE_URI + "prod_db"
        else:
            DATABASE_URI = self._DATABASE_URI + "dev_db"

        return DATABASE_URI

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
