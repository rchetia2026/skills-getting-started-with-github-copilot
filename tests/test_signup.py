"""Tests for the signup endpoint using AAA pattern"""

import pytest


def test_signup_for_activity_success(client):
    """Test successful registration for an activity"""
    # Arrange
    activity_name = "Chess Club"
    new_student_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_student_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up" in data["message"]
    assert new_student_email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity"""
    # Arrange
    activity_name = "Programming Class"
    new_email = "alice@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was added by fetching activities
    activities = client.get("/activities").json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup fails for non-existent activity"""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    student_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup?email={student_email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email_returns_400(client):
    """Test that duplicate signup is rejected"""
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "bob@mergington.edu"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )
    assert response1.status_code == 200
    
    # Act - Attempt duplicate signup
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )
    
    # Assert
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_with_special_characters_in_email(client):
    """Test signup with email containing special characters"""
    # Arrange
    activity_name = "Gym Class"
    special_email = "student+tag@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={special_email}"
    )
    
    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert special_email in activities[activity_name]["participants"]


def test_signup_multiple_students_same_activity(client):
    """Test that multiple different students can register for the same activity"""
    # Arrange
    activity_name = "Art Studio"
    students = ["student1@mergington.edu", "student2@mergington.edu"]
    
    # Act
    for student_email in students:
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        assert response.status_code == 200
    
    # Assert
    activities = client.get("/activities").json()
    participants = activities[activity_name]["participants"]
    for student_email in students:
        assert student_email in participants


def test_signup_different_activities_same_student(client):
    """Test that same student can register for different activities"""
    # Arrange
    student_email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class"]
    
    # Act
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        assert response.status_code == 200
    
    # Assert
    activities = client.get("/activities").json()
    for activity_name in activities_to_join:
        assert student_email in activities[activity_name]["participants"]
