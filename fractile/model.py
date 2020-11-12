from enum import Enum


class FractalType(str, Enum):
    mandelbrot = 'mandelbrot'
    julia = 'julia'
