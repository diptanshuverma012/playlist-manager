"""
Unit tests for adding and deleting songs functionality.
Tests the add_song and delete_song methods of the User class.
"""

import pytest
from playlist_manager.user import User


class TestAddDeleteSong:
    """Test cases for adding and deleting songs from playlists."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user = User(
            username="test_user",
            password="test_pass",
            playlists={
                "happy": ["Song 1", "Song 2"],
                "sad": ["Sad Song 1"],
                "empty": []
            }
        )

    def teardown_method(self):
        """Clean up after each test method."""
        self.user = None

    # --------- Add Song Tests ---------
    
    def test_add_song_to_existing_mood(self):
        """Test adding a song to an existing mood."""
        self.user.add_song("happy", "New Happy Song")
        assert "New Happy Song" in self.user.playlists["happy"]
        assert len(self.user.playlists["happy"]) == 3

    def test_add_song_to_empty_playlist(self):
        """Test adding a song to an empty playlist."""
        self.user.add_song("empty", "First Song")
        assert "First Song" in self.user.playlists["empty"]
        assert len(self.user.playlists["empty"]) == 1

    def test_add_song_case_insensitive_duplicate(self):
        """Test that adding a duplicate song (case-insensitive) raises ValueError."""
        with pytest.raises(ValueError, match="Song already exists"):
            self.user.add_song("happy", "song 1")  # lowercase version of "Song 1"

    def test_add_song_empty_name(self):
        """Test that adding a song with empty name raises ValueError."""
        with pytest.raises(ValueError, match="Song name cannot be empty"):
            self.user.add_song("happy", "")

    def test_add_song_whitespace_only_name(self):
        """Test that adding a song with only whitespace raises ValueError."""
        with pytest.raises(ValueError, match="Song name cannot be empty"):
            self.user.add_song("happy", "   ")

    def test_add_song_to_nonexistent_mood(self):
        """Test that adding a song to non-existent mood raises KeyError."""
        with pytest.raises(KeyError, match="Mood not found"):
            self.user.add_song("nonexistent", "Some Song")

    # --------- Delete Song Tests ---------

    def test_delete_song_by_valid_index(self):
        """Test deleting a song by valid index."""
        removed = self.user.delete_song("happy", 0)
        assert removed == "Song 1"
        assert "Song 1" not in self.user.playlists["happy"]
        assert len(self.user.playlists["happy"]) == 1

    def test_delete_last_song_in_playlist(self):
        """Test deleting the last song in a playlist."""
        removed = self.user.delete_song("sad", 0)
        assert removed == "Sad Song 1"
        assert len(self.user.playlists["sad"]) == 0

    def test_delete_song_valid_negative_index(self):
        """Test that deleting with negative index works (Python feature)."""
        # Negative indexing is valid in Python, -1 refers to last element
        removed = self.user.delete_song("happy", -1)
        assert removed == "Song 2"  # Last song in the list
        assert len(self.user.playlists["happy"]) == 1

    def test_delete_song_invalid_index_too_large(self):
        """Test that deleting with out-of-range index raises IndexError."""
        with pytest.raises(IndexError):
            self.user.delete_song("happy", 10)

    def test_delete_song_from_nonexistent_mood(self):
        """Test that deleting from non-existent mood raises KeyError."""
        with pytest.raises(KeyError, match="Mood not found"):
            self.user.delete_song("nonexistent", 0)

    def test_delete_song_from_empty_playlist(self):
        """Test that deleting from empty playlist raises IndexError."""
        with pytest.raises(IndexError):
            self.user.delete_song("empty", 0)

    # --------- Integration Tests ---------

    def test_add_then_delete_song(self):
        """Test adding a song and then deleting it."""
        self.user.add_song("happy", "Temporary Song")
        assert "Temporary Song" in self.user.playlists["happy"]
        
        # Find and delete the song
        index = self.user.playlists["happy"].index("Temporary Song")
        removed = self.user.delete_song("happy", index)
        
        assert removed == "Temporary Song"
        assert "Temporary Song" not in self.user.playlists["happy"]

    def test_multiple_add_delete_operations(self):
        """Test multiple add and delete operations."""
        initial_count = len(self.user.playlists["happy"])
        
        # Add three songs
        self.user.add_song("happy", "Song A")
        self.user.add_song("happy", "Song B")
        self.user.add_song("happy", "Song C")
        
        assert len(self.user.playlists["happy"]) == initial_count + 3
        
        # Delete two songs
        self.user.delete_song("happy", -1)  # Delete last
        self.user.delete_song("happy", -1)  # Delete last again
        
        assert len(self.user.playlists["happy"]) == initial_count + 1
        assert "Song A" in self.user.playlists["happy"]
