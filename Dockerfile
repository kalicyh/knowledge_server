# Step 1: Build the Vue.js application
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies and build the Vue.js app
COPY package.json yarn.lock ./
RUN yarn install
COPY . ./
RUN yarn build

# Step 2: Set up the FastAPI application with Poetry using a smaller Python image
FROM python:3.12-alpine AS runtime

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache curl gcc g++ libffi-dev musl-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy FastAPI code
COPY api/ ./api

# Copy the built Vue.js app into the FastAPI image
COPY --from=build /app/dist /app/dist

# Set environment variable
ENV DATABASE_URL=

# Expose ports
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
