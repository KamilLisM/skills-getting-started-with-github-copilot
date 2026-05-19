"""
Tests for the POST /activities/{activity_name}/signup and 
DELETE /activities/{activity_name}/signup endpoints.
"""

import pytest


class TestSignupEndpoint:
    """Test cases for signing up a student for an activity."""

    def test_signup_success_new_student(self, client, valid_activity, valid_email):
        """
        Test successful signup of a new student to an activity.
        
        AAA Pattern:
        - Arrange: Define valid activity name and email
        - Act: Make POST request to signup endpoint with valid parameters
        - Assert: Verify response status is 200 and confirmation message is returned
        """
        # Arrange
        expected_status_code = 200

        # Act
        response = client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": valid_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert "message" in response.json()
        assert valid_email in response.json()["message"]
        assert valid_activity in response.json()["message"]

    def test_signup_adds_student_to_participants(self, client, valid_activity, valid_email):
        """
        Test that signup actually adds the student to the activity's participant list.
        
        AAA Pattern:
        - Arrange: Get initial participants list
        - Act: Sign up student, then retrieve activities again
        - Assert: Verify student is now in the participants list
        """
        # Arrange
        response_before = client.get("/activities")
        initial_participants = response_before.json()[valid_activity]["participants"].copy()
        initial_count = len(initial_participants)

        # Act
        client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": valid_email}
        )
        response_after = client.get("/activities")
        updated_participants = response_after.json()[valid_activity]["participants"]

        # Assert
        assert valid_email in updated_participants
        assert len(updated_participants) == initial_count + 1

    def test_signup_duplicate_email_fails(self, client, valid_activity):
        """
        Test that signing up with an email already enrolled fails with 400 status.
        
        AAA Pattern:
        - Arrange: Use an email that is already in the participants list
        - Act: Attempt to sign up that email
        - Assert: Verify response status is 400 and error message is returned
        """
        # Arrange
        response = client.get("/activities")
        existing_email = response.json()[valid_activity]["participants"][0]
        expected_status_code = 400

        # Act
        response = client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self, client, valid_email, invalid_activity):
        """
        Test that signing up for a non-existent activity fails with 404 status.
        
        AAA Pattern:
        - Arrange: Use an activity name that doesn't exist
        - Act: Attempt to sign up for that activity
        - Assert: Verify response status is 404 and error message is returned
        """
        # Arrange
        expected_status_code = 404

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": valid_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert "not found" in response.json()["detail"]

    def test_signup_multiple_different_emails_success(self, client, valid_activity):
        """
        Test that multiple different emails can successfully sign up for the same activity.
        
        AAA Pattern:
        - Arrange: Create two different test emails
        - Act: Sign up both emails to the same activity
        - Assert: Verify both signups are successful and both emails are in participants
        """
        # Arrange
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        response_check = client.get("/activities")
        participants = response_check.json()[valid_activity]["participants"]
        assert email1 in participants
        assert email2 in participants


class TestUnregisterEndpoint:
    """Test cases for unregistering a student from an activity."""

    def test_unregister_success_existing_student(self, client, valid_activity):
        """
        Test successful unregistration of an existing student from an activity.
        
        AAA Pattern:
        - Arrange: Get an existing participant email
        - Act: Make DELETE request to unregister that email
        - Assert: Verify response status is 200 and confirmation message is returned
        """
        # Arrange
        response = client.get("/activities")
        email = response.json()[valid_activity]["participants"][0]
        expected_status_code = 200

        # Act
        response = client.delete(
            f"/activities/{valid_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert "message" in response.json()
        assert email in response.json()["message"]

    def test_unregister_removes_student_from_participants(self, client, valid_activity):
        """
        Test that unregister actually removes the student from the activity's participant list.
        
        AAA Pattern:
        - Arrange: Get an existing participant and verify they're in the list
        - Act: Unregister the student
        - Assert: Verify student is no longer in the participants list
        """
        # Arrange
        response_before = client.get("/activities")
        email = response_before.json()[valid_activity]["participants"][0]
        initial_count = len(response_before.json()[valid_activity]["participants"])

        # Act
        client.delete(
            f"/activities/{valid_activity}/signup",
            params={"email": email}
        )
        response_after = client.get("/activities")

        # Assert
        updated_participants = response_after.json()[valid_activity]["participants"]
        assert email not in updated_participants
        assert len(updated_participants) == initial_count - 1

    def test_unregister_nonexistent_activity_fails(self, client, valid_email, invalid_activity):
        """
        Test that unregistering from a non-existent activity fails with 404 status.
        
        AAA Pattern:
        - Arrange: Use an activity name that doesn't exist
        - Act: Attempt to unregister from that activity
        - Assert: Verify response status is 404 and error message is returned
        """
        # Arrange
        expected_status_code = 404

        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/signup",
            params={"email": valid_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert "not found" in response.json()["detail"]

    def test_unregister_non_enrolled_student_fails(self, client, valid_activity, valid_email):
        """
        Test that unregistering a student not enrolled in the activity fails with 400 status.
        
        AAA Pattern:
        - Arrange: Use an email that is not in the participants list
        - Act: Attempt to unregister that email
        - Assert: Verify response status is 400 and error message is returned
        """
        # Arrange
        expected_status_code = 400

        # Act
        response = client.delete(
            f"/activities/{valid_activity}/signup",
            params={"email": valid_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert "not signed up" in response.json()["detail"]

    def test_signup_after_unregister_success(self, client, valid_activity):
        """
        Test that a student can sign up again after unregistering.
        
        AAA Pattern:
        - Arrange: Get an existing participant
        - Act: Unregister them, then sign them up again
        - Assert: Verify both operations are successful
        """
        # Arrange
        response = client.get("/activities")
        email = response.json()[valid_activity]["participants"][0]

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{valid_activity}/signup",
            params={"email": email}
        )

        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200

        response_check = client.get("/activities")
        assert email in response_check.json()[valid_activity]["participants"]
