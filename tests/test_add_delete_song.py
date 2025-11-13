"""
Test cases for adding and deleting songs from playlists
"""

import pytest
from playlist_manager.user import User


def test_add_song_success(test_user):
    """Test successfully adding a song to a mood."""
    initial_count = len(test_user.playlists["happy"])
    test_user.add_song("happy", "New Happy Song")

    assert len(test_user.playlists["happy"]) == initial_count + 1
    assert "New Happy Song" in test_user.playlists["happy"]


def test_add_song_case_insensitive(test_user):
    """Test adding a song is case-insensitive."""
    test_user.add_song("HAPPY", "Another Song")
    assert "Another Song" in test_user.playlists["happy"]


def test_add_song_duplicate(test_user):
    """Test that adding a duplicate song raises ValueError."""
    test_user.add_song("happy", "Unique Song")

    with pytest.raises(ValueError, match="Song already exists"):
        test_user.add_song("happy", "Unique Song")


def test_add_song_duplicate_case_insensitive(test_user):
    """Test that duplicate detection is case-insensitive."""
    test_user.add_song("happy", "Test Song")

    with pytest.raises(ValueError, match="Song already exists"):
        test_user.add_song("happy", "test song")


def test_add_song_empty_name(test_user):
    """Test that adding an empty song name raises ValueError."""
    with pytest.raises(ValueError, match="Song name cannot be empty"):
        test_user.add_song("happy", "")


def test_add_song_nonexistent_mood(test_user):
    """Test that adding to a non-existent mood raises KeyError."""
    with pytest.raises(KeyError, match="Mood not found"):
        test_user.add_song("nonexistent", "Some Song")


def test_delete_song_success(test_user):
    """Test successfully deleting a song from a mood."""
    initial_count = len(test_user.playlists["happy"])
    removed_song = test_user.delete_song("happy", 0)

    assert len(test_user.playlists["happy"]) == initial_count - 1
    assert removed_song not in test_user.playlists["happy"]


def test_delete_song_by_index(test_user):
    """Test deleting a specific song by index."""
    songs_before = test_user.playlists["happy"].copy()
    removed = test_user.delete_song("happy", 1)

    assert removed == songs_before[1]
    assert removed not in test_user.playlists["happy"]


def test_delete_song_invalid_index(test_user):
    """Test that deleting with invalid index raises IndexError."""
    with pytest.raises(IndexError):
        test_user.delete_song("happy", 999)


def test_delete_song_negative_index(test_user):
    """Test deleting with negative index (Python allows this)."""
    last_song = test_user.playlists["happy"][-1]
    removed = test_user.delete_song("happy", -1)

    assert removed == last_song
    assert removed not in test_user.playlists["happy"]


def test_delete_song_nonexistent_mood(test_user):
    """Test that deleting from non-existent mood raises KeyError."""
    with pytest.raises(KeyError, match="Mood not found"):
        test_user.delete_song("nonexistent", 0)


def test_delete_song_empty_playlist(empty_user):
    """Test deleting from an empty playlist raises IndexError."""
    with pytest.raises(IndexError):
        empty_user.delete_song("happy", 0)


def test_add_multiple_songs(test_user):
    """Test adding multiple songs in sequence."""
    initial_count = len(test_user.playlists["calm"])
    songs_to_add = ["Song A", "Song B", "Song C"]

    for song in songs_to_add:
        test_user.add_song("calm", song)

    assert len(test_user.playlists["calm"]) == initial_count + len(songs_to_add)
    for song in songs_to_add:
        assert song in test_user.playlists["calm"]


def test_delete_all_songs(test_user):
    """Test deleting all songs from a playlist."""
    mood = "sad"
    while test_user.playlists[mood]:
        test_user.delete_song(mood, 0)

    assert len(test_user.playlists[mood]) == 0


def test_add_after_delete(test_user):
    """Test adding a song after deleting one."""
    test_user.delete_song("happy", 0)
    test_user.add_song("happy", "Replacement Song")

    assert "Replacement Song" in test_user.playlists["happy"]
