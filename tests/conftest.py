"""
Pytest configuration and fixtures for Playlist Manager tests
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from playlist_manager.user import User


@pytest.fixture
def default_playlists():
    """Fixture providing default playlists for testing."""
    return {
        "happy": ["Happy Song 1", "Happy Song 2", "Happy Song 3"],
        "sad": ["Sad Song 1", "Sad Song 2"],
        "energetic": ["Energy Song 1", "Energy Song 2", "Energy Song 3"],
        "calm": ["Calm Song 1"]
    }


@pytest.fixture
def test_user(default_playlists):
    """Fixture providing a test user with default playlists."""
    return User(
        username="test_user",
        password="test_password",
        playlists={k: v.copy() for k, v in default_playlists.items()},
        default_playlists=default_playlists
    )


@pytest.fixture
def empty_user():
    """Fixture providing a user with empty playlists."""
    return User(
        username="empty_user",
        password="test_password",
        playlists={"happy": [], "sad": []},
        default_playlists={}
    )
