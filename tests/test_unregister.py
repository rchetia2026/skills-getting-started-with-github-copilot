"""Tests for the unregister endpoint using AAA pattern"""

import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "unregister_user@mergington.edu"
    
    # First signup the user
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # Arrange
    activity_name = "Programming Class"
    email = "alice_unregister@mergington.edu"
    
    # Setup: signup user
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Verify user is registered
    activities_before = client.get("/activities").json()
    assert email in activities_before[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert response.status_code == 200
    
    # Assert
    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity_name]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregister fails for non-existent activity"""
    # Arrange
    fake_activity = "Fake Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{fake_activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_not_registered_returns_400(client):
    """Test that unregister fails for student not in the activity"""
    # Arrange
    activity_name = "Chess Club"
    unregistered_email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={unregistered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_initial_participant(client):
    """Test unregistering an initial participant (from the database)"""
    # Arrange
    activity_name = "Chess Club"
    initial_participant = "michael@mergington.edu"
    
    # Verify initial state
    activities = client.get("/activities").json()
    assert initial_participant in activities[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={initial_participant}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify removal
    activities_after = client.get("/activities").json()
    assert initial_participant not in activities_after[activity_name]["participants"]


def test_unregister_doesnt_affect_other_activities(client):
    """Test that unregistering from one activity doesn't affect others"""
    # Arrange
    email = "multi_activity@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Setup: Register for two activities
    client.post(f"/activities/{activity1}/signup?email={email}")
    client.post(f"/activities/{activity2}/signup?email={email}")
    
    # Act: Unregister from first activity
    response = client.delete(
        f"/activities/{activity1}/unregister?email={email}"
    )
    assert response.status_code == 200
    
    # Assert: Check both activities
    activities = client.get("/activities").json()
    assert email not in activities[activity1]["participants"]
    assert email in activities[activity2]["participants"]


def test_unregister_multiple_times_fails_second_time(client):
    """Test that unregistering twice fails the second time"""
    # Arrange
    activity_name = "Gym Class"
    email = "repeat_unregister@mergington.edu"
    
    # Setup: Signup user
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act - First unregister
    response1 = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert first unregister succeeds
    assert response1.status_code == 200
    
    # Act - Second unregister attempt
    response2 = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert second unregister fails
    assert response2.status_code == 400
    data = response2.json()
    assert "not registered" in data["detail"]
