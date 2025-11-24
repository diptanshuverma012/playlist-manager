"""
Unit tests for creating mood playlists.
Tests the create_mood method of the User class.
"""

import pytest
from playlist_manager.user import User


class TestCreateMood:
    """Test cases for creating mood playlists."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user = User(
            username="test_user",
            password="test_pass",
            playlists={
                "happy": ["Song 1", "Song 2"],
                "sad": []
            }
        )

    def teardown_method(self):
        """Clean up after each test method."""
        self.user = None

    # --------- Basic Create Mood Tests ---------

    def test_create_new_mood(self):
        """Test creating a new mood playlist."""
        self.user.create_mood("energetic")
        assert "energetic" in self.user.playlists
        assert self.user.playlists["energetic"] == []

    def test_create_mood_with_uppercase(self):
        """Test that mood names are converted to lowercase."""
        self.user.create_mood("CALM")
        assert "calm" in self.user.playlists
        assert "CALM" not in self.user.playlists

    def test_create_mood_with_mixed_case(self):
        """Test that mood names with mixed case are normalized."""
        self.user.create_mood("ReLaXeD")
        assert "relaxed" in self.user.playlists

    def test_create_mood_with_spaces(self):
        """Test creating a mood with spaces in the name."""
        self.user.create_mood("  chill vibes  ")
        assert "chill vibes" in self.user.playlists

    # --------- Error Handling Tests ---------

    def test_create_mood_empty_name(self):
        """Test that creating a mood with empty name raises ValueError."""
        with pytest.raises(ValueError, match="Mood name cannot be empty"):
            self.user.create_mood("")

    def test_create_mood_whitespace_only(self):
        """Test that creating a mood with only whitespace raises ValueError."""
        with pytest.raises(ValueError, match="Mood name cannot be empty"):
            self.user.create_mood("   ")

    def test_create_mood_already_exists(self):
        """Test that creating a duplicate mood raises ValueError."""
        with pytest.raises(ValueError, match="Mood already exists"):
            self.user.create_mood("happy")

    def test_create_mood_duplicate_case_insensitive(self):
        """Test that mood existence check is case-insensitive."""
        with pytest.raises(ValueError, match="Mood already exists"):
            self.user.create_mood("HAPPY")

    # --------- Edge Cases ---------

    def test_create_mood_special_characters(self):
        """Test creating a mood with special characters."""
        self.user.create_mood("90's hits")
        assert "90's hits" in self.user.playlists

    def test_create_mood_with_numbers(self):
        """Test creating a mood with numbers."""
        self.user.create_mood("top100")
        assert "top100" in self.user.playlists

    def test_create_multiple_moods(self):
        """Test creating multiple moods sequentially."""
        moods = ["energetic", "calm", "romantic", "party"]
        for mood in moods:
            self.user.create_mood(mood)
        
        for mood in moods:
            assert mood in self.user.playlists
            assert self.user.playlists[mood] == []

    # --------- Integration Tests ---------

    def test_create_mood_then_add_songs(self):
        """Test creating a mood and then adding songs to it."""
        self.user.create_mood("workout")
        assert "workout" in self.user.playlists
        
        self.user.add_song("workout", "Pump It Up")
        self.user.add_song("workout", "Eye of the Tiger")
        
        assert len(self.user.playlists["workout"]) == 2
        assert "Pump It Up" in self.user.playlists["workout"]

    def test_create_mood_on_empty_user(self):
        """Test creating a mood for a user with no existing playlists."""
        empty_user = User("new_user", "pass", playlists={})
        empty_user.create_mood("first_mood")
        
        assert "first_mood" in empty_user.playlists
        assert len(empty_user.playlists) == 1

    def test_create_mood_preserve_existing(self):
        """Test that creating a new mood doesn't affect existing moods."""
        original_happy = self.user.playlists["happy"].copy()
        original_sad = self.user.playlists["sad"].copy()
        
        self.user.create_mood("new_mood")
        
        # Verify existing moods are unchanged
        assert self.user.playlists["happy"] == original_happy
        assert self.user.playlists["sad"] == original_sad
        assert "new_mood" in self.user.playlists
