import math

import cupy as np

from fractile.kernel import kernel_map
from fractile.model import TILE_SIZE, FractalType

SCALE = 3


def get_fractal_coords(tile_x: int, tile_y: int, tile_z: int) -> np.ndarray:
    x_offset = tile_x * TILE_SIZE
    y_offset = tile_y * TILE_SIZE

    map_size = math.pow(2, tile_z) * TILE_SIZE

    real_start, real_stop = map(
        lambda x: SCALE * ((x + 0.5) / map_size - 0.5) - 0.5,
        [x_offset, x_offset + TILE_SIZE])
    imag_start, imag_stop = map(
        lambda y: SCALE * (0.5 - (y + 0.5) / map_size),
        [y_offset, y_offset + TILE_SIZE])

    return np.meshgrid(
        np.linspace(real_start, real_stop, num=TILE_SIZE, dtype=np.float64),
        np.linspace(imag_start, imag_stop, num=TILE_SIZE, dtype=np.float64))


def get_fractal_iterations(tile_x: int, tile_y: int, tile_z: int, fractal_type: FractalType):
    real, imag = get_fractal_coords(tile_x, tile_y, tile_z)

    kernel = kernel_map[fractal_type]
    iterations = kernel(real, imag)

    return iterations


def colour_iterations(i: np.ndarray) -> np.ndarray:
    li = np.log(i)

    img = np.empty((TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)
    img[:, :, 0] = (li * 255) % 255
    img[:, :, 1] = 128
    img[:, :, 2] = 128 + 13 * np.sin(li * 100) - np.minimum(115, (10000 * 13 / (10000 - i)))

    return img
