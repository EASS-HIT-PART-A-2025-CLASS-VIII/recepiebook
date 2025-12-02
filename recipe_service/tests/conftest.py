import pytest
from fastapi.testclient import TestClient

from recipe_service.app.main import app
from recipe_service.app.dependencies import get_repository


@pytest.fixture(autouse=True)
def clear_repository():
    """Clear repo before each test."""
    repo = next(get_repository())
    repo.clear()
    yield
    repo.clear()


@pytest.fixture
def client():
    return TestClient(app)
