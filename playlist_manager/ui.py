"""
UI module for Playlist Manager.
Contains user interface functions for menus, display, and input handling.
"""

import logging
from .user import User
from .storage import save_data

logger = logging.getLogger(__name__)


def show_all_playlists(playlists):
    """
    Nicely print playlists (mood -> songs).
    
    Args:
        playlists: Dictionary mapping mood names to song lists
    """
    if not playlists:
        print("⚠️ No playlists found.")
        logger.info("Display: No playlists found")
        return
    print("\n📚 All Playlists:")
    for mood, songs in playlists.items():
        print(f"\n━ {mood} ({len(songs)} songs)")
        if songs:
            for i, s in enumerate(songs, 1):
                print(f"   {i}. {s}")
        else:
            print("   (empty)")
    logger.info(f"Displayed all playlists ({len(playlists)} moods)")


def playlist_manager(user: User, users_raw: dict):
    """
    Interactive playlist manager for a given user (User object).
    Saves changes into users_raw (the raw dict) and writes to disk/MySQL when necessary.
    
    Args:
        user: User object representing the current user
        users_raw: Dictionary containing all users' raw data
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
        logger.info(f"User selected playlist menu option: {choice}")
        
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
                logger.info(f"Displayed songs for mood '{mood}'")
            else:
                print("❌ Mood not found. Try again.")
                logger.warning(f"Mood '{mood}' not found")

        elif choice == "2":  # Add song
            mood = input("Enter the mood you want to add a song to: ").strip().lower()
            try:
                if mood not in user.playlists:
                    print("❌ Mood not found. You can create it from the Playlist Menu option 'Create new mood'.")
                    logger.warning(f"Attempted to add song to non-existent mood '{mood}'")
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
                logger.warning(f"Mood '{mood}' not found for deletion")
            elif not user.playlists[mood]:
                print(f"⚠️ The '{mood}' playlist is empty.")
                logger.info(f"Mood '{mood}' is empty")
            else:
                print(f"\n🎵 Songs in '{mood}' playlist:")
                for idx, song in enumerate(user.playlists[mood], 1):
                    print(f" {idx}. {song}")
                try:
                    song_index = int(input("Enter the number of the song to delete: ").strip()) - 1
                except ValueError:
                    print("❌ Please enter a valid number.")
                    logger.error("Invalid number input for song deletion")
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
                logger.warning("Empty keyword provided for search")

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
                logger.warning(f"Mood '{mood}' not found for renaming song")
                continue
            if not user.playlists[mood]:
                print(f"⚠️ The '{mood}' playlist is empty.")
                logger.info(f"Mood '{mood}' is empty")
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
                logger.warning(f"Mood '{old_mood}' not found for renaming")
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
                logger.info("No playlists to export")
                continue
            print("Choose export format:")
            print("1. .txt")
            print("2. .csv")
            print("3. .json")
            exp_choice = input("Enter 1, 2 or 3: ").strip()
            base_filename = input("Enter filename (without extension): ").strip()
            if not base_filename:
                print("❌ Filename cannot be empty.")
                logger.warning("Empty filename provided for export")
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
                logger.warning(f"Invalid export format choice: {exp_choice}")

        elif choice == "9":  # Show all playlists
            show_all_playlists(user.playlists)

        elif choice == "10":  # Clear all playlists (preserve password)
            confirm = input("Are you sure you want to CLEAR ALL playlists? This cannot be undone. (yes/no): ").strip().lower()
            if confirm not in ("yes", "y"):
                print("⚠️ Clear all cancelled.")
                logger.info("Clear all playlists cancelled by user")
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
                logger.info("Favorite mood removed")
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
                logger.warning(f"Invalid surprise me choice: {sub}")

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
            logger.info("Displayed playlist statistics")

        elif choice == "14":  # Back
            logger.info("Returning to main menu")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1-14.")
            logger.warning(f"Invalid playlist menu choice: {choice}")


def update_password(user: User, users_raw: dict):
    """
    Update a user's password after verifying the current password.
    
    Args:
        user: User object representing the current user
        users_raw: Dictionary containing all users' raw data
    """
    old_pass = input("Enter your current password: ").strip()
    if user.password != old_pass:
        print("❌ Incorrect current password. Password not changed.")
        logger.warning(f"Failed password change attempt for user '{user.username}'")
        return

    new_pass = input("Enter your new password: ").strip()
    confirm_pass = input("Confirm your new password: ").strip()

    if not new_pass:
        print("❌ New password cannot be empty.")
        logger.warning("Empty password provided")
        return

    if new_pass and new_pass == confirm_pass:
        # update both user object and raw dict
        user.password = new_pass
        users_raw[user.username]["password"] = new_pass
        save_data(users_raw)
        print("✅ Password updated successfully!")
        logger.info(f"Password updated for user '{user.username}'")
    else:
        print("❌ Passwords do not match or empty.")
        logger.warning("Password mismatch during update")
