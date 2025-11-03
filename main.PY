import json
import os
import csv
import random
from config import USE_MYSQL, MYSQL_CONFIG, JSON_CONFIG, DEFAULT_PLAYLISTS

if USE_MYSQL:
    try:
        from database import PlaylistDatabase, load_data_from_mysql, save_data_to_mysql
    except ImportError:
        print("⚠️ MySQL module not found. Falling back to JSON storage.")
        USE_MYSQL = False

# Configuration
PLAYLIST_FILE = str(JSON_CONFIG['file_path'])

# Initialize database connection if using MySQL
db = None
if USE_MYSQL:
    db = PlaylistDatabase(**MYSQL_CONFIG)
    db.create_database()
    db.connect()
    db.create_table()

# Default playlists
default_playlists = DEFAULT_PLAYLISTS


# -------------------------
# Utility / Helpers
# -------------------------
def safe_int_input(prompt, min_value=None, max_value=None):
    """Get an integer from user with validation."""
    while True:
        val = input(prompt).strip()
        try:
            i = int(val)
        except ValueError:
            print("❌ Please enter a valid integer.")
            continue
        if (min_value is not None and i < min_value) or (max_value is not None and i > max_value):
            print(f"❌ Please enter a number between {min_value} and {max_value}.")
            continue
        return i


# -------------------------
# Load / Save (MySQL or JSON)
# -------------------------
def load_data():
    """
    Load users data from MySQL or JSON file based on USE_MYSQL setting.
    Returns {} if no data or corrupted data.
    """
    if USE_MYSQL:
        try:
            return load_data_from_mysql(db)
        except Exception as e:
            print(f"❌ Error loading from MySQL: {e}")
            return {}
    else:
        # Original JSON file logic
        if not os.path.exists(PLAYLIST_FILE):
            return {}

        try:
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    print("⚠️ Unexpected data format in file. Resetting to empty.")
                    return {}
                return data
        except FileNotFoundError:
            print("⚠️ Playlist file not found. Starting fresh.")
            return {}
        except json.JSONDecodeError:
            print("❌ Corrupted playlist file (invalid JSON). Resetting data.")
            return {}
        except Exception as e:
            print(f"❌ Unexpected error loading data: {e}")
            return {}


def save_data(data):
    """
    Save full users dict to MySQL or JSON file based on USE_MYSQL setting.
    """
    if USE_MYSQL:
        try:
            save_data_to_mysql(db, data)
        except Exception as e:
            print(f"❌ Error saving to MySQL: {e}")
    else:
        # Original JSON file logic
        try:
            with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except PermissionError:
            print("❌ Permission denied when trying to write the playlists file.")
        except Exception as e:
            print(f"❌ Error saving data: {e}")


