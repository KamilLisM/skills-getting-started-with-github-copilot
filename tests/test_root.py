"""
Tests for the root endpoint GET /.
"""

import pytest


class TestRootEndpoint:
    """Test cases for the root endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to the static index.html file.
        
        AAA Pattern:
        - Arrange: Create test client
        - Act: Make GET request to root endpoint with follow_redirects=False
        - Assert: Verify response status is 307 (temporary redirect) and location header points to /static/index.html
        """
        # Arrange
        expected_status_code = 307
        expected_location = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status_code
        assert response.headers["location"] == expected_location

    def test_root_redirect_location_header_exists(self, client):
        """
        Test that the redirect response includes a location header.
        
        AAA Pattern:
        - Arrange: Create test client
        - Act: Make GET request to root endpoint
        - Assert: Verify location header is present in response
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert "location" in response.headers
