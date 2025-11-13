"""
Test cases for renaming moods/playlists
"""

import pytest
from playlist_manager.user import User


def test_rename_mood_success(test_user):
    """Test successfully renaming a mood."""
    songs_before = test_user.playlists["happy"].copy()
    test_user.rename_mood("happy", "joyful")

    assert "happy" not in test_user.playlists
    assert "joyful" in test_user.playlists
    assert test_user.playlists["joyful"] == songs_before


def test_rename_mood_preserves_songs(test_user):
    """Test that renaming a mood preserves all songs."""
    original_songs = test_user.playlists["energetic"].copy()
    test_user.rename_mood("energetic", "pumped")

    assert test_user.playlists["pumped"] == original_songs
    assert len(test_user.playlists["pumped"]) == len(original_songs)


def test_rename_mood_case_insensitive_source(test_user):
    """Test that source mood name is case-insensitive."""
    test_user.rename_mood("HAPPY", "joyful")
    assert "happy" not in test_user.playlists
    assert "joyful" in test_user.playlists


def test_rename_mood_case_insensitive_target(test_user):
    """Test that target mood name is normalized to lowercase."""
    test_user.rename_mood("happy", "JOYFUL")
    assert "joyful" in test_user.playlists


def test_rename_mood_nonexistent(test_user):
    """Test that renaming a non-existent mood raises KeyError."""
    with pytest.raises(KeyError, match="Mood not found"):
        test_user.rename_mood("nonexistent", "newname")


def test_rename_mood_empty_new_name(test_user):
    """Test that renaming to empty name raises ValueError."""
    with pytest.raises(ValueError, match="New mood name cannot be empty"):
        test_user.rename_mood("happy", "")


def test_rename_mood_whitespace_new_name(test_user):
    """Test that renaming to whitespace-only name raises ValueError."""
    with pytest.raises(ValueError, match="New mood name cannot be empty"):
        test_user.rename_mood("happy", "   ")


def test_rename_mood_same_name(test_user):
    """Test that renaming to the same name raises ValueError."""
    with pytest.raises(ValueError, match="New mood name is the same as old"):
        test_user.rename_mood("happy", "happy")


def test_rename_mood_same_name_different_case(test_user):
    """Test that renaming to same name with different case raises ValueError."""
    with pytest.raises(ValueError, match="New mood name is the same as old"):
        test_user.rename_mood("happy", "HAPPY")


def test_rename_mood_to_existing(test_user):
    """Test that renaming to an existing mood name raises ValueError."""
    with pytest.raises(ValueError, match="A mood with that name already exists"):
        test_user.rename_mood("happy", "sad")


def test_rename_mood_to_existing_different_case(test_user):
    """Test that duplicate detection is case-insensitive."""
    with pytest.raises(ValueError, match="A mood with that name already exists"):
        test_user.rename_mood("happy", "SAD")


def test_rename_mood_with_spaces(test_user):
    """Test renaming with leading/trailing spaces."""
    test_user.rename_mood("  happy  ", "  joyful  ")
    assert "happy" not in test_user.playlists
    assert "joyful" in test_user.playlists


def test_rename_multiple_moods(test_user):
    """Test renaming multiple moods in sequence."""
    test_user.rename_mood("happy", "joyful")
    test_user.rename_mood("sad", "melancholy")
    test_user.rename_mood("energetic", "pumped")

    assert "joyful" in test_user.playlists
    assert "melancholy" in test_user.playlists
    assert "pumped" in test_user.playlists
    assert "happy" not in test_user.playlists
    assert "sad" not in test_user.playlists
    assert "energetic" not in test_user.playlists


def test_rename_mood_chain(test_user):
    """Test renaming a mood multiple times."""
    original_songs = test_user.playlists["happy"].copy()

    test_user.rename_mood("happy", "joyful")
    test_user.rename_mood("joyful", "cheerful")
    test_user.rename_mood("cheerful", "upbeat")

    assert "upbeat" in test_user.playlists
    assert test_user.playlists["upbeat"] == original_songs
    assert "happy" not in test_user.playlists
    assert "joyful" not in test_user.playlists
    assert "cheerful" not in test_user.playlists


def test_rename_mood_empty_playlist(empty_user):
    """Test renaming a mood with an empty playlist."""
    empty_user.rename_mood("happy", "joyful")
    assert "joyful" in empty_user.playlists
    assert empty_user.playlists["joyful"] == []


def test_rename_mood_special_characters(test_user):
    """Test renaming to a name with special characters."""
    test_user.rename_mood("happy", "super-happy")
    assert "super-happy" in test_user.playlists


def test_rename_mood_affects_favorite(test_user):
    """Test that renaming a favorite mood should be handled by caller."""
    test_user.set_favorite_mood("happy")
    test_user.rename_mood("happy", "joyful")

    # The rename itself doesn't update favorite_mood
    # This should be handled by the UI layer
    assert test_user.favorite_mood == "happy"  # Still points to old name
    assert "happy" not in test_user.playlists
    assert "joyful" in test_user.playlists
