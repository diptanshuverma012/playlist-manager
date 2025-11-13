"""
POM (Page Object Model) - Python version for Playlist Manager
Organizes project structure and dependencies
"""

import sys
import subprocess
from pathlib import Path


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
            {"name": "pytest-cov", "version": "4.1.0"},
            {"name": "unittest", "version": "builtin"},
        ],
        "development": [
            {"name": "black", "version": "23.0.0"},
            {"name": "pylint", "version": "2.17.0"},
        ]
    }
    
    SOURCE_STRUCTURE = {
        "playlist_manager": {
            "modules": [
                "__init__.py",
                "main.py",
                "user.py",
                "storage.py",
                "ui.py",
                "utils.py"
            ]
        },
        "tests": {
            "test_files": [
                "__init__.py",
                "conftest.py",
                "test_add_delete_song.py",
                "test_create_mood.py",
                "test_rename_mood.py",
                "test_search_song.py",
                "test_surprise_me.py"
            ]
        },
        "config": [
            "config.py",
            "database.py"
        ],
        "resources": [
            "playlists.json",
            "playlist.log"
        ]
    }

    BUILD_CONFIG = {
        "python_version": "3.8+",
        "python_version_min": (3, 8),
        "entry_point": "playlist_manager/main.py",
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
Testing Dependencies: {len(cls.DEPENDENCIES['testing'])}
Development Dependencies: {len(cls.DEPENDENCIES['development'])}
"""

    @classmethod
    def validate_environment(cls):
        """
        Validate the environment meets all requirements.
        Checks Python version and required dependencies.

        Returns:
            Tuple of (success: bool, messages: list)
        """
        messages = []
        success = True

        # Check Python version
        messages.append("=" * 60)
        messages.append("🔍 Validating Environment")
        messages.append("=" * 60)

        current_version = sys.version_info
        min_version = cls.BUILD_CONFIG['python_version_min']

        messages.append(f"\n✓ Python Version Check:")
        messages.append(f"  Current: {current_version.major}.{current_version.minor}.{current_version.micro}")
        messages.append(f"  Required: {min_version[0]}.{min_version[1]}+")

        if current_version < min_version:
            messages.append(f"  ❌ FAIL: Python {min_version[0]}.{min_version[1]}+ required")
            success = False
        else:
            messages.append(f"  ✅ PASS")

        # Check runtime dependencies
        messages.append(f"\n✓ Runtime Dependencies:")
        for dep in cls.DEPENDENCIES['runtime']:
            name = dep['name']
            version = dep['version']

            if version == "builtin":
                messages.append(f"  ✅ {name} (builtin)")
            else:
                try:
                    # Try to import the package
                    if name == "mysql-connector-python":
                        import mysql.connector
                        messages.append(f"  ✅ {name} {version}")
                    else:
                        __import__(name)
                        messages.append(f"  ✅ {name} {version}")
                except ImportError:
                    messages.append(f"  ⚠️  {name} {version} (not installed - optional for JSON mode)")
                    # Don't fail for mysql-connector as it's optional
                    if name != "mysql-connector-python":
                        success = False

        # Check testing dependencies
        messages.append(f"\n✓ Testing Dependencies:")
        for dep in cls.DEPENDENCIES['testing']:
            name = dep['name']
            version = dep['version']

            if version == "builtin":
                messages.append(f"  ✅ {name} (builtin)")
            else:
                try:
                    __import__(name.replace('-', '_'))
                    messages.append(f"  ✅ {name} {version}")
                except ImportError:
                    messages.append(f"  ⚠️  {name} {version} (not installed)")
                    # Testing deps are optional

        # Check development dependencies
        messages.append(f"\n✓ Development Dependencies:")
        for dep in cls.DEPENDENCIES['development']:
            name = dep['name']
            version = dep['version']

            try:
                __import__(name)
                messages.append(f"  ✅ {name} {version}")
            except ImportError:
                messages.append(f"  ⚠️  {name} {version} (not installed)")
                # Dev deps are optional

        messages.append("\n" + "=" * 60)
        if success:
            messages.append("✅ Environment validation PASSED")
        else:
            messages.append("❌ Environment validation FAILED")
        messages.append("=" * 60)

        return success, messages

    @classmethod
    def generate_requirements(cls, output_file="requirements.txt"):
        """
        Generate requirements.txt file with runtime dependencies.

        Args:
            output_file: Path to output requirements file

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            requirements = []

            # Add header
            requirements.append("# Playlist Manager - Runtime Dependencies")
            requirements.append(f"# Generated by POM.py")
            requirements.append(f"# Project: {cls.PROJECT['name']} v{cls.PROJECT['version']}")
            requirements.append("")

            # Add runtime dependencies
            requirements.append("# Runtime Dependencies")
            for dep in cls.DEPENDENCIES['runtime']:
                name = dep['name']
                version = dep['version']
                if version != "builtin":
                    requirements.append(f"{name}>={version}")

            requirements.append("")
            requirements.append("# Testing Dependencies")
            for dep in cls.DEPENDENCIES['testing']:
                name = dep['name']
                version = dep['version']
                if version != "builtin":
                    requirements.append(f"{name}>={version}")

            requirements.append("")
            requirements.append("# Development Dependencies (optional)")
            for dep in cls.DEPENDENCIES['development']:
                name = dep['name']
                version = dep['version']
                if version != "builtin":
                    requirements.append(f"# {name}>={version}")

            # Write to file
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(requirements))

            return True, f"✅ Requirements file generated: {output_file}"

        except Exception as e:
            return False, f"❌ Failed to generate requirements: {str(e)}"


if __name__ == "__main__":
    print(POMConfig.get_info())

    # Run environment validation
    success, messages = POMConfig.validate_environment()
    for msg in messages:
        print(msg)

    # Generate requirements file
    print("\n")
    success, message = POMConfig.generate_requirements()
    print(message)