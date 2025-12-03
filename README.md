# Recipe API

A simple FastAPI service that exposes CRUD endpoints for managing recipes.
All data is stored in-memory, and the service runs fully inside Docker using docker-compose.

## Project Layout

```
recipe_service/
├── app/
│   ├── main.py              # FastAPI application + routes
│   ├── models.py            # Pydantic models (Recipe, RecipeCreate)
│   ├── repository.py        # In-memory recipe repository
│   ├── dependencies.py      # Dependency injection for repository + settings
│   └── config.py            # App configuration using pydantic-settings
└── tests/
    ├── test_recipes.py      # CRUD tests for the API
    └── conftest.py          # TestClient setup

Dockerfile                   # Docker build file
docker-compose.yml           # Docker Compose service definition
pyproject.toml               # Project dependencies and metadata
README.md                    # Documentation (this file)
```

## API Endpoints

The API includes:

- **POST /recipes** — create a recipe
- **GET /recipes** — list all recipes
- **GET /recipes/{id}** — retrieve recipe by ID
- **DELETE /recipes/{id}** — delete a recipe
- **GET /health** — health check (returns app name)

All responses conform to the Pydantic models.

## Getting Started

### Run the API using Docker Compose (Recommended)

From the project root:

```bash
docker compose up --build
```

Then open:

```
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger UI where you can test every endpoint.

### Live Demo

You can also try the running service on the public demo instance:

```
https://recepiebook.onrender.com/docs#/
```

Note: this project is hosted on a free tier. The service may take a couple of minutes to start (cold start) when it's not been used recently — please allow time for the demo to load on first access.

### Running the Tests (without Docker)

Inside your virtual environment:

```bash
uv run pytest
```

All tests should pass (7 tests total).

### Development (Local, without Docker)

If you want to run the API locally:

```bash
uv run uvicorn recipe_service.app.main:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

### Building & Running with Docker (Manual Method)

Build the image:

```bash
docker build -t recipe-service .
```

Run the container:

```bash
docker run -p 8000:8000 recipe-service
```

## Configuration

Configuration lives in:

```
recipe_service/app/config.py
```

The app uses pydantic-settings for environment-based configuration.
The default application name is:

```python
app_name: str = "Recipe Service"
```

You can override settings using environment variables with the `RECIPE_` prefix. For example:

```bash
export RECIPE_APP_NAME="My Recipe App"
docker compose up
```

## Features

- ✅ Full CRUD operations
- ✅ Input validation with Pydantic
- ✅ Type hints throughout
- ✅ Comprehensive test coverage (8 tests)
- ✅ Docker containerization with health checks
- ✅ Health check endpoint
- ✅ Structured logging
- ✅ Clean dependency injection pattern
- ✅ Environment-based configuration
- ✅ Proper HTTP status codes and error handling