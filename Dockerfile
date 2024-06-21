FROM python:3.11-slim-buster

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENV_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . /app

# CMD ["uvicorn", "faheem.server:app", "--host", "0.0.0.0", "--port", "3030"]
CMD ["fastapi", "run", "faheem/server.py"]
