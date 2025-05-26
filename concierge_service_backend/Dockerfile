FROM python:3.11.5-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl libpq-dev && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8080

CMD ["uvicorn", "server.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
