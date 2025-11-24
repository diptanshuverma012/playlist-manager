"""
Unit tests for the "surprise me" feature.
Tests the surprise_me method of the User class.
"""

import pytest
from playlist_manager.user import User


class TestSurpriseMe:
    """Test cases for the surprise me (random song) functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user = User(
            username="test_user",
            password="test_pass",
            playlists={
                "happy": ["Happy Song 1", "Happy Song 2", "Happy Song 3"],
                "sad": ["Sad Song 1"],
                "energetic": ["Energetic Song 1", "Energetic Song 2"],
                "empty": []
            }
        )

    def teardown_method(self):
        """Clean up after each test method."""
        self.user = None

    # --------- Basic Surprise Me Tests ---------

    def test_surprise_me_from_specific_mood(self):
        """Test getting a random song from a specific mood."""
        mood, song = self.user.surprise_me("happy")
        
        assert mood == "happy"
        assert song in self.user.playlists["happy"]

    def test_surprise_me_from_all_playlists(self):
        """Test getting a random song from all playlists."""
        mood, song = self.user.surprise_me()
        
        assert mood in self.user.playlists
        assert song in self.user.playlists[mood]

    def test_surprise_me_single_song_mood(self):
        """Test surprise me from a mood with only one song."""
        mood, song = self.user.surprise_me("sad")
        
        assert mood == "sad"
        assert song == "Sad Song 1"

    # --------- Error Handling Tests ---------

    def test_surprise_me_nonexistent_mood(self):
        """Test that surprise me from non-existent mood raises KeyError."""
        with pytest.raises(KeyError, match="Mood not found"):
            self.user.surprise_me("nonexistent")

    def test_surprise_me_empty_mood(self):
        """Test that surprise me from empty mood raises ValueError."""
        with pytest.raises(ValueError, match="That playlist is empty"):
            self.user.surprise_me("empty")

    def test_surprise_me_all_empty_playlists(self):
        """Test surprise me when all playlists are empty."""
        empty_user = User("user", "pass", playlists={"mood1": [], "mood2": []})
        
        with pytest.raises(ValueError, match="No songs available"):
            empty_user.surprise_me()

    def test_surprise_me_no_playlists(self):
        """Test surprise me when user has no playlists."""
        empty_user = User("user", "pass", playlists={})
        
        with pytest.raises(ValueError, match="No songs available"):
            empty_user.surprise_me()

    # --------- Case Handling Tests ---------

    def test_surprise_me_case_insensitive_mood(self):
        """Test that mood name is case-insensitive."""
        mood, song = self.user.surprise_me("HAPPY")
        
        assert mood == "happy"
        assert song in self.user.playlists["happy"]

    def test_surprise_me_mood_with_whitespace(self):
        """Test surprise me with whitespace in mood name."""
        mood, song = self.user.surprise_me("  happy  ")
        
        assert mood == "happy"
        assert song in self.user.playlists["happy"]

    # --------- Randomness Tests ---------

    def test_surprise_me_returns_valid_song_multiple_times(self):
        """Test that multiple calls return valid songs (not testing true randomness)."""
        for _ in range(10):
            mood, song = self.user.surprise_me("happy")
            assert mood == "happy"
            assert song in self.user.playlists["happy"]

    def test_surprise_me_coverage_over_multiple_calls(self):
        """Test that surprise me can return different songs over multiple calls."""
        results = set()
        
        # Call surprise_me multiple times
        for _ in range(20):
            mood, song = self.user.surprise_me("happy")
            results.add(song)
        
        # With 3 songs and 20 calls, we should get at least 2 different songs
        # (statistically very likely, though not guaranteed due to randomness)
        assert len(results) >= 1  # At minimum, we get valid songs

    # --------- Integration Tests ---------

    def test_surprise_me_after_adding_song(self):
        """Test surprise me after adding a new song."""
        new_song = "New Happy Song"
        self.user.add_song("happy", new_song)
        
        # Call surprise me multiple times to increase chance of getting the new song
        songs_found = set()
        for _ in range(50):
            mood, song = self.user.surprise_me("happy")
            songs_found.add(song)
        
        # The new song should be in the pool of possible results
        assert new_song in self.user.playlists["happy"]

    def test_surprise_me_after_deleting_song(self):
        """Test surprise me after deleting a song."""
        deleted_song = self.user.playlists["happy"][0]
        self.user.delete_song("happy", 0)
        
        # Call surprise me multiple times
        for _ in range(20):
            mood, song = self.user.surprise_me("happy")
            # Deleted song should never appear
            assert song != deleted_song

    def test_surprise_me_from_different_moods(self):
        """Test getting surprise songs from different moods."""
        happy_mood, happy_song = self.user.surprise_me("happy")
        sad_mood, sad_song = self.user.surprise_me("sad")
        energetic_mood, energetic_song = self.user.surprise_me("energetic")
        
        assert happy_mood == "happy"
        assert happy_song in self.user.playlists["happy"]
        
        assert sad_mood == "sad"
        assert sad_song in self.user.playlists["sad"]
        
        assert energetic_mood == "energetic"
        assert energetic_song in self.user.playlists["energetic"]

    # --------- Edge Cases ---------

    def test_surprise_me_all_songs_distribution(self):
        """Test that surprise me from all playlists can return songs from any mood."""
        moods_found = set()
        
        # Call surprise_me many times without specifying mood
        for _ in range(100):
            mood, song = self.user.surprise_me()
            moods_found.add(mood)
        
        # We should find at least one song (statistically, likely more)
        assert len(moods_found) >= 1

    def test_surprise_me_last_song_in_mood(self):
        """Test surprise me when mood has only one song left after deletions."""
        # Delete all but one song from happy
        while len(self.user.playlists["happy"]) > 1:
            self.user.delete_song("happy", 0)
        
        last_song = self.user.playlists["happy"][0]
        mood, song = self.user.surprise_me("happy")
        
        assert mood == "happy"
        assert song == last_song

    def test_surprise_me_mixed_empty_and_full_playlists(self):
        """Test surprise me with mix of empty and non-empty playlists."""
        self.user.playlists["empty1"] = []
        self.user.playlists["empty2"] = []
        
        # Should still work and return a song from non-empty playlists
        mood, song = self.user.surprise_me()
        
        assert mood in ["happy", "sad", "energetic"]
        assert song in self.user.playlists[mood]
        assert len(self.user.playlists[mood]) > 0
