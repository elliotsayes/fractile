ARG PROJECT_ID
FROM gcr.io/$PROJECT_ID/cuda-fastapi-cupy-docker:11.1-devel

COPY requirements-docker.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

WORKDIR /app
COPY fractile fractile
COPY webui webui
COPY main.py main.py

ENV REDIS_ENABLED=0
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
