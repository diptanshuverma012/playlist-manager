"""
POM (Page Object Model) - Python version for Playlist Manager
Organizes project structure and dependencies
"""

class POMConfig:
    """Project Object Model Configuration"""
    
    PROJECT = {
        "groupId": "com.playlist",
        "artifactId": "playlist-manager",
        "version": "1.0.0",
        "name": "Playlist Manager",
        "description": "Python-based playlist management with MySQL & JSON support",
        "packaging": "python",
        "author": "diptanshuverma012",
        "created": "2025-11-03 08:14:20"
    }
    
    DEPENDENCIES = {
        "runtime": [
            {"name": "mysql-connector-python", "version": "8.0.33"},
            {"name": "json", "version": "builtin"},
            {"name": "csv", "version": "builtin"},
            {"name": "os", "version": "builtin"},
            {"name": "random", "version": "builtin"},
        ],
        "testing": [
            {"name": "pytest", "version": "7.4.0"},
            {"name": "unittest", "version": "builtin"},
        ],
        "development": [
            {"name": "black", "version": "23.0.0"},
            {"name": "pylint", "version": "2.17.0"},
        ]
    }
    
    SOURCE_STRUCTURE = {
        "src": {
            "main": {
                "python": [
                    "main.py",
                    "database.py",
                ]
            },
            "resources": [
                "playlists.json",
                "config.py"
            ]
        }
    }
    
    BUILD_CONFIG = {
        "python_version": "3.8+",
        "entry_point": "main.py",
        "output_dir": "dist/",
        "test_runner": "pytest"
    }
    
    @classmethod
    def get_info(cls):
        """Print POM information"""
        return f"""
🎵 Playlist Manager - POM (Python Object Model)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: {cls.PROJECT['name']} v{cls.PROJECT['version']}
Author: {cls.PROJECT['author']}
Created: {cls.PROJECT['created']}
Python Version: {cls.BUILD_CONFIG['python_version']}
Entry Point: {cls.BUILD_CONFIG['entry_point']}
Runtime Dependencies: {len(cls.DEPENDENCIES['runtime'])}
"""

if __name__ == "__main__":
    print(POMConfig.get_info())