# -------------------------
# User class
# -------------------------
class User:
    """
    Represents a user with username, password, playlists, and a favorite mood.
    All playlist operations are provided as methods.
    """

    def __init__(self, username: str, password: str, playlists=None, favorite_mood=None):
        """
        Initialize a User object.
        playlists: dict mapping mood -> list of songs
        favorite_mood: optional string with the user's favorite mood
        """
        self.username = username
        self.password = password
        self.playlists = playlists if playlists is not None else {k: v.copy() for k, v in default_playlists.items()}
        self.favorite_mood = favorite_mood

    # -------------------------
    # Playlist operations (methods)
    # -------------------------
    def create_mood(self, mood_name: str):
        """Create a new mood/playlist if it doesn't exist."""
        mood = mood_name.strip().lower()
        if not mood:
            raise ValueError("Mood name cannot be empty.")
        if mood in self.playlists:
            raise ValueError("Mood already exists.")
        self.playlists[mood] = []

    def add_song(self, mood_name: str, song_name: str):
        """Add a song to a mood; prevents case-insensitive duplicates."""
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            raise KeyError("Mood not found.")
        song = song_name.strip()
        if not song:
            raise ValueError("Song name cannot be empty.")
        existing_lower = [s.lower() for s in self.playlists[mood]]
        if song.lower() in existing_lower:
            raise ValueError("Song already exists in playlist.")
        self.playlists[mood].append(song)

    def delete_song(self, mood_name: str, index: int):
        """Delete a song by index (0-based) from a mood. Raises IndexError if out of range."""
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            raise KeyError("Mood not found.")
        try:
            removed = self.playlists[mood].pop(index)
            return removed
        except IndexError:
            raise

    def rename_song(self, mood_name: str, index: int, new_name: str):
        """Rename a song at position index in the given mood, avoiding duplicates."""
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            raise KeyError("Mood not found.")
        if not self.playlists[mood]:
            raise ValueError("Playlist is empty.")
        if index < 0 or index >= len(self.playlists[mood]):
            raise IndexError("Song index out of range.")
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("New name cannot be empty.")
        # avoid duplicate after rename
        existing_lower = [s.lower() for i, s in enumerate(self.playlists[mood]) if i != index]
        if new_name.lower() in existing_lower:
            raise ValueError("A song with that name already exists.")
        old = self.playlists[mood][index]
        self.playlists[mood][index] = new_name
        return old, new_name

    def rename_mood(self, old_mood: str, new_mood_name: str):
        """Rename a mood (key) if possible."""
        old = old_mood.strip().lower()
        new = new_mood_name.strip().lower()
        if old not in self.playlists:
            raise KeyError("Mood not found.")
        if not new:
            raise ValueError("New mood name cannot be empty.")
        if new == old:
            raise ValueError("New mood name is the same as old.")
        if new in self.playlists:
            raise ValueError("A mood with that name already exists.")
        self.playlists[new] = self.playlists.pop(old)

    def clear_all_playlists(self):
        """Clear all playlists (empty each mood) but keep the mood keys."""
        if not self.playlists:
            self.playlists = {}
            return
        self.playlists = {k: [] for k in self.playlists.keys()}

    # -------------------------
    # Favorite mood
    # -------------------------
    def set_favorite_mood(self, mood_name: str):
        """Set favorite mood on the user (must exist)."""
        mood = mood_name.strip().lower()
        if mood not in self.playlists:
            raise KeyError("Mood not found.")
        self.favorite_mood = mood

    def get_favorite_songs(self):
        """Return list of songs for the favorite mood, or None if no favorite set."""
        if self.favorite_mood and self.favorite_mood in self.playlists:
            return self.playlists[self.favorite_mood]
        return None

    # -------------------------
    # Search & Surprise
    # -------------------------
    def search_song(self, keyword: str):
        """Return list of tuples (mood, song) that match the keyword (case-insensitive)."""
        kw = keyword.strip().lower()
        results = []
        for mood, songs in self.playlists.items():
            for song in songs:
                if kw in song.lower():
                    results.append((mood, song))
        return results

    def surprise_me(self, mood_name: str = None):
        """
        Return one random song.
        If mood_name given and exists, pick from that mood; otherwise pick from all songs.
        Raises ValueError if no songs are available.
        """
        if mood_name:
            m = mood_name.strip().lower()
            if m not in self.playlists:
                raise KeyError("Mood not found.")
            choices = self.playlists[m]
            if not choices:
                raise ValueError("That playlist is empty.")
            return m, random.choice(choices)
        # pick from all songs
        all_songs = [(m, s) for m, songs in self.playlists.items() for s in songs]
        if not all_songs:
            raise ValueError("No songs available in any playlist.")
        return random.choice(all_songs)

    # -------------------------
    # Statistics
    # -------------------------
    def playlist_statistics(self):
        """
        Compute and return playlist statistics:
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
        """Export playlists to text file (does not export password)."""
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
            return True, f"Exported to {filename}"
        except Exception as e:
            return False, str(e)

    def export_to_csv(self, filename):
        """Export playlists to CSV file."""
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
            return True, f"Exported to {filename}"
        except Exception as e:
            return False, str(e)

    def export_to_json(self, filename):
        """Export playlists as JSON (playlists only)."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.playlists, f, indent=4, ensure_ascii=False)
            return True, f"Exported to {filename}"
        except Exception as e:
            return False, str(e)


