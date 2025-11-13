"""
User module for Playlist Manager
Contains the User class with all playlist operations.
"""

import json
import csv
import random
from .utils import get_logger


class User:
    """
    Represents a user with username, password, playlists, and a favorite mood.
    All playlist operations are provided as methods.
    """

    def __init__(self, username: str, password: str, playlists=None, favorite_mood=None, default_playlists=None):
        """
        Initialize a User object.

        Args:
            username: Username string
            password: Password string
            playlists: dict mapping mood -> list of songs
            favorite_mood: optional string with the user's favorite mood
            default_playlists: default playlists template (optional)
        """
        self.username = username
        self.password = password
        self.logger = get_logger()

        if playlists is not None:
            self.playlists = playlists
        elif default_playlists is not None:
            self.playlists = {k: v.copy() for k, v in default_playlists.items()}
        else:
            self.playlists = {}

        self.favorite_mood = favorite_mood
        self.logger.info(f"User '{username}' initialized with {len(self.playlists)} playlists")

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
            self.logger.error(f"User '{self.username}' attempted to create mood with empty name")
            raise ValueError("Mood name cannot be empty.")
        if mood in self.playlists:
            self.logger.warning(f"User '{self.username}' attempted to create existing mood '{mood}'")
            raise ValueError("Mood already exists.")
        self.playlists[mood] = []
        self.logger.info(f"User '{self.username}' created new mood '{mood}'")

    def add_song(self, mood_name: str, song_name: str):
        """
        Add a song to a mood; prevents case-insensitive duplicates.

        Args:
            mood_name: Name of the mood
            song_name: Name of the song to add

        Raises:
            KeyError: If mood not found
            ValueError: If song name is empty or already exists
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            self.logger.error(f"User '{self.username}' attempted to add song to non-existent mood '{mood}'")
            raise KeyError("Mood not found.")
        song = song_name.strip()
        if not song:
            self.logger.error(f"User '{self.username}' attempted to add empty song name to mood '{mood}'")
            raise ValueError("Song name cannot be empty.")
        existing_lower = [s.lower() for s in self.playlists[mood]]
        if song.lower() in existing_lower:
            self.logger.warning(f"User '{self.username}' attempted to add duplicate song '{song}' to mood '{mood}'")
            raise ValueError("Song already exists in playlist.")
        self.playlists[mood].append(song)
        self.logger.info(f"User '{self.username}' added song '{song}' to mood '{mood}'")

    def delete_song(self, mood_name: str, index: int):
        """
        Delete a song by index (0-based) from a mood.

        Args:
            mood_name: Name of the mood
            index: Index of song to delete (0-based)

        Returns:
            The deleted song name

        Raises:
            KeyError: If mood not found
            IndexError: If index out of range
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            self.logger.error(f"User '{self.username}' attempted to delete song from non-existent mood '{mood}'")
            raise KeyError("Mood not found.")
        try:
            removed = self.playlists[mood].pop(index)
            self.logger.info(f"User '{self.username}' deleted song '{removed}' from mood '{mood}' at index {index}")
            return removed
        except IndexError:
            self.logger.error(f"User '{self.username}' attempted to delete song at invalid index {index} from mood '{mood}'")
            raise

    def rename_song(self, mood_name: str, index: int, new_name: str):
        """
        Rename a song at position index in the given mood, avoiding duplicates.

        Args:
            mood_name: Name of the mood
            index: Index of song to rename (0-based)
            new_name: New name for the song

        Returns:
            Tuple of (old_name, new_name)

        Raises:
            KeyError: If mood not found
            ValueError: If playlist is empty, new name is empty, or duplicate
            IndexError: If index out of range
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            self.logger.error(f"User '{self.username}' attempted to rename song in non-existent mood '{mood}'")
            raise KeyError("Mood not found.")
        if not self.playlists[mood]:
            self.logger.error(f"User '{self.username}' attempted to rename song in empty mood '{mood}'")
            raise ValueError("Playlist is empty.")
        if index < 0 or index >= len(self.playlists[mood]):
            self.logger.error(f"User '{self.username}' attempted to rename song at invalid index {index} in mood '{mood}'")
            raise IndexError("Song index out of range.")
        new_name = new_name.strip()
        if not new_name:
            self.logger.error(f"User '{self.username}' attempted to rename song with empty name in mood '{mood}'")
            raise ValueError("New name cannot be empty.")
        # avoid duplicate after rename
        existing_lower = [s.lower() for i, s in enumerate(self.playlists[mood]) if i != index]
        if new_name.lower() in existing_lower:
            self.logger.warning(f"User '{self.username}' attempted to rename song to existing name '{new_name}' in mood '{mood}'")
            raise ValueError("A song with that name already exists.")
        old = self.playlists[mood][index]
        self.playlists[mood][index] = new_name
        self.logger.info(f"User '{self.username}' renamed song '{old}' to '{new_name}' in mood '{mood}'")
        return old, new_name

    def rename_mood(self, old_mood: str, new_mood_name: str):
        """
        Rename a mood (key) if possible.

        Args:
            old_mood: Current mood name
            new_mood_name: New mood name

        Raises:
            KeyError: If old mood not found
            ValueError: If new name is empty, same as old, or already exists
        """
        old = old_mood.strip().lower()
        new = new_mood_name.strip().lower()
        if old not in self.playlists:
            self.logger.error(f"User '{self.username}' attempted to rename non-existent mood '{old}'")
            raise KeyError("Mood not found.")
        if not new:
            self.logger.error(f"User '{self.username}' attempted to rename mood '{old}' with empty name")
            raise ValueError("New mood name cannot be empty.")
        if new == old:
            self.logger.warning(f"User '{self.username}' attempted to rename mood '{old}' to same name")
            raise ValueError("New mood name is the same as old.")
        if new in self.playlists:
            self.logger.warning(f"User '{self.username}' attempted to rename mood '{old}' to existing mood '{new}'")
            raise ValueError("A mood with that name already exists.")
        self.playlists[new] = self.playlists.pop(old)
        self.logger.info(f"User '{self.username}' renamed mood '{old}' to '{new}'")

    def clear_all_playlists(self):
        """Clear all playlists (empty each mood) but keep the mood keys."""
        if not self.playlists:
            self.playlists = {}
            self.logger.info(f"User '{self.username}' cleared all playlists (was empty)")
            return
        self.playlists = {k: [] for k in self.playlists.keys()}
        self.logger.warning(f"User '{self.username}' cleared all playlists")

    # -------------------------
    # Favorite mood
    # -------------------------
    def set_favorite_mood(self, mood_name: str):
        """
        Set favorite mood on the user (must exist).

        Args:
            mood_name: Name of mood to set as favorite

        Raises:
            KeyError: If mood not found
        """
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            self.logger.error(f"User '{self.username}' attempted to set non-existent mood '{mood}' as favorite")
            raise KeyError("Mood not found.")
        self.favorite_mood = mood
        self.logger.info(f"User '{self.username}' set favorite mood to '{mood}'")

    def get_favorite_songs(self):
        """
        Return list of songs for the favorite mood, or None if no favorite set.

        Returns:
            List of songs or None
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
            List of (mood, song) tuples
        """
        kw = keyword.strip().lower()
        results = []
        for mood, songs in self.playlists.items():
            for song in songs:
                if kw in song.lower():
                    results.append((mood, song))
        self.logger.info(f"User '{self.username}' searched for '{keyword}', found {len(results)} results")
        return results

    def surprise_me(self, mood_name: str = None):
        """
        Return one random song.

        Args:
            mood_name: Optional mood to pick from; if None, pick from all songs

        Returns:
            Tuple of (mood, song)

        Raises:
            KeyError: If specified mood not found
            ValueError: If no songs available
        """
        if mood_name:
            m = mood_name.strip().lower()
            if m not in self.playlists:
                self.logger.error(f"User '{self.username}' requested surprise from non-existent mood '{m}'")
                raise KeyError("Mood not found.")
            choices = self.playlists[m]
            if not choices:
                self.logger.warning(f"User '{self.username}' requested surprise from empty mood '{m}'")
                raise ValueError("That playlist is empty.")
            song = random.choice(choices)
            self.logger.info(f"User '{self.username}' got surprise song '{song}' from mood '{m}'")
            return m, song
        # pick from all songs
        all_songs = [(m, s) for m, songs in self.playlists.items() for s in songs]
        if not all_songs:
            self.logger.warning(f"User '{self.username}' requested surprise but no songs available")
            raise ValueError("No songs available in any playlist.")
        mood, song = random.choice(all_songs)
        self.logger.info(f"User '{self.username}' got surprise song '{song}' from mood '{mood}'")
        return mood, song

    # -------------------------
    # Statistics
    # -------------------------
    def playlist_statistics(self):
        """
        Compute and return playlist statistics.

        Returns:
            Dictionary with statistics:
            - total_songs: int
            - num_moods: int
            - longest_playlist: (mood, count) or (None, 0)
            - shortest_playlist: (mood, count) or (None, 0)
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
        self.logger.info(f"User '{self.username}' retrieved playlist statistics: {total} songs, {num_moods} moods")
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
            filename: Output filename

        Returns:
            Tuple of (success: bool, message: str)
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
            self.logger.info(f"User '{self.username}' exported playlists to TXT: {filename}")
            return True, f"Exported to {filename}"
        except Exception as e:
            self.logger.error(f"User '{self.username}' failed to export to TXT: {e}")
            return False, str(e)

    def export_to_csv(self, filename):
        """
        Export playlists to CSV file.

        Args:
            filename: Output filename

        Returns:
            Tuple of (success: bool, message: str)
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
            self.logger.info(f"User '{self.username}' exported playlists to CSV: {filename}")
            return True, f"Exported to {filename}"
        except Exception as e:
            self.logger.error(f"User '{self.username}' failed to export to CSV: {e}")
            return False, str(e)

    def export_to_json(self, filename):
        """
        Export playlists as JSON (playlists only).

        Args:
            filename: Output filename

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.playlists, f, indent=4, ensure_ascii=False)
            self.logger.info(f"User '{self.username}' exported playlists to JSON: {filename}")
            return True, f"Exported to {filename}"
        except Exception as e:
            self.logger.error(f"User '{self.username}' failed to export to JSON: {e}")
            return False, str(e)
