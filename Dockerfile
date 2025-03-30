ARG BASE_IMAGE=python:3.10-slim

FROM ${BASE_IMAGE} as builder
ARG POETRY_VERSION=1.5.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python -m pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
RUN poetry config virtualenvs.create false \
    && poetry install --without=dev --no-cache --no-interaction --no-ansi

FROM ${BASE_IMAGE}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN poetry config virtualenvs.create false

COPY ./backend /app/backend
COPY ./pyproject.toml /app/pyproject.toml
COPY ./gunicorn.conf.py /app/gunicorn.conf.py
COPY ./alembic.ini /app/alembic.ini
COPY ./scripts/wait-fot-it.sh /app/scripts/wait-for-it.sh

CMD [ "poetry", "run", "gunicorn" ]
