FROM fastgpu:latest

WORKDIR /app
COPY requirements-docker.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY fractile /app/fractile
COPY main.py /app/main.py
