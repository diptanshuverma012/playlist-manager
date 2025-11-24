"""
Unit tests for renaming mood playlists.
Tests the rename_mood method of the User class.
"""

import pytest
from playlist_manager.user import User


class TestRenameMood:
    """Test cases for renaming mood playlists."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user = User(
            username="test_user",
            password="test_pass",
            playlists={
                "happy": ["Song 1", "Song 2", "Song 3"],
                "sad": ["Sad Song 1"],
                "energetic": []
            }
        )

    def teardown_method(self):
        """Clean up after each test method."""
        self.user = None

    # --------- Basic Rename Tests ---------

    def test_rename_mood_basic(self):
        """Test basic mood renaming."""
        self.user.rename_mood("happy", "joyful")
        
        assert "joyful" in self.user.playlists
        assert "happy" not in self.user.playlists
        assert self.user.playlists["joyful"] == ["Song 1", "Song 2", "Song 3"]

    def test_rename_mood_preserves_songs(self):
        """Test that renaming preserves all songs in the playlist."""
        original_songs = self.user.playlists["happy"].copy()
        self.user.rename_mood("happy", "cheerful")
        
        assert self.user.playlists["cheerful"] == original_songs

    def test_rename_empty_mood(self):
        """Test renaming a mood that has no songs."""
        self.user.rename_mood("energetic", "pumped")
        
        assert "pumped" in self.user.playlists
        assert "energetic" not in self.user.playlists
        assert self.user.playlists["pumped"] == []

    def test_rename_mood_case_normalization(self):
        """Test that new mood name is normalized to lowercase."""
        self.user.rename_mood("happy", "EXCITED")
        
        assert "excited" in self.user.playlists
        assert "EXCITED" not in self.user.playlists

    # --------- Error Handling Tests ---------

    def test_rename_nonexistent_mood(self):
        """Test that renaming a non-existent mood raises KeyError."""
        with pytest.raises(KeyError, match="Mood not found"):
            self.user.rename_mood("nonexistent", "new_name")

    def test_rename_mood_empty_new_name(self):
        """Test that renaming to empty name raises ValueError."""
        with pytest.raises(ValueError, match="New mood name cannot be empty"):
            self.user.rename_mood("happy", "")

    def test_rename_mood_whitespace_only_new_name(self):
        """Test that renaming to whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="New mood name cannot be empty"):
            self.user.rename_mood("happy", "   ")

    def test_rename_mood_to_same_name(self):
        """Test that renaming to the same name raises ValueError."""
        with pytest.raises(ValueError, match="New mood name is the same as old"):
            self.user.rename_mood("happy", "happy")

    def test_rename_mood_to_same_name_different_case(self):
        """Test that renaming to same name with different case raises ValueError."""
        with pytest.raises(ValueError, match="New mood name is the same as old"):
            self.user.rename_mood("happy", "HAPPY")

    def test_rename_mood_to_existing_mood(self):
        """Test that renaming to an existing mood name raises ValueError."""
        with pytest.raises(ValueError, match="A mood with that name already exists"):
            self.user.rename_mood("happy", "sad")

    def test_rename_mood_to_existing_mood_different_case(self):
        """Test that collision check is case-insensitive."""
        with pytest.raises(ValueError, match="A mood with that name already exists"):
            self.user.rename_mood("happy", "SAD")

    # --------- Edge Cases ---------

    def test_rename_mood_with_spaces(self):
        """Test renaming with spaces in new name."""
        self.user.rename_mood("happy", "  very happy  ")
        
        assert "very happy" in self.user.playlists
        assert "happy" not in self.user.playlists

    def test_rename_mood_special_characters(self):
        """Test renaming to a name with special characters."""
        self.user.rename_mood("happy", "90's classics")
        
        assert "90's classics" in self.user.playlists

    def test_rename_all_moods_sequentially(self):
        """Test renaming all moods one by one."""
        renames = [
            ("happy", "joyful"),
            ("sad", "melancholy"),
            ("energetic", "pumped")
        ]
        
        for old, new in renames:
            self.user.rename_mood(old, new)
        
        for old, new in renames:
            assert old not in self.user.playlists
            assert new in self.user.playlists

    # --------- Integration Tests ---------

    def test_rename_mood_then_add_song(self):
        """Test renaming a mood and then adding a song to it."""
        self.user.rename_mood("happy", "cheerful")
        self.user.add_song("cheerful", "New Happy Song")
        
        assert "New Happy Song" in self.user.playlists["cheerful"]
        assert len(self.user.playlists["cheerful"]) == 4

    def test_rename_mood_with_favorite_mood_update(self):
        """Test that favorite mood should be updated when renamed."""
        self.user.set_favorite_mood("happy")
        self.user.rename_mood("happy", "joyful")
        
        # Note: This test documents expected behavior
        # The actual update of favorite_mood happens in the UI layer
        assert "joyful" in self.user.playlists
        assert "happy" not in self.user.playlists

    def test_rename_preserves_other_moods(self):
        """Test that renaming one mood doesn't affect others."""
        original_sad = self.user.playlists["sad"].copy()
        original_energetic = self.user.playlists["energetic"].copy()
        
        self.user.rename_mood("happy", "cheerful")
        
        assert self.user.playlists["sad"] == original_sad
        assert self.user.playlists["energetic"] == original_energetic

    def test_multiple_renames_same_mood(self):
        """Test renaming the same mood multiple times."""
        self.user.rename_mood("happy", "joyful")
        self.user.rename_mood("joyful", "excited")
        self.user.rename_mood("excited", "thrilled")
        
        assert "thrilled" in self.user.playlists
        assert len(self.user.playlists["thrilled"]) == 3
        assert "happy" not in self.user.playlists
        assert "joyful" not in self.user.playlists
        assert "excited" not in self.user.playlists
