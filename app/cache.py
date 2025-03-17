from functools import wraps
from typing import Callable

import redis

from app.settings import REDIS_URL, DEFAULT_EXPIRE_TIME

redis_client = redis.from_url(REDIS_URL)


def cache(expire_time: int = DEFAULT_EXPIRE_TIME):
    """
    Decorator for caching function results using Redis.

    This is useful for caching expensive operations like database queries
    that don't change frequently, such as listing all tasks or retrieving
    task details.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            cached_data = redis_client.get(key)
            if cached_data:
                return {"_cached": True, "data": cached_data.decode("utf-8")}

            result = await func(*args, **kwargs)

            redis_client.setex(key, expire_time, str(result))

            return result

        return wrapper

    return decorator


def invalidate_cache(pattern: str = ""):
    """
    Invalidate cache entries that match the pattern.
    """
    for key in redis_client.scan_iter(f"*{pattern}*"):
        redis_client.delete(key)
