from io import BytesIO
from typing import Optional

import redis
import os

from fractile.model import FractalType

REDIS_ENABLED = os.environ.get("REDIS_ENABLED")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_EXPIRY = 3600

con: redis.client.Redis = None


def startup():
    global con
    if not REDIS_ENABLED:
        return False
    con = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def shutdown():
    global con
    con.close()


def stringify_args(*args):
    return ",".join([str(arg) for arg in args])


def tile_key(x: int, y: int, z: int, fractal_type: FractalType):
    return f"TILE:{stringify_args(x, y, z, fractal_type)}"


def lookup_tile(x: int, y: int, z: int, fractal_type: FractalType) -> Optional[BytesIO]:
    global con
    if not con:
        return None
    key = tile_key(x, y, z, fractal_type)
    data = con.get(key)
    if not data:
        return None
    con.expire(key, REDIS_EXPIRY)
    con.close()
    return BytesIO(data)


def save_tile(buffer: BytesIO, x: int, y: int, z: int, fractal_type: FractalType) -> bool:
    global con
    if not con:
        return False
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    key = tile_key(x, y, z, fractal_type)
    if r.exists(key):
        return False
    r.set(key, buffer.getvalue())
    r.expire(key, REDIS_EXPIRY)
    return True
