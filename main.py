"""
Playlist Manager - Main Entry Point
POM (Page Object Model) Architecture

Version: 2.0.0
"""

import sys
from config.config import Config
from src.database.db_handler import PlaylistDatabase
from src.services.data_service import DataService
from src.services.auth_service import AuthService
from src.services.playlist_service import PlaylistService
from src.services.export_service import ExportService
from src.ui.menu import MenuUI


def initialize_database():
    """
    Initialize database connection if using MySQL.
    
    Returns:
        PlaylistDatabase instance or None
    """
    if not Config.USE_MYSQL:
        return None
    
    try:
        db = PlaylistDatabase(**Config.MYSQL_CONFIG)
        
        # Create database if it doesn't exist
        print("🔧 Setting up database...")
        db.create_database()
        
        # Connect to database
        if not db.connect():
            print("❌ Failed to connect to database!")
            print("💡 Tip: Check your MySQL credentials in config/config.py")
            return None
        
        # Create table if it doesn't exist
        db.create_table()
        
        print("✅ Database initialized successfully!")
        return db
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("💡 Falling back to JSON file storage...")
        return None


def main():
    """Main application entry point."""
    try:
        # Initialize database (if using MySQL)
        db = initialize_database()
        
        # If MySQL failed and was supposed to be used, offer to use JSON instead
        if Config.USE_MYSQL and db is None:
            choice = input("\nWould you like to use JSON file storage instead? (yes/no): ").strip().lower()
            if choice != 'yes':
                print("❌ Cannot proceed without a data storage method.")
                sys.exit(1)
            # Continue with JSON (db will be None)
        
        # Initialize services
        data_service = DataService(db)
        auth_service = AuthService(data_service)
        playlist_service = PlaylistService(data_service)
        export_service = ExportService()
        
        # Initialize and run UI
        menu = MenuUI(auth_service, playlist_service, export_service)
        menu.run()
        
        # Clean up
        if db:
            db.disconnect()
        
        print("\n✅ Application closed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Application interrupted by user!")
        if db:
            db.disconnect()
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if db:
            db.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    main()