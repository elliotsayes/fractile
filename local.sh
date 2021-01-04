#!/usr/bin/env bash
REDIS_ENABLED=${1:-0} REDIS_HOST=${2:-localhost} REDIS_PORT=${3:-6379} uvicorn main:app --reload