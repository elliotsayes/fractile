import io

import cupy as cp
from PIL import Image

from fractile.cache import lookup_tile, save_tile
from fractile.generate import get_fractal_iterations, colour_iterations
from fractile.model import FractalType


def get_fractal_tile(x: int, y: int, z: int, fractal_type: FractalType) -> Image:
    img_buffer = lookup_tile(x, y, z, fractal_type)

    if not img_buffer:
        iter_gpu = get_fractal_iterations(x, y, z, fractal_type)
        img_gpu = colour_iterations(iter_gpu)

        img_arr = cp.asnumpy(img_gpu)
        img_hsv = Image.fromarray(img_arr, "HSV")
        img_rgb = img_hsv.convert("RGB")

        img_buffer = io.BytesIO()
        img_rgb.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        save_tile(img_buffer, x, y, z, fractal_type)

    return img_buffer
