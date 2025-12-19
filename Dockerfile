FROM python:3.10.4-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/home/appuser/web/

WORKDIR ${WORKDIR}

RUN mkdir ${WORKDIR}/staticfiles

# Install system dependencies with retry and cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
        build-essential \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* 

RUN pip install --upgrade pip

# Copy requirements file and install dependencies
COPY requirements.txt ${WORKDIR}

RUN pip install --no-cache-dir -r requirements.txt

COPY . ${WORKDIR}

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser ${WORKDIR}

USER appuser

EXPOSE 8000
