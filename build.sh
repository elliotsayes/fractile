#!/usr/bin/env bash
docker build -f fastgpu/Dockerfile -t fastgpu:latest fastgpu
docker build -t fractile:latest .