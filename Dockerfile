FROM python:3.11-slim-buster

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENV_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY faheem ./faheem

EXPOSE 80

CMD ["uvicorn", "faheem.server.app:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-include", "*"]
