import cupy as cp

from fractile.model import FractalType

mandelbrot_kernel = cp.ElementwiseKernel(
    "float64 c_r, float64 c_i",
    "int64 m",
    """
    double z_r = c_r;
    double z_i = c_i;

    m = 10000;
    for(int iter=1; iter<=m; iter++){
        double temp = (z_r*z_r) - (z_i*z_i) + c_r;
        z_i = z_r*z_i*2. + c_i;
        z_r = temp;

        if((z_r*z_r+z_i*z_i)>4.0){
          m = iter;
          break;
        }
    }
    """,
    "mandelbrot")

julia_kernel = cp.ElementwiseKernel(
    "float64 c_r, float64 c_i",
    "int64 m",
    """
    double z_r = c_r;
    double z_i = c_i;

    double k_r = -0.8;
    double k_i = 0.156;

    m = 10000;
    for(int iter=1; iter<=m; iter++){
        double temp = (z_r*z_r) - (z_i*z_i) + k_r;
        z_i = z_r*z_i*2. + k_i;
        z_r = temp;

        if((z_r*z_r+z_i*z_i)>4.0){
          m = iter;
          break;
        }
    }
    """,
    "julia")

kernel_map = {
    FractalType.mandelbrot: mandelbrot_kernel,
    FractalType.julia: julia_kernel,
}