# -------------------------
# Login
# -------------------------
def login():
    """
    Prompt for username/password and return a User object and the loaded raw users dict.
    If a new user is created or malformed data is detected, it will initialize defaults.
    """
    users = load_data()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username:
        print("❌ Username cannot be empty.")
        return None, users

    if username in users:
        try:
            stored = users[username]
            # Validate structure
            if not isinstance(stored, dict) or "password" not in stored or "playlists" not in stored:
                # Malformed user; create fresh profile
                print("⚠️ User data malformed. Creating a fresh profile for this username.")
                users[username] = {"password": password, "playlists": {k: v.copy() for k, v in default_playlists.items()}}
                save_data(users)
                user_obj = User(username, password, playlists=users[username]["playlists"])
                return user_obj, users

            if users[username]["password"] == password:
                # Successful login: construct User object with favorite_mood if present
                fav = users[username].get("favorite_mood")
                user_obj = User(username, users[username]["password"], playlists=users[username]["playlists"], favorite_mood=fav)
                print(f"✅ Welcome back, {username}!")
                # Auto-display favorite mood songs if set
                if user_obj.favorite_mood:
                    fav_songs = user_obj.get_favorite_songs()
                    if fav_songs is not None:
                        print(f"\n⭐ Your favorite mood is '{user_obj.favorite_mood}'. Songs:")
                        if fav_songs:
                            for i, s in enumerate(fav_songs, 1):
                                print(f"   {i}. {s}")
                        else:
                            print("   (empty)")
                return user_obj, users
            else:
                print("❌ Incorrect password.")
                return None, users
        except Exception as e:
            print(f"❌ Error during login: {e}")
            return None, users
    else:
        # New user: set default playlists copy to prevent shared references
        print("🆕 New user created with default playlists.")
        users[username] = {"password": password, "playlists": {k: v.copy() for k, v in default_playlists.items()}}
        save_data(users)
        user_obj = User(username, password, playlists=users[username]["playlists"])
        return user_obj, users


# -------------------------
# Print helpers (UI)
# -------------------------
def show_all_playlists(playlists):
    """
    Nicely print playlists (mood -> songs). playlists is dict.
    """
    if not playlists:
        print("⚠️ No playlists found.")
        return
    print("\n📚 All Playlists:")
    for mood, songs in playlists.items():
        print(f"\n━ {mood} ({len(songs)} songs)")
        if songs:
            for i, s in enumerate(songs, 1):
                print(f"   {i}. {s}")
        else:
            print("   (empty)")


