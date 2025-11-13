"""
Test cases for surprise me feature (random song selection)
"""

import pytest
from playlist_manager.user import User


def test_surprise_me_from_specific_mood(test_user):
    """Test getting a random song from a specific mood."""
    mood, song = test_user.surprise_me("happy")

    assert mood == "happy"
    assert song in test_user.playlists["happy"]


def test_surprise_me_from_all_moods(test_user):
    """Test getting a random song from all playlists."""
    mood, song = test_user.surprise_me()

    assert mood in test_user.playlists
    assert song in test_user.playlists[mood]


def test_surprise_me_case_insensitive(test_user):
    """Test that mood name is case-insensitive."""
    mood, song = test_user.surprise_me("HAPPY")

    assert mood == "happy"
    assert song in test_user.playlists["happy"]


def test_surprise_me_nonexistent_mood(test_user):
    """Test that surprise from non-existent mood raises KeyError."""
    with pytest.raises(KeyError, match="Mood not found"):
        test_user.surprise_me("nonexistent")


def test_surprise_me_empty_mood(empty_user):
    """Test that surprise from empty mood raises ValueError."""
    with pytest.raises(ValueError, match="That playlist is empty"):
        empty_user.surprise_me("happy")


def test_surprise_me_empty_all_playlists(empty_user):
    """Test that surprise from all empty playlists raises ValueError."""
    with pytest.raises(ValueError, match="No songs available"):
        empty_user.surprise_me()


def test_surprise_me_single_song(test_user):
    """Test surprise when mood has only one song."""
    # Create a mood with single song
    test_user.create_mood("single")
    test_user.add_song("single", "Only Song")

    mood, song = test_user.surprise_me("single")

    assert mood == "single"
    assert song == "Only Song"


def test_surprise_me_returns_valid_song(test_user):
    """Test that surprise always returns a valid song from the mood."""
    # Run multiple times to ensure randomness works
    for _ in range(10):
        mood, song = test_user.surprise_me("energetic")
        assert mood == "energetic"
        assert song in test_user.playlists["energetic"]


def test_surprise_me_all_playlists_returns_valid_song(test_user):
    """Test that surprise from all playlists returns valid songs."""
    # Run multiple times to check different possibilities
    for _ in range(10):
        mood, song = test_user.surprise_me()
        assert mood in test_user.playlists
        assert song in test_user.playlists[mood]


def test_surprise_me_with_spaces_in_mood(test_user):
    """Test surprise with mood name containing spaces."""
    mood, song = test_user.surprise_me("  happy  ")
    assert mood == "happy"


def test_surprise_me_distribution(test_user):
    """Test that surprise has some randomness (not always same song)."""
    # For a mood with multiple songs, we should get different ones eventually
    results = set()
    for _ in range(20):
        mood, song = test_user.surprise_me("happy")
        results.add(song)

    # With 3+ songs and 20 attempts, we should get at least 2 different songs
    # (statistically very likely)
    assert len(results) >= 2


def test_surprise_me_after_adding_songs(test_user):
    """Test surprise after adding new songs."""
    test_user.add_song("happy", "Brand New Song")
    mood, song = test_user.surprise_me("happy")

    assert mood == "happy"
    assert song in test_user.playlists["happy"]


def test_surprise_me_after_deleting_songs(test_user):
    """Test surprise after deleting songs."""
    songs_before = test_user.playlists["sad"].copy()
    test_user.delete_song("sad", 0)

    mood, song = test_user.surprise_me("sad")

    assert mood == "sad"
    assert song in test_user.playlists["sad"]
    assert song in songs_before[1:]  # Should be from remaining songs


def test_surprise_me_mixed_empty_and_full_moods():
    """Test surprise from all playlists when some are empty."""
    user = User(
        "test",
        "pass",
        playlists={
            "empty1": [],
            "filled": ["Song 1", "Song 2"],
            "empty2": []
        }
    )

    mood, song = user.surprise_me()

    assert mood == "filled"
    assert song in ["Song 1", "Song 2"]


def test_surprise_me_multiple_moods_all_access():
    """Test that surprise can access songs from any mood."""
    user = User(
        "test",
        "pass",
        playlists={
            "mood1": ["Song A"],
            "mood2": ["Song B"],
            "mood3": ["Song C"]
        }
    )

    # Collect results from multiple attempts
    found_moods = set()
    for _ in range(30):
        mood, song = user.surprise_me()
        found_moods.add(mood)

    # With 30 attempts and 3 moods, we should hit at least 2 different moods
    assert len(found_moods) >= 2


def test_surprise_me_none_mood_parameter():
    """Test calling surprise_me with None explicitly."""
    user = User(
        "test",
        "pass",
        playlists={
            "happy": ["Song 1", "Song 2"]
        }
    )

    mood, song = user.surprise_me(None)
    assert mood == "happy"
    assert song in ["Song 1", "Song 2"]
