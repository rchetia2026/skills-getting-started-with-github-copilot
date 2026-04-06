"""Pytest configuration and fixtures for the API tests"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    # Reload the app module before each test to get a fresh database state
    import importlib
    import src.app
    importlib.reload(src.app)
    return TestClient(src.app.app)
