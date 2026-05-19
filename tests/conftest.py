"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance for making requests to the app.
    
    Returns:
        TestClient: A test client connected to the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def valid_email():
    """
    Fixture providing a valid email format for testing.
    
    Returns:
        str: A valid test email address.
    """
    return "test@mergington.edu"


@pytest.fixture
def valid_activity():
    """
    Fixture providing a valid activity name that exists in the app.
    
    Returns:
        str: A valid activity name.
    """
    return "Chess Club"


@pytest.fixture
def invalid_activity():
    """
    Fixture providing an activity name that does not exist in the app.
    
    Returns:
        str: An invalid activity name.
    """
    return "Nonexistent Activity"
