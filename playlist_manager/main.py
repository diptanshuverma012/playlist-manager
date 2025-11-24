"""
Main entry point for Playlist Manager
Orchestrates the application flow using modular components.
"""

from .storage import load_data, save_data, get_storage_type, close_storage
from .ui import login, playlist_manager, update_password
from .utils import setup_logging, get_logger


def main():
    """
    Main application entry point.
    Handles user login and main menu navigation.
    """
    # Setup logging first
    setup_logging()
    logger = get_logger()

    logger.info("="*50)
    logger.info("Application started")
    logger.info("="*50)

    # Display welcome message
    storage_type = get_storage_type()
    print(f" 🎵 Welcome to the Playlist App 🎵")
    print(f" 💾 Storage: {storage_type}")
    logger.info(f"Using storage: {storage_type}")

    # Load existing data
    users_raw = load_data()

    # Login
    user_obj, users_raw = login(users_raw)

    if user_obj:
        # Ensure playlists key exists for user in raw dict
        users_raw.setdefault(user_obj.username, {})
        if "playlists" not in users_raw[user_obj.username]:
            from config import DEFAULT_PLAYLISTS
            users_raw[user_obj.username]["playlists"] = {k: v.copy() for k, v in DEFAULT_PLAYLISTS.items()}
            logger.warning(f"Playlists key missing for user '{user_obj.username}', added default playlists")

        # ensure favorite_mood present if set
        if user_obj.favorite_mood:
            users_raw[user_obj.username]["favorite_mood"] = user_obj.favorite_mood

        # Main menu loop
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
                # persist any final state
                users_raw[user_obj.username]["playlists"] = user_obj.playlists
                if user_obj.favorite_mood:
                    users_raw[user_obj.username]["favorite_mood"] = user_obj.favorite_mood
                else:
                    users_raw[user_obj.username].pop("favorite_mood", None)
                save_data(users_raw)

                # Close storage connections
                close_storage()

                print("👋 Goodbye!")
                logger.info(f"User '{user_obj.username}' logged out")
                logger.info("="*50)
                logger.info("Application terminated normally")
                logger.info("="*50)
                break
            else:
                print("❌ Invalid choice. Please select 1, 2, or 3.")
                logger.warning(f"User '{user_obj.username}' entered invalid main menu choice: {main_choice}")
    else:
        logger.warning("Login failed or cancelled")
        print("Login failed or cancelled. Exiting.")


if __name__ == "__main__":
    main()
