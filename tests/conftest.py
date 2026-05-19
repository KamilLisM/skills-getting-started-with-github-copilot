"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient
import os
from pathlib import Path


def create_app():
    """
    Create a fresh FastAPI app instance with clean in-memory data.
    This ensures test isolation by providing a new app for each test.
    
    Returns:
        FastAPI: A new FastAPI application instance with reset data.
    """
    app = FastAPI(title="Mergington High School API",
                  description="API for viewing and signing up for extracurricular activities")

    # Mount the static files directory
    app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent.parent,
              "src", "static")), name="static")

    # In-memory activity database (fresh copy for each test)
    activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Practice teamwork, drills, and matches in a friendly school league",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and water safety with lap practices and relay events",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Explore acting, stagecraft, and rehearsal for school performances",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["sophia@mergington.edu", "ryan@mergington.edu"]
        },
        "Painting Workshop": {
            "description": "Create paintings, learn color theory, and display artwork in the school gallery",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Sharpen problem-solving skills with challenging math puzzles and competitions",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["lucas@mergington.edu", "chloe@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking, research, and competitive debate formats",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 16,
            "participants": ["amelia@mergington.edu", "jack@mergington.edu"]
        }
    }

    @app.get("/")
    def root():
        return RedirectResponse(url="/static/index.html")

    @app.get("/activities")
    def get_activities():
        return activities

    @app.delete("/activities/{activity_name}/signup")
    def unregister_from_activity(activity_name: str, email: str):
        """Unregister a student from an activity"""
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        activity = activities[activity_name]

        if email not in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is not signed up")

        activity["participants"].remove(email)
        return {"message": f"Unregistered {email} from {activity_name}"}

    @app.post("/activities/{activity_name}/signup")
    def signup_for_activity(activity_name: str, email: str):
        """Sign up a student for an activity"""
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        activity = activities[activity_name]

        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        activity["participants"].append(email)
        return {"message": f"Signed up {email} for {activity_name}"}

    return app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance for making requests to the app.
    Creates a fresh app instance with clean data for each test.
    
    Returns:
        TestClient: A test client connected to a fresh FastAPI application instance.
    """
    app = create_app()
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
