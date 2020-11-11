import sys

from fastapi import FastAPI

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def read_root():
    message = f"Hello Fractile! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}