# -------------------------
# Playlist Manager (menu)
# -------------------------
def playlist_manager(user: User, users_raw: dict):
    """
    Interactive playlist manager for a given user (User object).
    Saves changes into users_raw (the raw dict) and writes to disk/MySQL when necessary.
    """
    while True:
        print("\n🎶 Playlist Menu:")
        print("1. Show songs for a mood")
        print("2. Add a song to a mood")
        print("3. Delete a song from a mood")
        print("4. Search for a song")
        print("5. Create new mood/playlist")
        print("6. Rename a song")
        print("7. Rename a mood")
        print("8. Export playlists to file (txt/csv/json)")
        print("9. Show all playlists")
        print("10. Clear all playlists (preserve password)")
        print("11. Set / Show Favorite Mood")
        print("12. Surprise Me (random song)")
        print("13. Playlist Statistics")
        print("14. Back to Main Menu")

        choice = input("Enter your choice (1-14): ").strip()
        # Always operate on user.playlists; update users_raw when changes made
        if choice == "1":  # Show songs for mood
            mood = input("Enter your mood: ").strip().lower()
            if mood in user.playlists:
                print(f"\n🎵 Songs for '{mood}' mood:")
                if user.playlists[mood]:
                    for idx, song in enumerate(user.playlists[mood], 1):
                        print(f" {idx}. {song}")
                else:
                    print(" (empty)")
            else:
                print("❌ Mood not found. Try again.")

        elif choice == "2":  # Add song
            mood = input("Enter the mood you want to add a song to: ").strip().lower()
            try:
                if mood not in user.playlists:
                    print("❌ Mood not found. You can create it from the Playlist Menu option 'Create new mood'.")
                else:
                    new_song = input("Enter the name of the song to add: ").strip()
                    user.add_song(mood, new_song)
                    # persist
                    users_raw[user.username]["playlists"] = user.playlists
                    save_data(users_raw)
                    print(f"✅ '{new_song}' added to the '{mood}' playlist.")
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "3":  # Delete song
            mood = input("Enter the mood you want to delete a song from: ").strip().lower()
            if mood not in user.playlists:
                print("❌ Mood not found. Cannot delete song.")
            elif not user.playlists[mood]:
                print(f"⚠️ The '{mood}' playlist is empty.")
            else:
                print(f"\n🎵 Songs in '{mood}' playlist:")
                for idx, song in enumerate(user.playlists[mood], 1):
                    print(f" {idx}. {song}")
                try:
                    song_index = int(input("Enter the number of the song to delete: ").strip()) - 1
                except ValueError:
                    print("❌ Please enter a valid number.")
                    continue
                try:
                    removed = user.delete_song(mood, song_index)
                    users_raw[user.username]["playlists"] = user.playlists
                    save_data(users_raw)
                    print(f"🗑️ '{removed}' has been deleted from '{mood}' playlist.")
                except IndexError:
                    print("❌ That number is out of range. No song deleted.")
                except Exception as e:
                    print(f"❌ {e}")

        elif choice == "4":  # Search
            keyword = input("Enter a keyword to search for: ").strip()
            if keyword:
                results = user.search_song(keyword)
                if results:
                    print("\n🔍 Search Results:")
                    for mood, song in results:
                        print(f" - {song} ({mood})")
                else:
                    print("❌ No matching songs found.")
            else:
                print("❌ Keyword cannot be empty.")

        elif choice == "5":  # Create new mood
            new_mood = input("Enter the new mood name: ").strip().lower()
            try:
                user.create_mood(new_mood)
                users_raw[user.username]["playlists"] = user.playlists
                save_data(users_raw)
                print(f"✅ Mood '{new_mood}' created (empty).")
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "6":  # Rename a song
            mood = input("Enter the mood containing the song to rename: ").strip().lower()
            if mood not in user.playlists:
                print("❌ Mood not found.")
                continue
            if not user.playlists[mood]:
                print(f"⚠️ The '{mood}' playlist is empty.")
                continue
            print(f"\n🎵 Songs in '{mood}' playlist:")
            for idx, song in enumerate(user.playlists[mood], 1):
                print(f" {idx}. {song}")
            try:
                song_index = int(input("Enter the number of the song to rename: ").strip()) - 1
                new_name = input(f"Enter new name: ").strip()
                old, new = user.rename_song(mood, song_index, new_name)
                users_raw[user.username]["playlists"] = user.playlists
                save_data(users_raw)
                print(f"✏️ Renamed '{old}' → '{new}' in '{mood}'.")
            except ValueError as ve:
                print(f"❌ {ve}")
            except IndexError:
                print("❌ That number is out of range.")
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "7":  # Rename a mood
            old_mood = input("Enter the mood you want to rename: ").strip().lower()
            if old_mood not in user.playlists:
                print("❌ Mood not found.")
                continue
            new_mood = input(f"Enter the new name for mood '{old_mood}': ").strip().lower()
            try:
                user.rename_mood(old_mood, new_mood)
                users_raw[user.username]["playlists"] = user.playlists
                # If favorite mood was old name, update favorite_mood
                if user.favorite_mood == old_mood:
                    user.favorite_mood = new_mood
                    users_raw[user.username]["favorite_mood"] = new_mood
                save_data(users_raw)
                print(f"✏️ Mood renamed '{old_mood}' → '{new_mood}'.")
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "8":  # Export playlists
            if not user.playlists:
                print("⚠️ No playlists to export.")
                continue
            print("Choose export format:")
            print("1. .txt")
            print("2. .csv")
            print("3. .json")
            exp_choice = input("Enter 1, 2 or 3: ").strip()
            base_filename = input("Enter filename (without extension): ").strip()
            if not base_filename:
                print("❌ Filename cannot be empty.")
                continue
            if exp_choice == "1":
                filename = base_filename + ".txt"
                ok, msg = user.export_to_txt(filename)
                if ok:
                    print(f"✅ {msg}.")
                else:
                    print(f"❌ Failed to export: {msg}")
            elif exp_choice == "2":
                filename = base_filename + ".csv"
                ok, msg = user.export_to_csv(filename)
                if ok:
                    print(f"✅ {msg}.")
                else:
                    print(f"❌ Failed to export: {msg}")
            elif exp_choice == "3":
                filename = base_filename + ".json"
                ok, msg = user.export_to_json(filename)
                if ok:
                    print(f"✅ {msg}.")
                else:
                    print(f"❌ Failed to export: {msg}")
            else:
                print("❌ Invalid choice for export format.")

        elif choice == "9":  # Show all playlists
            show_all_playlists(user.playlists)

        elif choice == "10":  # Clear all playlists (preserve password)
            confirm = input("Are you sure you want to CLEAR ALL playlists? This cannot be undone. (yes/no): ").strip().lower()
            if confirm not in ("yes", "y"):
                print("⚠️ Clear all cancelled.")
                continue
            user.clear_all_playlists()
            users_raw[user.username]["playlists"] = user.playlists
            save_data(users_raw)
            print("🧹 All playlists cleared (password preserved).")

        elif choice == "11":  # Set / Show Favorite Mood
            print(f"\n⭐ Current favorite mood: {user.favorite_mood}")
            print("1. Set favorite mood")
            print("2. Remove favorite mood")
            print("3. Back")
            sub = input("Enter choice (1-3): ").strip()
            if sub == "1":
                mood = input("Enter mood to set as favorite: ").strip().lower()
                try:
                    user.set_favorite_mood(mood)
                    users_raw[user.username]["favorite_mood"] = user.favorite_mood
                    save_data(users_raw)
                    print(f"✅ Favorite mood set to '{mood}'.")
                    fav_songs = user.get_favorite_songs()
                    if fav_songs:
                        print("Songs in favorite mood:")
                        for i, s in enumerate(fav_songs, 1):
                            print(f" {i}. {s}")
                    else:
                        print(" (empty)")
                except Exception as e:
                    print(f"❌ {e}")
            elif sub == "2":
                user.favorite_mood = None
                # remove key if existed
                users_raw[user.username].pop("favorite_mood", None)
                save_data(users_raw)
                print("✅ Favorite mood removed.")
            else:
                continue

        elif choice == "12":  # Surprise Me
            print("1. Surprise me from a specific mood")
            print("2. Surprise me from all playlists")
            sub = input("Enter choice (1-2): ").strip()
            if sub == "1":
                mood = input("Enter mood: ").strip().lower()
                try:
                    mood_name, song = user.surprise_me(mood)
                    print(f"🎉 Surprise! From '{mood_name}': {song}")
                except Exception as e:
                    print(f"❌ {e}")
            elif sub == "2":
                try:
                    mood_name, song = user.surprise_me()
                    print(f"🎉 Surprise! From '{mood_name}': {song}")
                except Exception as e:
                    print(f"❌ {e}")
            else:
                print("❌ Invalid choice.")

        elif choice == "13":  # Playlist Statistics
            stats = user.playlist_statistics()
            print("\n📊 Playlist Statistics:")
            print(f" - Total number of songs: {stats['total_songs']}")
            print(f" - Number of moods: {stats['num_moods']}")
            long_mood, long_count = stats["longest_playlist"]
            short_mood, short_count = stats["shortest_playlist"]
            if long_mood:
                print(f" - Longest playlist: '{long_mood}' ({long_count} songs)")
            else:
                print(" - Longest playlist: (none)")
            if short_mood:
                print(f" - Shortest playlist: '{short_mood}' ({short_count} songs)")
            else:
                print(" - Shortest playlist: (none)")

        elif choice == "14":  # Back
            break
        else:
            print("❌ Invalid choice. Please select a number from 1-14.")


