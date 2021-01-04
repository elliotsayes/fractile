from io import BytesIO
from typing import Optional

import redis
from pydantic import BaseSettings

from fractile.model import FractalType


class RedisSettings(BaseSettings):
    REDIS_ENABLED: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_EXPIRY: int = 3600


redis_settings = RedisSettings()
con: redis.client.Redis = None


def startup():
    global con, redis_settings
    if not redis_settings.REDIS_ENABLED:
        return False
    con = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT)
    return True


def shutdown():
    global con, redis_settings
    if not redis_settings.REDIS_ENABLED:
        return False
    con.close()
    return True


def stringify_args(*args):
    return ",".join([str(arg) for arg in args])


def tile_key(x: int, y: int, z: int, fractal_type: FractalType):
    return f"TILE:{stringify_args(x, y, z, fractal_type)}"


def lookup_tile(x: int, y: int, z: int, fractal_type: FractalType) -> Optional[BytesIO]:
    global con, redis_settings
    if not con:
        return None
    key = tile_key(x, y, z, fractal_type)
    data = con.get(key)
    if not data:
        return None
    con.expire(key, redis_settings.REDIS_EXPIRY)
    con.close()
    return BytesIO(data)


def save_tile(buffer: BytesIO, x: int, y: int, z: int, fractal_type: FractalType) -> bool:
    global con, redis_settings
    if not con:
        return False
    key = tile_key(x, y, z, fractal_type)
    if con.exists(key):
        return False
    con.set(key, buffer.getvalue())
    con.expire(key, redis_settings.REDIS_EXPIRY)
    return True
