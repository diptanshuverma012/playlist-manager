"""
UI module for Playlist Manager
Handles all user interface and interaction functions.
"""

from .user import User
from .storage import save_data
from .utils import get_logger
from config import DEFAULT_PLAYLISTS


def show_all_playlists(playlists):
    """
    Display all playlists (mood -> songs) in a formatted way.

    Args:
        playlists: Dictionary mapping mood names to song lists
    """
    logger = get_logger()
    if not playlists:
        print("⚠️ No playlists found.")
        logger.info("Displayed playlists: None found")
        return
    print("\n📚 All Playlists:")
    for mood, songs in playlists.items():
        print(f"\n━ {mood} ({len(songs)} songs)")
        if songs:
            for i, s in enumerate(songs, 1):
                print(f"   {i}. {s}")
        else:
            print("   (empty)")
    logger.info(f"Displayed all playlists: {len(playlists)} moods")


def login(users):
    """
    Prompt for username/password and return a User object and the loaded raw users dict.

    Args:
        users: Existing users dictionary

    Returns:
        Tuple of (User object or None, users dict)
    """
    logger = get_logger()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username:
        print("❌ Username cannot be empty.")
        logger.warning("Login attempt with empty username")
        return None, users

    if username in users:
        try:
            stored = users[username]
            # Validate structure
            if not isinstance(stored, dict) or "password" not in stored or "playlists" not in stored:
                # Malformed user; create fresh profile
                print("⚠️ User data malformed. Creating a fresh profile for this username.")
                logger.warning(f"Malformed data for user '{username}', creating fresh profile")
                users[username] = {
                    "password": password,
                    "playlists": {k: v.copy() for k, v in DEFAULT_PLAYLISTS.items()}
                }
                save_data(users)
                user_obj = User(username, password, playlists=users[username]["playlists"],
                                default_playlists=DEFAULT_PLAYLISTS)
                return user_obj, users

            if users[username]["password"] == password:
                # Successful login: construct User object with favorite_mood if present
                fav = users[username].get("favorite_mood")
                user_obj = User(username, users[username]["password"],
                                playlists=users[username]["playlists"],
                                favorite_mood=fav,
                                default_playlists=DEFAULT_PLAYLISTS)
                print(f"✅ Welcome back, {username}!")
                logger.info(f"User '{username}' logged in successfully")
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
                logger.warning(f"Failed login attempt for user '{username}': incorrect password")
                return None, users
        except Exception as e:
            print(f"❌ Error during login: {e}")
            logger.error(f"Error during login for user '{username}': {e}")
            return None, users
    else:
        # New user: set default playlists copy to prevent shared references
        print("🆕 New user created with default playlists.")
        logger.info(f"New user '{username}' created")
        users[username] = {
            "password": password,
            "playlists": {k: v.copy() for k, v in DEFAULT_PLAYLISTS.items()}
        }
        save_data(users)
        user_obj = User(username, password, playlists=users[username]["playlists"],
                        default_playlists=DEFAULT_PLAYLISTS)
        return user_obj, users


def playlist_manager(user: User, users_raw: dict):
    """
    Interactive playlist manager for a given user.

    Args:
        user: User object with playlist data
        users_raw: Raw users dictionary for persistence
    """
    logger = get_logger()
    logger.info(f"User '{user.username}' entered playlist manager")

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

        if choice == "1":  # Show songs for mood
            mood = input("Enter your mood: ").strip().lower()
            if mood in user.playlists:
                print(f"\n🎵 Songs for '{mood}' mood:")
                if user.playlists[mood]:
                    for idx, song in enumerate(user.playlists[mood], 1):
                        print(f" {idx}. {song}")
                else:
                    print(" (empty)")
                logger.info(f"User '{user.username}' viewed songs for mood '{mood}'")
            else:
                print("❌ Mood not found. Try again.")
                logger.warning(f"User '{user.username}' tried to view non-existent mood '{mood}'")

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
                    logger.warning(f"User '{user.username}' entered invalid number for song deletion")
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

        elif choice == "10":  # Clear all playlists
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
                users_raw[user.username].pop("favorite_mood", None)
                save_data(users_raw)
                print("✅ Favorite mood removed.")
                logger.info(f"User '{user.username}' removed favorite mood")
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
            logger.info(f"User '{user.username}' exited playlist manager")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1-14.")
            logger.warning(f"User '{user.username}' entered invalid menu choice: {choice}")


def update_password(user: User, users_raw: dict):
    """
    Update a user's password after verifying the current password.

    Args:
        user: User object
        users_raw: Raw users dictionary for persistence
    """
    logger = get_logger()
    old_pass = input("Enter your current password: ").strip()
    if user.password != old_pass:
        print("❌ Incorrect current password. Password not changed.")
        logger.warning(f"User '{user.username}' failed password update: incorrect current password")
        return

    new_pass = input("Enter your new password: ").strip()
    confirm_pass = input("Confirm your new password: ").strip()

    if not new_pass:
        print("❌ New password cannot be empty.")
        logger.warning(f"User '{user.username}' attempted to set empty password")
        return

    if new_pass and new_pass == confirm_pass:
        # update both user object and raw dict
        user.password = new_pass
        users_raw[user.username]["password"] = new_pass
        save_data(users_raw)
        print("✅ Password updated successfully!")
        logger.info(f"User '{user.username}' updated password successfully")
    else:
        print("❌ Passwords do not match or empty.")
        logger.warning(f"User '{user.username}' failed password update: passwords don't match")
