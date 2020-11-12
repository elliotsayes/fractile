from fastapi import FastAPI
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from fractile import cache
from fractile.cache import save_tile
from fractile.model import FractalType
from fractile.tile import get_fractal_tile

app = FastAPI()


@app.on_event("startup")
def startup():
    cache.startup()


@app.on_event("shutdown")
def shutdown():
    cache.shutdown()


@app.get("/api/tiles/{fractal_type}/{zoom}/{x}/{y}/tile.png")
async def tiles(fractal_type: FractalType, zoom: int, x: int, y: int):
    if zoom < 0 or any(i < 0 or i >= (pow(2, zoom)) for i in [x, y]):
        return

    img_buffer = get_fractal_tile(x, y, zoom, fractal_type)
    cache_task = BackgroundTask(save_tile, img_buffer, x, y, zoom, fractal_type)

    return StreamingResponse(
        img_buffer,
        media_type="image/png",
        headers={'Content-Disposition': 'inline; filename="tile.png"'},
        background=cache_task)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="index.html")


app.mount("/", StaticFiles(directory="webui"), name="webui")
