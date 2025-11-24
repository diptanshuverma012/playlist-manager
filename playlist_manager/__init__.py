"""
Playlist Manager Package
A modular playlist management system with MySQL and JSON storage support.
"""

__version__ = "1.0.0"
__author__ = "diptanshuverma012"

# Package-level imports for convenience
from .user import User
from .storage import load_data, save_data
from .main import main

__all__ = ['User', 'load_data', 'save_data', 'main']
