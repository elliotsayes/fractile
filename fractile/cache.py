from io import BytesIO
from typing import Optional

import redis
import os

from fractile.model import FractalType

REDIS_ENABLED = os.environ.get("REDIS_ENABLED")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


def hash_args(*args):
    return ",".join([str(arg) for arg in args])


def tile_key(x: int, y: int, z: int, fractal_type: FractalType):
    return f"TILE:{hash_args(x, y, z, fractal_type)}"


def lookup_tile(x: int, y: int, z: int, fractal_type: FractalType) -> Optional[BytesIO]:
    if not REDIS_ENABLED:
        return None
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    key = tile_key(x, y, z, fractal_type)
    data = r.get(key)
    if not data:
        return None
    return BytesIO(data)


def save_tile(buffer: BytesIO, x: int, y: int, z: int, fractal_type: FractalType) -> bool:
    if not REDIS_ENABLED:
        return False
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    key = tile_key(x, y, z, fractal_type)
    if r.exists(key):
        return False
    r.set(key, buffer.getvalue())
    return True
