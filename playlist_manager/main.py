"""
Main application module for Playlist Manager.
Entry point and main application logic including user authentication.
"""

import logging
import sys
from .user import User
from .storage import load_data, save_data, get_default_playlists, close_storage
from .ui import playlist_manager, update_password

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('playlist.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import configuration for storage type
try:
    from config import USE_MYSQL
except ImportError:
    USE_MYSQL = False


def login():
    """
    Prompt for username/password and return a User object and the loaded raw users dict.
    If a new user is created or malformed data is detected, it will initialize defaults.
    
    Returns:
        tuple: (User object or None, users dictionary)
    """
    users = load_data()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username:
        print("❌ Username cannot be empty.")
        logger.error("Empty username provided")
        return None, users

    if username in users:
        try:
            stored = users[username]
            # Validate structure
            if not isinstance(stored, dict) or "password" not in stored or "playlists" not in stored:
                # Malformed user; create fresh profile
                print("⚠️ User data malformed. Creating a fresh profile for this username.")
                logger.warning(f"Malformed user data for '{username}', creating fresh profile")
                users[username] = {
                    "password": password, 
                    "playlists": get_default_playlists()
                }
                save_data(users)
                user_obj = User(username, password, playlists=users[username]["playlists"])
                return user_obj, users

            if users[username]["password"] == password:
                # Successful login: construct User object with favorite_mood if present
                fav = users[username].get("favorite_mood")
                user_obj = User(
                    username, 
                    users[username]["password"], 
                    playlists=users[username]["playlists"], 
                    favorite_mood=fav
                )
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
                logger.warning(f"Incorrect password attempt for user '{username}'")
                return None, users
        except Exception as e:
            logger.error(f"Error during login for user '{username}': {e}")
            print(f"❌ Error during login: {e}")
            return None, users
    else:
        # New user: set default playlists copy to prevent shared references
        print("🆕 New user created with default playlists.")
        logger.info(f"New user created: {username}")
        users[username] = {
            "password": password, 
            "playlists": get_default_playlists()
        }
        save_data(users)
        user_obj = User(username, password, playlists=users[username]["playlists"])
        return user_obj, users


def main():
    """
    Main application entry point.
    Handles user authentication and main menu navigation.
    """
    storage_type = "MySQL Database" if USE_MYSQL else "JSON File"
    print(f" 🎵 Welcome to the Playlist App 🎵")
    print(f" 💾 Storage: {storage_type}")
    logger.info(f"Application started with storage type: {storage_type}")

    user_obj, users_raw = login()
    if user_obj:
        # Ensure playlists key exists for user in raw dict
        users_raw.setdefault(user_obj.username, {})
        users_raw[user_obj.username].setdefault("playlists", get_default_playlists())
        # ensure favorite_mood present if set
        if user_obj.favorite_mood:
            users_raw[user_obj.username]["favorite_mood"] = user_obj.favorite_mood

        while True:
            print("\n📌 Main Menu:")
            print("1. Playlist Manager")
            print("2. Update Password")
            print("3. Exit")

            main_choice = input("Enter your choice (1-3): ").strip()
            logger.info(f"User selected main menu option: {main_choice}")

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
                close_storage()
                
                print("👋 Goodbye!")
                logger.info(f"User '{user_obj.username}' logged out")
                break
            else:
                print("❌ Invalid choice. Please select 1, 2, or 3.")
                logger.warning(f"Invalid main menu choice: {main_choice}")


if __name__ == "__main__":
    main()
