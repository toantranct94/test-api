
from typing import List, Union

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    APP_NAME: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    API_PREFIX: str = "/api"

    description = """
        Caching service
    """
    debug: bool = True

    # rabbitmq
    amqp_url: str = "amqp://guest:guest@localhost"

    # redis
    redis_host: str = "localhost"
    redis_port: str = 6379
    redis_password: str = None
    redis_db: int = 0
    default_cache_ttl: int = 3600

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
