import json
from typing import Any
import redis
import random

from cache.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=settings.redis_db
)


class CacheService:
    @staticmethod
    def get(key: str) -> Any:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    @staticmethod
    def insert(key: str, value: Any, ttl: int = None) -> None:
        value_str = CacheService.__standalize(value)
        if ttl is None:
            # Add cache jitter to avoid cache avalanche
            jitter = random.randint(0, 60)
            ttl = settings.default_cache_ttl + jitter

        redis_client.setex(key, ttl, value_str)

    @staticmethod
    def __standalize(value: Any) -> str:
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value)
        else:
            return str(value)
