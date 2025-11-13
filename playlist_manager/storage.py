"""
Storage module for Playlist Manager
Handles data persistence using MySQL or JSON.
"""

import json
import os
from config import USE_MYSQL, MYSQL_CONFIG, JSON_CONFIG
from .utils import get_logger

# Initialize logger
logger = None

# Initialize database connection if using MySQL
db = None
if USE_MYSQL:
    try:
        from database import PlaylistDatabase, load_data_from_mysql, save_data_to_mysql
        db = PlaylistDatabase(**MYSQL_CONFIG)
        db.create_database()
        db.connect()
        db.create_table()
    except ImportError:
        logger_instance = get_logger()
        logger_instance.warning("MySQL module not found. Falling back to JSON storage.")
        print("⚠️ MySQL module not found. Falling back to JSON storage.")
        USE_MYSQL = False
    except Exception as e:
        logger_instance = get_logger()
        logger_instance.error(f"MySQL initialization failed: {e}")
        print(f"⚠️ MySQL initialization failed: {e}. Falling back to JSON storage.")
        USE_MYSQL = False


# Configuration
PLAYLIST_FILE = str(JSON_CONFIG['file_path'])


def load_data():
    """
    Load users data from MySQL or JSON file based on USE_MYSQL setting.

    Returns:
        Dictionary of users data, or {} if no data or corrupted data
    """
    global logger
    if logger is None:
        logger = get_logger()

    if USE_MYSQL:
        try:
            data = load_data_from_mysql(db)
            logger.info(f"Loaded data from MySQL: {len(data)} users")
            return data
        except Exception as e:
            logger.error(f"Error loading from MySQL: {e}")
            print(f"❌ Error loading from MySQL: {e}")
            return {}
    else:
        # JSON file logic
        if not os.path.exists(PLAYLIST_FILE):
            logger.info("Playlist file not found. Starting with empty data.")
            return {}

        try:
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    logger.warning("Unexpected data format in file. Resetting to empty.")
                    print("⚠️ Unexpected data format in file. Resetting to empty.")
                    return {}
                logger.info(f"Loaded data from JSON: {len(data)} users")
                return data
        except FileNotFoundError:
            logger.info("Playlist file not found. Starting fresh.")
            print("⚠️ Playlist file not found. Starting fresh.")
            return {}
        except json.JSONDecodeError:
            logger.error("Corrupted playlist file (invalid JSON). Resetting data.")
            print("❌ Corrupted playlist file (invalid JSON). Resetting data.")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            print(f"❌ Unexpected error loading data: {e}")
            return {}


def save_data(data):
    """
    Save full users dict to MySQL or JSON file based on USE_MYSQL setting.

    Args:
        data: Dictionary containing all users data
    """
    global logger
    if logger is None:
        logger = get_logger()

    if USE_MYSQL:
        try:
            save_data_to_mysql(db, data)
            logger.info(f"Saved data to MySQL: {len(data)} users")
        except Exception as e:
            logger.error(f"Error saving to MySQL: {e}")
            print(f"❌ Error saving to MySQL: {e}")
    else:
        # JSON file logic
        try:
            with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved data to JSON: {len(data)} users")
        except PermissionError:
            logger.error("Permission denied when trying to write the playlists file.")
            print("❌ Permission denied when trying to write the playlists file.")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            print(f"❌ Error saving data: {e}")


def close_storage():
    """
    Close any open storage connections (e.g., database connection).
    """
    global logger
    if logger is None:
        logger = get_logger()

    if USE_MYSQL and db:
        try:
            db.disconnect()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")


def get_storage_type():
    """
    Get the current storage type being used.

    Returns:
        String describing the storage type
    """
    return "MySQL Database" if USE_MYSQL else "JSON File"
