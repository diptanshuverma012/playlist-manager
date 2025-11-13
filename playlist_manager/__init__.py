"""
Playlist Manager Package
A modular playlist management system with MySQL and JSON support.
"""

__version__ = "1.0.0"
__author__ = "diptanshuverma012"

from .user import User
from .storage import load_data, save_data
from .ui import show_all_playlists, playlist_manager, update_password, login
from .utils import safe_int_input, setup_logging, get_logger

__all__ = [
    'User',
    'load_data',
    'save_data',
    'show_all_playlists',
    'playlist_manager',
    'update_password',
    'login',
    'safe_int_input',
    'setup_logging',
    'get_logger'
]
