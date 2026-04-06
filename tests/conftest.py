"""Pytest configuration and fixtures for the API tests"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities(client):
    """Reset the activities database to a known state before each test"""
    # This fixture ensures tests have a clean state
    # The app uses an in-memory database that persists during test session
    yield
    # Teardown: reset activities after each test by reloading the module
    import importlib
    import src.app
    importlib.reload(src.app)
