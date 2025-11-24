"""
Storage module for Playlist Manager.
Handles data persistence using MySQL or JSON file storage.
"""

import json
import os
import logging

logger = logging.getLogger(__name__)

# Import configuration
try:
    from config import USE_MYSQL, MYSQL_CONFIG, JSON_CONFIG, DEFAULT_PLAYLISTS
except ImportError:
    # Fallback defaults if config not available
    USE_MYSQL = False
    JSON_CONFIG = {'file_path': 'playlists.json', 'encoding': 'utf-8'}
    DEFAULT_PLAYLISTS = {
        "happy": ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake", "Uptown Funk - Bruno Mars"],
        "sad": ["Someone Like You - Adele", "Let Her Go - Passenger", "Fix You - Coldplay"],
        "energetic": ["Stronger - Kanye West", "Eye of the Tiger - Survivor", "Titanium - David Guetta ft. Sia"],
        "calm": ["Weightless - Marconi Union", "River Flows in You - Yiruma", "Sunrise - Norah Jones"]
    }

# Initialize MySQL if enabled
db = None
if USE_MYSQL:
    try:
        from database import PlaylistDatabase, load_data_from_mysql, save_data_to_mysql
        db = PlaylistDatabase(**MYSQL_CONFIG)
        db.create_database()
        db.connect()
        db.create_table()
        logger.info("MySQL database initialized successfully")
    except ImportError:
        logger.warning("MySQL module not found. Falling back to JSON storage.")
        USE_MYSQL = False
    except Exception as e:
        logger.error(f"Failed to initialize MySQL: {e}. Falling back to JSON storage.")
        USE_MYSQL = False

# Configuration
PLAYLIST_FILE = str(JSON_CONFIG['file_path'])


def get_default_playlists():
    """
    Return a copy of default playlists.
    
    Returns:
        dict: Copy of default playlists configuration
    """
    return {k: v.copy() for k, v in DEFAULT_PLAYLISTS.items()}


def load_data():
    """
    Load users data from MySQL or JSON file based on USE_MYSQL setting.
    
    Returns:
        dict: Dictionary of all users data, or {} if no data or error
    """
    if USE_MYSQL:
        try:
            data = load_data_from_mysql(db)
            logger.info("Data loaded from MySQL")
            return data
        except Exception as e:
            logger.error(f"Error loading from MySQL: {e}")
            return {}
    else:
        # Original JSON file logic
        if not os.path.exists(PLAYLIST_FILE):
            logger.info("Playlist file not found, starting fresh")
            return {}

        try:
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    logger.warning("Unexpected data format in file. Resetting to empty.")
                    return {}
                logger.info("Data loaded from JSON file")
                return data
        except FileNotFoundError:
            logger.info("Playlist file not found. Starting fresh.")
            return {}
        except json.JSONDecodeError:
            logger.error("Corrupted playlist file (invalid JSON). Resetting data.")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            return {}


def save_data(data):
    """
    Save full users dict to MySQL or JSON file based on USE_MYSQL setting.
    
    Args:
        data: Dictionary containing all users data
    """
    if USE_MYSQL:
        try:
            save_data_to_mysql(db, data)
            logger.info("Data saved to MySQL")
        except Exception as e:
            logger.error(f"Error saving to MySQL: {e}")
    else:
        # Original JSON file logic
        try:
            with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("Data saved to JSON file")
        except PermissionError:
            logger.error("Permission denied when trying to write the playlists file.")
        except Exception as e:
            logger.error(f"Error saving data: {e}")


def close_storage():
    """
    Close any open storage connections (e.g., MySQL).
    """
    if USE_MYSQL and db:
        try:
            db.disconnect()
            logger.info("MySQL connection closed")
        except Exception as e:
            logger.error(f"Error closing MySQL connection: {e}")
