"""Tests for the /activities endpoint using AAA pattern"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange
    # (No setup needed, activities are pre-loaded)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_has_correct_structure(client):
    """Test that activities have the expected data structure"""
    # Arrange
    expected_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    # Assert
    assert response.status_code == 200
    for field in expected_fields:
        assert field in activity
    
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_contains_initial_participants(client):
    """Test that activities contain initial participants"""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    actual_participants = data["Chess Club"]["participants"]
    
    # Assert
    assert response.status_code == 200
    assert len(actual_participants) > 0
    for participant in expected_chess_participants:
        assert participant in actual_participants
