import io

from fastapi import FastAPI
from starlette.responses import StreamingResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from fractile.generate import get_fractal_tile
from fractile.model import FractalType

app = FastAPI()


@app.get("/api/tiles/{fractal_type}/{zoom}/{x}/{y}/tile.png")
async def tiles(fractal_type: FractalType, zoom: int, x: int, y: int):
    if zoom < 0 or any(i < 0 or i >= (pow(2, zoom)) for i in [x, y]):
        return

    img = get_fractal_tile(x, y, zoom, fractal_type)

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return StreamingResponse(buffer,
                             media_type="image/png",
                             headers={'Content-Disposition': 'inline; filename="tile.png"'})


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="index.html")


app.mount("/", StaticFiles(directory="webui"), name="webui")
