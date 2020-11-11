from enum import Enum

TILE_SIZE = 512


class FractalType(str, Enum):
    mandelbrot = 'mandelbrot'
    julia = 'julia'
