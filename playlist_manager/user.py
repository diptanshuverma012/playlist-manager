"""
User module for Playlist Manager.
Contains User class and authentication-related functionality.
"""

import random
import csv
import json
import logging

logger = logging.getLogger(__name__)


class User:
    """
    Represents a user with username, password, playlists, and a favorite mood.
    All playlist operations are provided as methods.
    """

    def __init__(self, username: str, password: str, playlists=None, favorite_mood=None):
        """
        Initialize a User object.
        
        Args:
            username: User's unique username
            password: User's password
            playlists: dict mapping mood -> list of songs (default: None)
            favorite_mood: optional string with the user's favorite mood (default: None)
        """
        self.username = username
        self.password = password
        self.playlists = playlists if playlists is not None else {}
        self.favorite_mood = favorite_mood

    # -------------------------
    # Playlist operations (methods)
    # -------------------------
    def create_mood(self, mood_name: str):
        """
        Create a new mood/playlist if it doesn't exist.
        
        Args:
            mood_name: Name of the mood to create
        
        Raises:
            ValueError: If mood name is empty or already exists
        """
        mood = mood_name.strip().lower()
        if not mood:
            logger.error("Attempted to create mood with empty name")
            raise ValueError("Mood name cannot be empty.")
        if mood in self.playlists:
            logger.error(f"Mood '{mood}' already exists")
            raise ValueError("Mood already exists.")
        self.playlists[mood] = []
        logger.info(f"Created new mood: {mood}")

    def add_song(self, mood_name: str, song_name: str):
        """
        Add a song to a mood; prevents case-insensitive duplicates.
        
        Args:
            mood_name: Mood to add the song to
            song_name: Name of the song to add
        
        Raises:
            KeyError: If mood doesn't exist
            ValueError: If song name is empty or already exists in playlist
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            logger.error(f"Mood '{mood}' not found")
            raise KeyError("Mood not found.")
        song = song_name.strip()
        if not song:
            logger.error("Attempted to add song with empty name")
            raise ValueError("Song name cannot be empty.")
        existing_lower = [s.lower() for s in self.playlists[mood]]
        if song.lower() in existing_lower:
            logger.error(f"Song '{song}' already exists in '{mood}' playlist")
            raise ValueError("Song already exists in playlist.")
        self.playlists[mood].append(song)
        logger.info(f"Added song '{song}' to mood '{mood}'")

    def delete_song(self, mood_name: str, index: int):
        """
        Delete a song by index (0-based) from a mood.
        
        Args:
            mood_name: Mood to delete the song from
            index: 0-based index of the song to delete
        
        Returns:
            str: Name of the deleted song
        
        Raises:
            KeyError: If mood doesn't exist
            IndexError: If index is out of range
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            logger.error(f"Mood '{mood}' not found")
            raise KeyError("Mood not found.")
        try:
            removed = self.playlists[mood].pop(index)
            logger.info(f"Deleted song '{removed}' from mood '{mood}'")
            return removed
        except IndexError:
            logger.error(f"Song index {index} out of range in mood '{mood}'")
            raise

    def rename_song(self, mood_name: str, index: int, new_name: str):
        """
        Rename a song at position index in the given mood, avoiding duplicates.
        
        Args:
            mood_name: Mood containing the song
            index: 0-based index of the song to rename
            new_name: New name for the song
        
        Returns:
            tuple: (old_name, new_name)
        
        Raises:
            KeyError: If mood doesn't exist
            ValueError: If playlist is empty, new name is empty, or duplicate
            IndexError: If index is out of range
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            logger.error(f"Mood '{mood}' not found")
            raise KeyError("Mood not found.")
        if not self.playlists[mood]:
            logger.error(f"Playlist '{mood}' is empty")
            raise ValueError("Playlist is empty.")
        if index < 0 or index >= len(self.playlists[mood]):
            logger.error(f"Song index {index} out of range in mood '{mood}'")
            raise IndexError("Song index out of range.")
        new_name = new_name.strip()
        if not new_name:
            logger.error("Attempted to rename song with empty name")
            raise ValueError("New name cannot be empty.")
        # avoid duplicate after rename
        existing_lower = [s.lower() for i, s in enumerate(self.playlists[mood]) if i != index]
        if new_name.lower() in existing_lower:
            logger.error(f"Song '{new_name}' already exists in '{mood}' playlist")
            raise ValueError("A song with that name already exists.")
        old = self.playlists[mood][index]
        self.playlists[mood][index] = new_name
        logger.info(f"Renamed song '{old}' to '{new_name}' in mood '{mood}'")
        return old, new_name

    def rename_mood(self, old_mood: str, new_mood_name: str):
        """
        Rename a mood (key) if possible.
        
        Args:
            old_mood: Current mood name
            new_mood_name: New name for the mood
        
        Raises:
            KeyError: If old mood doesn't exist
            ValueError: If new mood name is empty, same as old, or already exists
        """
        old = old_mood.strip().lower()
        new = new_mood_name.strip().lower()
        if old not in self.playlists:
            logger.error(f"Mood '{old}' not found")
            raise KeyError("Mood not found.")
        if not new:
            logger.error("Attempted to rename mood with empty name")
            raise ValueError("New mood name cannot be empty.")
        if new == old:
            logger.error("New mood name is same as old name")
            raise ValueError("New mood name is the same as old.")
        if new in self.playlists:
            logger.error(f"Mood '{new}' already exists")
            raise ValueError("A mood with that name already exists.")
        self.playlists[new] = self.playlists.pop(old)
        logger.info(f"Renamed mood '{old}' to '{new}'")

    def clear_all_playlists(self):
        """
        Clear all playlists (empty each mood) but keep the mood keys.
        """
        if not self.playlists:
            self.playlists = {}
            logger.info("Cleared empty playlists dictionary")
            return
        self.playlists = {k: [] for k in self.playlists.keys()}
        logger.info("Cleared all playlists")

    # -------------------------
    # Favorite mood
    # -------------------------
    def set_favorite_mood(self, mood_name: str):
        """
        Set favorite mood on the user (must exist).
        
        Args:
            mood_name: Name of the mood to set as favorite
        
        Raises:
            KeyError: If mood doesn't exist
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            logger.error(f"Mood '{mood}' not found")
            raise KeyError("Mood not found.")
        self.favorite_mood = mood
        logger.info(f"Set favorite mood to '{mood}'")

    def get_favorite_songs(self):
        """
        Return list of songs for the favorite mood, or None if no favorite set.
        
        Returns:
            list or None: List of songs in favorite mood, or None
        """
        if self.favorite_mood and self.favorite_mood in self.playlists:
            return self.playlists[self.favorite_mood]
        return None

    # -------------------------
    # Search & Surprise
    # -------------------------
    def search_song(self, keyword: str):
        """
        Return list of tuples (mood, song) that match the keyword (case-insensitive).
        
        Args:
            keyword: Search keyword
        
        Returns:
            list: List of (mood, song) tuples matching the keyword
        """
        kw = keyword.strip().lower()
        results = []
        for mood, songs in self.playlists.items():
            for song in songs:
                if kw in song.lower():
                    results.append((mood, song))
        logger.info(f"Search for '{keyword}' returned {len(results)} results")
        return results

    def surprise_me(self, mood_name: str = None):
        """
        Return one random song.
        If mood_name given and exists, pick from that mood; otherwise pick from all songs.
        
        Args:
            mood_name: Optional mood to select from (default: None for all songs)
        
        Returns:
            tuple: (mood, song)
        
        Raises:
            KeyError: If specified mood doesn't exist
            ValueError: If no songs are available
        """
        if mood_name:
            m = mood_name.strip().lower()
            if m not in self.playlists:
                logger.error(f"Mood '{m}' not found for surprise")
                raise KeyError("Mood not found.")
            choices = self.playlists[m]
            if not choices:
                logger.error(f"Playlist '{m}' is empty for surprise")
                raise ValueError("That playlist is empty.")
            song = random.choice(choices)
            logger.info(f"Surprise me returned '{song}' from mood '{m}'")
            return m, song
        # pick from all songs
        all_songs = [(m, s) for m, songs in self.playlists.items() for s in songs]
        if not all_songs:
            logger.error("No songs available for surprise")
            raise ValueError("No songs available in any playlist.")
        result = random.choice(all_songs)
        logger.info(f"Surprise me returned '{result[1]}' from mood '{result[0]}'")
        return result

    # -------------------------
    # Statistics
    # -------------------------
    def playlist_statistics(self):
        """
        Compute and return playlist statistics.
        
        Returns:
            dict: Statistics including total_songs, num_moods, longest_playlist, shortest_playlist
        """
        if not self.playlists:
            return {
                "total_songs": 0,
                "num_moods": 0,
                "longest_playlist": (None, 0),
                "shortest_playlist": (None, 0)
            }
        total = sum(len(songs) for songs in self.playlists.values())
        num_moods = len(self.playlists)
        # find longest and shortest by length
        longest_mood = max(self.playlists.items(), key=lambda kv: len(kv[1]))
        shortest_mood = min(self.playlists.items(), key=lambda kv: len(kv[1]))
        return {
            "total_songs": total,
            "num_moods": num_moods,
            "longest_playlist": (longest_mood[0], len(longest_mood[1])),
            "shortest_playlist": (shortest_mood[0], len(shortest_mood[1]))
        }

    # -------------------------
    # Export helpers
    # -------------------------
    def export_to_txt(self, filename):
        """
        Export playlists to text file (does not export password).
        
        Args:
            filename: Path to the output file
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for mood, songs in self.playlists.items():
                    f.write(f"{mood}\n")
                    if songs:
                        for s in songs:
                            f.write(f"{s}\n")
                    else:
                        f.write("(empty)\n")
                    f.write("\n")
            logger.info(f"Exported playlists to {filename}")
            return True, f"Exported to {filename}"
        except Exception as e:
            logger.error(f"Failed to export to txt: {e}")
            return False, str(e)

    def export_to_csv(self, filename):
        """
        Export playlists to CSV file.
        
        Args:
            filename: Path to the output file
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["mood", "song"])
                for mood, songs in self.playlists.items():
                    if songs:
                        for s in songs:
                            writer.writerow([mood, s])
                    else:
                        writer.writerow([mood, ""])
            logger.info(f"Exported playlists to {filename}")
            return True, f"Exported to {filename}"
        except Exception as e:
            logger.error(f"Failed to export to csv: {e}")
            return False, str(e)

    def export_to_json(self, filename):
        """
        Export playlists as JSON (playlists only).
        
        Args:
            filename: Path to the output file
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.playlists, f, indent=4, ensure_ascii=False)
            logger.info(f"Exported playlists to {filename}")
            return True, f"Exported to {filename}"
        except Exception as e:
            logger.error(f"Failed to export to json: {e}")
            return False, str(e)
