from enum import Enum


TILE_SIZE = 256


class FractalType(str, Enum):
    mandelbrot = 'mandelbrot'
    julia = 'julia'
