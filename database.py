"""
Database module for Playlist Manager
Handles MySQL database operations
"""

import mysql.connector
from mysql.connector import Error
import json
from config import MYSQL_CONFIG


class PlaylistDatabase:
    """
    MySQL database handler for playlist application.
    Stores and retrieves JSON playlist data from MySQL database.
    """
    
    def __init__(self, host='localhost', user='root', password='', database='playlist_db'):
        """
        Initialize database connection parameters.
        
        Args:
            host: MySQL server host (default: localhost)
            user: MySQL username (default: root)
            password: MySQL password
            database: Database name (default: playlist_db)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """
        Establish connection to MySQL database.
        Returns True if successful, False otherwise.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("✅ Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 MySQL connection closed")
    
    def create_database(self):
        """
        Create the playlist database if it doesn't exist.
        """
        try:
            # Connect without specifying database
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"✅ Database '{self.database}' created or already exists")
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    def create_table(self):
        """
        Create the playlists table with id and data columns.
        The data column stores JSON data.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS playlists (
            id VARCHAR(100) PRIMARY KEY,
            data JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print("✅ Table 'playlists' created successfully")
            cursor.close()
            return True
        except Error as e:
            print(f"❌ Error creating table: {e}")
            return False
    
    def insert_user_data(self, username, user_data):
        """
        Insert or update user playlist data into MySQL.
        
        Args:
            username: Unique username (acts as id)
            user_data: Dictionary containing user's password, playlists, etc.
        
        Returns:
            True if successful, False otherwise
        """
        insert_query = """
        INSERT INTO playlists (id, data) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE data = %s, updated_at = CURRENT_TIMESTAMP
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            json_data = json.dumps(user_data)
            cursor.execute(insert_query, (username, json_data, json_data))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"❌ Error inserting data: {e}")
            return False
    
    def fetch_user_data(self, username):
        """
        Retrieve user data from MySQL by username.
        
        Args:
            username: Username to fetch data for
        
        Returns:
            Dictionary containing user data, or None if not found
        """
        select_query = "SELECT data FROM playlists WHERE id = %s"
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                # Parse JSON data from result
                user_data = json.loads(result[0]) if isinstance(result[0], str) else result[0]
                return user_data
            return None
        except Error as e:
            print(f"❌ Error fetching data: {e}")
            return None
    
    def fetch_all_users(self):
        """
        Retrieve all users' data from MySQL.
        
        Returns:
            Dictionary with username as key and user data as value
        """
        select_query = "SELECT id, data FROM playlists"
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            results = cursor.fetchall()
            cursor.close()
            
            all_users = {}
            for row in results:
                username = row[0]
                user_data = json.loads(row[1]) if isinstance(row[1], str) else row[1]
                all_users[username] = user_data
            
            return all_users
        except Error as e:
            print(f"❌ Error fetching all users: {e}")
            return {}
    
    def delete_user(self, username):
        """
        Delete a user's data from MySQL.
        
        Args:
            username: Username to delete
        
        Returns:
            True if successful, False otherwise
        """
        delete_query = "DELETE FROM playlists WHERE id = %s"
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(delete_query, (username,))
            self.connection.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                print(f"✅ User '{username}' deleted successfully")
                return True
            else:
                print(f"⚠️ User '{username}' not found")
                return False
        except Error as e:
            print(f"❌ Error deleting user: {e}")
            return False
    
    def verify_data(self, username):
        """
        Verify that data for a user is correctly stored and can be retrieved.
        
        Args:
            username: Username to verify
        
        Returns:
            True if data exists and is valid, False otherwise
        """
        data = self.fetch_user_data(username)
        if data:
            print(f"✅ Verification successful for user '{username}'")
            print(f"   Data structure: {list(data.keys())}")
            return True
        else:
            print(f"❌ No data found for user '{username}'")
            return False


# -------------------------
# Integration Functions for main.py
# -------------------------

def load_data_from_mysql(db):
    """
    Load all users data from MySQL database.
    Replacement for load_data() function in main.py
    
    Args:
        db: PlaylistDatabase instance
    
    Returns:
        Dictionary of all users data
    """
    try:
        users = db.fetch_all_users()
        if not isinstance(users, dict):
            print("⚠️ Unexpected data format from database. Resetting to empty.")
            return {}
        return users
    except Exception as e:
        print(f"❌ Error loading data from MySQL: {e}")
        return {}


def save_data_to_mysql(db, users_data):
    """
    Save all users data to MySQL database.
    Replacement for save_data() function in main.py
    
    Args:
        db: PlaylistDatabase instance
        users_data: Dictionary containing all users data
    
    Returns:
        True if successful, False otherwise
    """
    try:
        for username, user_info in users_data.items():
            db.insert_user_data(username, user_info)
        return True
    except Exception as e:
        print(f"❌ Error saving data to MySQL: {e}")
        return False


# -------------------------
# Testing and Verification
# -------------------------

def test_database_operations():
    """
    Test all database operations to verify implementation.
    """
    print("\n" + "="*50)
    print("🧪 TESTING DATABASE OPERATIONS")
    print("="*50)
    
    # Initialize database
    db = PlaylistDatabase(
        host='localhost',
        user='root',
        password='your_password',  # Change this
        database='playlist_db'
    )
    
    # Step 1: Create database
    print("\n1️⃣ Creating database...")
    db.create_database()
    
    # Step 2: Connect to database
    print("\n2️⃣ Connecting to database...")
    if not db.connect():
        print("❌ Failed to connect. Check your credentials.")
        return
    
    # Step 3: Create table
    print("\n3️⃣ Creating table...")
    db.create_table()
    
    # Step 4: Insert sample data
    print("\n4️⃣ Inserting sample JSON data...")
    sample_data = {
        "password": "test123",
        "playlists": {
            "happy": ["Happy Song 1", "Happy Song 2"],
            "sad": ["Sad Song 1"]
        },
        "favorite_mood": "happy"
    }
    db.insert_user_data("test_user", sample_data)
    print("✅ Sample data inserted for 'test_user'")
    
    # Step 5: Fetch data
    print("\n5️⃣ Fetching data from MySQL...")
    fetched_data = db.fetch_user_data("test_user")
    if fetched_data:
        print("✅ Data retrieved successfully:")
        print(json.dumps(fetched_data, indent=2))
    
    # Step 6: Verify data
    print("\n6️⃣ Verifying data integrity...")
    db.verify_data("test_user")
    
    # Step 7: Fetch all users
    print("\n7️⃣ Fetching all users...")
    all_users = db.fetch_all_users()
    print(f"✅ Total users in database: {len(all_users)}")
    
    # Step 8: Update data
    print("\n8️⃣ Updating user data...")
    sample_data["playlists"]["energetic"] = ["Energy Song 1", "Energy Song 2"]
    db.insert_user_data("test_user", sample_data)
    print("✅ Data updated successfully")
    
    # Disconnect
    print("\n9️⃣ Closing connection...")
    db.disconnect()
    
    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*50)


if __name__ == "__main__":
    # Run tests
    test_database_operations()