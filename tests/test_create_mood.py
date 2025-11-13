"""
Test cases for creating new moods/playlists
"""

import pytest
from playlist_manager.user import User


def test_create_mood_success(test_user):
    """Test successfully creating a new mood."""
    initial_count = len(test_user.playlists)
    test_user.create_mood("excited")

    assert len(test_user.playlists) == initial_count + 1
    assert "excited" in test_user.playlists
    assert test_user.playlists["excited"] == []


def test_create_mood_case_insensitive(test_user):
    """Test that mood creation is case-insensitive."""
    test_user.create_mood("RELAXED")
    assert "relaxed" in test_user.playlists


def test_create_mood_with_spaces(test_user):
    """Test creating a mood with leading/trailing spaces."""
    test_user.create_mood("  peaceful  ")
    assert "peaceful" in test_user.playlists


def test_create_mood_empty_name(test_user):
    """Test that creating a mood with empty name raises ValueError."""
    with pytest.raises(ValueError, match="Mood name cannot be empty"):
        test_user.create_mood("")


def test_create_mood_whitespace_only(test_user):
    """Test that creating a mood with only whitespace raises ValueError."""
    with pytest.raises(ValueError, match="Mood name cannot be empty"):
        test_user.create_mood("   ")


def test_create_mood_duplicate(test_user):
    """Test that creating a duplicate mood raises ValueError."""
    with pytest.raises(ValueError, match="Mood already exists"):
        test_user.create_mood("happy")


def test_create_mood_duplicate_case_insensitive(test_user):
    """Test that duplicate detection is case-insensitive."""
    with pytest.raises(ValueError, match="Mood already exists"):
        test_user.create_mood("HAPPY")


def test_create_multiple_moods(test_user):
    """Test creating multiple moods in sequence."""
    moods_to_create = ["excited", "nostalgic", "romantic"]
    initial_count = len(test_user.playlists)

    for mood in moods_to_create:
        test_user.create_mood(mood)

    assert len(test_user.playlists) == initial_count + len(moods_to_create)
    for mood in moods_to_create:
        assert mood in test_user.playlists
        assert test_user.playlists[mood] == []


def test_create_mood_then_add_songs(test_user):
    """Test creating a mood and then adding songs to it."""
    test_user.create_mood("focused")
    test_user.add_song("focused", "Focus Song 1")
    test_user.add_song("focused", "Focus Song 2")

    assert "focused" in test_user.playlists
    assert len(test_user.playlists["focused"]) == 2
    assert "Focus Song 1" in test_user.playlists["focused"]
    assert "Focus Song 2" in test_user.playlists["focused"]


def test_create_mood_special_characters(test_user):
    """Test creating a mood with special characters."""
    test_user.create_mood("chill-out")
    assert "chill-out" in test_user.playlists


def test_create_mood_numeric_name(test_user):
    """Test creating a mood with numeric name."""
    test_user.create_mood("90s")
    assert "90s" in test_user.playlists


def test_create_mood_empty_user(empty_user):
    """Test creating a mood for a user with minimal playlists."""
    empty_user.create_mood("newmood")
    assert "newmood" in empty_user.playlists
    assert empty_user.playlists["newmood"] == []


def test_create_mood_initialization():
    """Test that a new user starts with no moods if not provided."""
    user = User("test", "pass", playlists={})
    assert len(user.playlists) == 0

    user.create_mood("first")
    assert len(user.playlists) == 1
    assert "first" in user.playlists
