#!/usr/bin/env python3
"""
Entry point for the Playlist Manager application.
This file provides backward compatibility and imports from the new modular structure.
"""

import sys
import os

# Add the current directory to the Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playlist_manager.main import main

if __name__ == "__main__":
    main()
