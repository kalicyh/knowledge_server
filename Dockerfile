FROM node:22-alpine AS build

WORKDIR /app

COPY . ./
RUN yarn install
RUN yarn build

FROM python:3.12-alpine AS builder

WORKDIR /app

RUN apk add --no-cache curl gcc g++ libffi-dev musl-dev

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

FROM python:3.12-alpine AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY api/ ./api

COPY --from=build /app/dist /app/dist

ENV DATABASE_URL=
ENV VITE_API_BASE_URL=

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
