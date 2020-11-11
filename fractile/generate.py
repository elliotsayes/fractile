import numpy as np
from PIL import Image

from fractile.model import FractalType, TILE_SIZE


def get_fractal_tile(x: int, y: int, z: int, fractal_type: FractalType):
    arr = np.ndarray((TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)

    arr[:, :, 0] = 0
    arr[:, :, 1] = 0
    arr[:, :, 2] = 0

    return Image.fromarray(arr, "RGB")
