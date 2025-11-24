"""
Test cases for searching songs in playlists
"""

import pytest
from playlist_manager.user import User


def test_search_song_found(test_user):
    """Test searching for a song that exists."""
    test_user.add_song("happy", "Test Search Song")
    results = test_user.search_song("Test Search")

    assert len(results) > 0
    assert any(song == "Test Search Song" for mood, song in results)


def test_search_song_case_insensitive(test_user):
    """Test that search is case-insensitive."""
    test_user.add_song("happy", "Happy Song Test")
    results = test_user.search_song("happy song test")

    assert len(results) > 0
    assert any("Happy Song Test" in song for mood, song in results)


def test_search_song_partial_match(test_user):
    """Test searching with partial keyword."""
    test_user.add_song("happy", "Beautiful Day")
    results = test_user.search_song("beautiful")

    assert len(results) > 0
    assert any("Beautiful Day" in song for mood, song in results)


def test_search_song_multiple_results(test_user):
    """Test searching returns multiple matching songs."""
    test_user.add_song("happy", "Happy Test 1")
    test_user.add_song("sad", "Happy Test 2")
    test_user.add_song("calm", "Test Happy 3")

    results = test_user.search_song("Test")

    assert len(results) >= 3
    song_names = [song for mood, song in results]
    assert "Happy Test 1" in song_names
    assert "Happy Test 2" in song_names
    assert "Test Happy 3" in song_names


def test_search_song_no_results(test_user):
    """Test searching for a song that doesn't exist."""
    results = test_user.search_song("NonexistentSong12345")
    assert len(results) == 0


def test_search_song_empty_keyword(test_user):
    """Test searching with empty keyword returns all songs."""
    results = test_user.search_song("")
    # Empty string matches all songs (substring of everything)
    total_songs = sum(len(songs) for songs in test_user.playlists.values())
    assert len(results) == total_songs


def test_search_song_whitespace_keyword(test_user):
    """Test searching with whitespace keyword."""
    results = test_user.search_song("   ")
    # Whitespace should be stripped, becoming empty, matching all songs
    total_songs = sum(len(songs) for songs in test_user.playlists.values())
    assert len(results) == total_songs


def test_search_song_returns_mood_info(test_user):
    """Test that search results include mood information."""
    test_user.add_song("happy", "Unique Search Song")
    results = test_user.search_song("Unique Search")

    assert len(results) > 0
    mood, song = results[0]
    assert mood == "happy"
    assert song == "Unique Search Song"


def test_search_song_across_multiple_moods(test_user):
    """Test searching finds songs across different moods."""
    test_user.add_song("happy", "Love Song")
    test_user.add_song("sad", "Love Ballad")
    test_user.add_song("calm", "Lovely Day")

    results = test_user.search_song("love")

    assert len(results) == 3
    moods = [mood for mood, song in results]
    assert "happy" in moods
    assert "sad" in moods
    assert "calm" in moods


def test_search_song_special_characters(test_user):
    """Test searching with special characters."""
    test_user.add_song("happy", "Song - With Dashes")
    results = test_user.search_song("dashes")

    assert len(results) > 0
    assert any("Song - With Dashes" in song for mood, song in results)


def test_search_song_numeric(test_user):
    """Test searching for numeric values in song names."""
    test_user.add_song("happy", "Song 123")
    results = test_user.search_song("123")

    assert len(results) > 0
    assert any("Song 123" in song for mood, song in results)


def test_search_song_empty_playlists(empty_user):
    """Test searching in empty playlists returns no results."""
    results = empty_user.search_song("anything")
    assert len(results) == 0


def test_search_song_substring_anywhere(test_user):
    """Test that search matches substring anywhere in song name."""
    test_user.add_song("happy", "The Best Song Ever")

    # Search for middle word
    results = test_user.search_song("best")
    assert len(results) > 0

    # Search for last word
    results = test_user.search_song("ever")
    assert len(results) > 0

    # Search for first word
    results = test_user.search_song("the")
    assert len(results) > 0


def test_search_song_default_playlists(test_user):
    """Test searching in default playlists."""
    # Search for songs that exist in default playlists
    results = test_user.search_song("song")

    # Should find songs containing "song" in default playlists
    assert len(results) > 0


def test_search_song_with_spaces_in_song_name(test_user):
    """Test searching for songs with multiple spaces."""
    test_user.add_song("happy", "Multi  Space  Song")
    results = test_user.search_song("multi")

    assert len(results) > 0
    assert any("Multi  Space  Song" in song for mood, song in results)
