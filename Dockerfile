ARG DOMAIN=docker.io
ARG CONTAINER_REPO=elliotsayes
ARG CONTAINER_SUFFIX
ARG TAG=latest
FROM $DOMAIN/$CONTAINER_REPO/cuda-fastapi-cupy$CONTAINER_SUFFIX:$TAG

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
