"""Tests for the root endpoint using AAA pattern"""

import pytest


def test_root_redirects_to_static(client):
    """Test that GET / redirects to /static/index.html"""
    # Arrange
    expected_redirect_path = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert expected_redirect_path in response.headers["location"]


def test_root_with_follow_redirects(client):
    """Test that GET / eventually serves the static page"""
    # Arrange
    expected_content_type = "text/html"
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    assert expected_content_type in response.headers.get("content-type", "")
