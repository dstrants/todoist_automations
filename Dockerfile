FROM python:3.10-alpine

LABEL version="0.2.0-alpha.0"

LABEL maintainer="Dimitris Strantsalis <dstrants@gmail.com>"

ENV PYTHONUNBUFFERED 1
ENV HOST=0.0.0.0
ENV PORT=8000
ENV POETRY_VIRTUANENVS_CREATE=false

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN apk add --no-cache libressl-dev musl-dev libffi-dev gcc  gcc make g++ zlib-dev curl\
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y\
    && source $HOME/.cargo/env\
    && pip install --disable-pip-version-check --no-cache-dir poetry\
    && poetry install --no-root --no-dev -n

ENTRYPOINT [ "poetry", "run", "uvicorn", "main:app", "--host", "${HOST}", "--port", "${PORT}" ]