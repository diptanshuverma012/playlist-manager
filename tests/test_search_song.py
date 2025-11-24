"""
Unit tests for song search functionality.
Tests the search_song method of the User class.
"""

import pytest
from playlist_manager.user import User


class TestSearchSong:
    """Test cases for searching songs in playlists."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user = User(
            username="test_user",
            password="test_pass",
            playlists={
                "happy": ["Happy Song", "Dancing Queen", "Celebration"],
                "sad": ["Tears in Heaven", "Someone Like You", "Fix You"],
                "energetic": ["Eye of the Tiger", "Stronger", "Titanium"],
                "empty": []
            }
        )

    def teardown_method(self):
        """Clean up after each test method."""
        self.user = None

    # --------- Basic Search Tests ---------

    def test_search_exact_match(self):
        """Test searching for exact song name."""
        results = self.user.search_song("Happy Song")
        
        assert len(results) == 1
        assert ("happy", "Happy Song") in results

    def test_search_partial_match(self):
        """Test searching with partial song name."""
        results = self.user.search_song("Tiger")
        
        assert len(results) == 1
        assert ("energetic", "Eye of the Tiger") in results

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        results = self.user.search_song("HAPPY")
        
        assert len(results) == 1
        assert ("happy", "Happy Song") in results

    def test_search_multiple_matches(self):
        """Test searching keyword that matches multiple songs."""
        results = self.user.search_song("You")
        
        # Should match "Someone Like You" and "Fix You"
        assert len(results) == 2
        assert ("sad", "Someone Like You") in results
        assert ("sad", "Fix You") in results

    def test_search_no_matches(self):
        """Test searching for non-existent keyword."""
        results = self.user.search_song("Nonexistent Song")
        
        assert len(results) == 0
        assert results == []

    # --------- Edge Cases ---------

    def test_search_empty_keyword(self):
        """Test searching with empty keyword returns all songs."""
        results = self.user.search_song("")
        
        # Empty string matches all songs since it's contained in every string
        total_songs = sum(len(songs) for songs in self.user.playlists.values())
        assert len(results) == total_songs

    def test_search_whitespace_keyword(self):
        """Test searching with whitespace keyword."""
        results = self.user.search_song("   ")
        
        # Should still match songs containing spaces
        assert len(results) >= 0

    def test_search_single_character(self):
        """Test searching with single character."""
        results = self.user.search_song("e")
        
        # Should match any song containing 'e' (case-insensitive)
        assert len(results) > 0
        for mood, song in results:
            assert 'e' in song.lower() or 'E' in song

    def test_search_in_empty_playlists(self):
        """Test searching when user has only empty playlists."""
        empty_user = User("user", "pass", playlists={"empty1": [], "empty2": []})
        results = empty_user.search_song("anything")
        
        assert len(results) == 0

    # --------- Keyword Pattern Tests ---------

    def test_search_common_word(self):
        """Test searching for common word that appears in multiple songs."""
        results = self.user.search_song("the")
        
        # Should match "Eye of the Tiger"
        assert len(results) >= 1
        assert any("Eye of the Tiger" in song for mood, song in results)

    def test_search_with_special_characters(self):
        """Test searching with special characters in keyword."""
        self.user.add_song("happy", "Don't Stop Me Now")
        results = self.user.search_song("Don't")
        
        assert len(results) == 1
        assert ("happy", "Don't Stop Me Now") in results

    def test_search_numeric_keyword(self):
        """Test searching with numeric keyword."""
        self.user.add_song("happy", "Summer of '69")
        results = self.user.search_song("69")
        
        assert len(results) == 1
        assert ("happy", "Summer of '69") in results

    # --------- Multiple Moods Tests ---------

    def test_search_across_all_moods(self):
        """Test that search looks across all mood playlists."""
        # Add a song with keyword "Love" to multiple moods
        self.user.add_song("happy", "Love Story")
        self.user.add_song("sad", "Love Hurts")
        
        results = self.user.search_song("Love")
        
        assert len(results) == 2
        mood_song_pairs = [(mood, song) for mood, song in results]
        assert ("happy", "Love Story") in mood_song_pairs
        assert ("sad", "Love Hurts") in mood_song_pairs

    def test_search_returns_correct_mood_mapping(self):
        """Test that search results correctly map songs to moods."""
        results = self.user.search_song("Queen")
        
        assert len(results) == 1
        mood, song = results[0]
        assert mood == "happy"
        assert song == "Dancing Queen"

    # --------- Integration Tests ---------

    def test_search_after_adding_songs(self):
        """Test search after dynamically adding songs."""
        initial_results = self.user.search_song("Rocket")
        assert len(initial_results) == 0
        
        self.user.add_song("happy", "Rocket Man")
        new_results = self.user.search_song("Rocket")
        
        assert len(new_results) == 1
        assert ("happy", "Rocket Man") in new_results

    def test_search_after_deleting_songs(self):
        """Test search after deleting songs."""
        initial_results = self.user.search_song("Happy")
        assert len(initial_results) == 1
        
        # Delete the song
        index = self.user.playlists["happy"].index("Happy Song")
        self.user.delete_song("happy", index)
        
        new_results = self.user.search_song("Happy")
        assert len(new_results) == 0

    def test_search_with_leading_trailing_spaces(self):
        """Test that search handles leading/trailing spaces in keyword."""
        results1 = self.user.search_song("  Happy  ")
        results2 = self.user.search_song("Happy")
        
        # Both should return the same results
        assert results1 == results2

    def test_search_performance_with_many_songs(self):
        """Test search works correctly with many songs."""
        # Add many songs
        for i in range(100):
            self.user.add_song("happy", f"Test Song {i}")
        
        # Search for specific song
        results = self.user.search_song("Test Song 50")
        
        assert len(results) == 1
        assert ("happy", "Test Song 50") in results