# -------------------------
# Update password
# -------------------------
def update_password(user: User, users_raw: dict):
    """Update a user's password after verifying the current password."""
    old_pass = input("Enter your current password: ").strip()
    if user.password != old_pass:
        print("❌ Incorrect current password. Password not changed.")
        return

    new_pass = input("Enter your new password: ").strip()
    confirm_pass = input("Confirm your new password: ").strip()

    if not new_pass:
        print("❌ New password cannot be empty.")
        return

    if new_pass and new_pass == confirm_pass:
        # update both user object and raw dict
        user.password = new_pass
        users_raw[user.username]["password"] = new_pass
        save_data(users_raw)
        print("✅ Password updated successfully!")
    else:
        print("❌ Passwords do not match or empty.")


# -------------------------
# Main Program
# -------------------------
def main():
    storage_type = "MySQL Database" if USE_MYSQL else "JSON File"
    print(f" 🎵 Welcome to the Playlist App 🎵")
    print(f" 💾 Storage: {storage_type}")

    user_obj, users_raw = login()
    if user_obj:
        # Ensure playlists key exists for user in raw dict
        users_raw.setdefault(user_obj.username, {})
        users_raw[user_obj.username].setdefault("playlists", {k: v.copy() for k, v in default_playlists.items()})
        # ensure favorite_mood present if set
        if user_obj.favorite_mood:
            users_raw[user_obj.username]["favorite_mood"] = user_obj.favorite_mood

        while True:
            print("\n📌 Main Menu:")
            print("1. Playlist Manager")
            print("2. Update Password")
            print("3. Exit")

            main_choice = input("Enter your choice (1-3): ").strip()

            if main_choice == "1":
                playlist_manager(user_obj, users_raw)
            elif main_choice == "2":
                update_password(user_obj, users_raw)
            elif main_choice == "3":
                # persist any final state to file/MySQL (playlists and favorite)
                users_raw[user_obj.username]["playlists"] = user_obj.playlists
                if user_obj.favorite_mood:
                    users_raw[user_obj.username]["favorite_mood"] = user_obj.favorite_mood
                else:
                    users_raw[user_obj.username].pop("favorite_mood", None)
                save_data(users_raw)
                
                # Close database connection if using MySQL
                if USE_MYSQL and db:
                    db.disconnect()
                
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()