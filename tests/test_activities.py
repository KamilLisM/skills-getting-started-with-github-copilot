"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestActivitiesEndpoint:
    """Test cases for retrieving all activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: Set expected number of activities
        - Act: Make GET request to /activities endpoint
        - Assert: Verify response status is 200 and contains all activities
        """
        # Arrange
        expected_activity_count = 9
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Drama Club",
            "Painting Workshop",
            "Math Olympiad",
            "Debate Team"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_returns_200_ok(self, client):
        """
        Test that GET /activities returns a 200 OK status code.
        
        AAA Pattern:
        - Arrange: Create test client
        - Act: Make GET request to /activities endpoint
        - Assert: Verify response status is 200
        """
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_response_structure(self, client, valid_activity):
        """
        Test that each activity in the response has the correct structure.
        
        AAA Pattern:
        - Arrange: Define required fields for each activity
        - Act: Make GET request to /activities and retrieve response
        - Assert: Verify all activities have required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())

    def test_activity_description_is_string(self, client, valid_activity):
        """
        Test that activity descriptions are strings.
        
        AAA Pattern:
        - Arrange: Get activities from endpoint
        - Act: Extract a valid activity
        - Assert: Verify description is a string
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert isinstance(activities[valid_activity]["description"], str)

    def test_activity_schedule_is_string(self, client, valid_activity):
        """
        Test that activity schedules are strings.
        
        AAA Pattern:
        - Arrange: Get activities from endpoint
        - Act: Extract a valid activity
        - Assert: Verify schedule is a string
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert isinstance(activities[valid_activity]["schedule"], str)

    def test_activity_max_participants_is_integer(self, client, valid_activity):
        """
        Test that activity max_participants is an integer.
        
        AAA Pattern:
        - Arrange: Get activities from endpoint
        - Act: Extract a valid activity
        - Assert: Verify max_participants is an integer
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert isinstance(activities[valid_activity]["max_participants"], int)

    def test_activity_participants_is_list(self, client, valid_activity):
        """
        Test that activity participants is a list.
        
        AAA Pattern:
        - Arrange: Get activities from endpoint
        - Act: Extract a valid activity
        - Assert: Verify participants is a list
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert isinstance(activities[valid_activity]["participants"], list)

    def test_activity_participants_contain_valid_emails(self, client, valid_activity):
        """
        Test that all participants in an activity are non-empty strings.
        
        AAA Pattern:
        - Arrange: Get activities from endpoint
        - Act: Extract participants list from a valid activity
        - Assert: Verify all participants are strings with content
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        participants = activities[valid_activity]["participants"]

        # Assert
        for participant in participants:
            assert isinstance(participant, str)
            assert len(participant) > 0
