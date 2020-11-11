FROM nvidia/cuda:11.1-devel

LABEL maintainer="Elliot Sayes <elliot@sayes.cloud>"

ENV PYTHON_MAJOR=3
ENV PYTHON_MINOR=8
ENV PYTHON_VERSION=${PYTHON_MAJOR}.${PYTHON_MINOR}

# Install python
RUN apt-get update && \
    apt-get install -y \
        python${PYTHON_VERSION} \
        python${PYTHON_MAJOR}-pip && \
    apt-get clean

RUN pip3 install --no-cache-dir \
    uvicorn[standard] \
    gunicorn \
    fastapi

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

WORKDIR /app
COPY ./app /app
ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
