"""
Configuration module for Playlist Manager
Centralized configuration management
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Storage Configuration
USE_MYSQL = True  # Set to False to use JSON file storage

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # CHANGE THIS
    'database': 'playlist_db'
}

JSON_CONFIG = {
    'file_path': PROJECT_ROOT / 'playlists.json',
    'encoding': 'utf-8'
}

# Default Playlists
DEFAULT_PLAYLISTS = {
    "happy": ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake", "Uptown Funk - Bruno Mars"],
    "sad": ["Someone Like You - Adele", "Let Her Go - Passenger", "Fix You - Coldplay"],
    "energetic": ["Stronger - Kanye West", "Eye of the Tiger - Survivor", "Titanium - David Guetta ft. Sia"],
    "calm": ["Weightless - Marconi Union", "River Flows in You - Yiruma", "Sunrise - Norah Jones"]
}

# Export Configuration
EXPORT_CONFIG = {
    'default_dir': PROJECT_ROOT / 'exports',
    'formats': ['txt', 'csv', 'json']
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}