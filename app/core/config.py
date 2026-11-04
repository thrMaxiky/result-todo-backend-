import os
from dataclasses import dataclass
from functools import lru_cache


# будем сразу писать с переменной окружения, нужно разобраться что это
@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_allowed_origins: list[str]


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres",
        ),
        cors_allowed_origins=os.getenv(
            "CORS_ALLOWED_ORIGINS",
            "http://localhost:3000",
        ).split(","),
    )
