# 🎵 Playlist Manager

A Python-based playlist management system with MySQL & JSON support using POM (Python Object Model) architecture.

## 📋 Project Structure

```
playlist-manager/
├── playlist_manager/          # Main package (modular structure)
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Entry point and main application logic
│   ├── user.py               # User class and authentication
│   ├── storage.py            # Data persistence (MySQL/JSON)
│   ├── ui.py                 # User interface functions
│   └── utils.py              # Helper functions and utilities
├── tests/                     # Unit tests (pytest)
│   ├── __init__.py
│   ├── test_add_delete_song.py
│   ├── test_create_mood.py
│   ├── test_rename_mood.py
│   ├── test_search_song.py
│   └── test_surprise_me.py
├── POM.PY                     # Python Object Model Configuration
├── config.py                  # Centralized Configuration
├── database.py                # MySQL Database Handler
├── run.py                     # Application entry point
├── requirements.txt           # Python Dependencies
├── playlists.json             # Default JSON Storage
├── playlist.log               # Application logs
├── .gitignore                # Git Ignore Rules
└── README.md                 # Documentation
```

## 🆕 What's New (v1.0.0)

### Modular Architecture
- **Separated concerns**: Code is now organized into focused modules
- **main.py**: Entry point and authentication logic
- **user.py**: User class with all playlist operations
- **storage.py**: Data persistence layer (MySQL/JSON abstraction)
- **ui.py**: User interface and menu handling
- **utils.py**: Reusable utility functions

### Logging System
- **Comprehensive logging** using Python's `logging` library
- **Log file**: All operations logged to `playlist.log`
- **Log format**: Timestamp, module, level, and message
- **Error tracking**: All errors are properly logged for debugging

### Unit Testing
- **81 comprehensive tests** covering all major functionality
- **Test coverage**: Add/delete songs, create/rename moods, search, surprise me
- **pytest framework**: Professional testing with setup/teardown
- **Edge cases**: Thorough testing of error conditions and boundaries

### Enhanced POM.py
- **validate_environment()**: Checks Python version and dependencies
- **generate_requirements()**: Auto-generates requirements.txt with versions
- **Validation reporting**: Clear feedback on environment readiness

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/diptanshuverma012/playlist-manager.git
cd playlist-manager
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL (Optional)
Edit `config.py`:
```python
USE_MYSQL = True  # Set to False to use JSON storage

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'playlist_db'
}
```

### 4. Run Application
```bash
python run.py
```

### 5. Run Tests
```bash
pytest tests/ -v
```

## ✨ Features

✅ User Authentication  
✅ Create/Manage Playlists by Mood  
✅ Add/Delete/Rename Songs  
✅ Search Functionality  
✅ Favorite Mood Support  
✅ Export to TXT/CSV/JSON  
✅ MySQL & JSON Storage  
✅ Statistics Dashboard  
✅ **NEW**: Comprehensive logging  
✅ **NEW**: Unit testing suite  
✅ **NEW**: Modular architecture  

## 🔧 Configuration (config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| USE_MYSQL | True | Use MySQL (False = JSON) |
| MYSQL_CONFIG | localhost | Database credentials |
| DEFAULT_PLAYLISTS | 4 moods | Initial playlists |

## 📦 POM Model

### View Project Info
```bash
python POM.PY
```

### Validate Environment
The POM.py script automatically:
- Checks Python version (3.7+ required)
- Validates dependencies are installed
- Reports missing packages
- Generates requirements.txt

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_add_delete_song.py -v
```

### Test Coverage
```bash
pytest tests/ --cov=playlist_manager --cov-report=html
```

## 📚 Module Documentation

### playlist_manager.user
Contains the `User` class with methods for:
- Playlist operations (create, rename, delete)
- Song management (add, delete, rename, search)
- Statistics and export functionality

### playlist_manager.storage
Handles data persistence:
- Abstracts MySQL and JSON storage
- Automatic fallback to JSON if MySQL unavailable
- Transaction-safe data operations

### playlist_manager.ui
User interface components:
- Menu systems
- Input handling
- Display formatting

### playlist_manager.utils
Utility functions:
- Input validation
- Helper methods

## 🔍 Logging

Logs are written to `playlist.log` with format:
```
2025-11-24 12:34:56,789 - module.name - LEVEL - Message
```

**Log Levels:**
- INFO: Normal operations (login, song additions, etc.)
- WARNING: Non-critical issues
- ERROR: Errors that don't stop execution

## 📝 Development Guidelines

### Adding New Features
1. Add functionality to appropriate module
2. Add docstrings to all new functions/classes
3. Follow PEP 8 style guidelines
4. Write unit tests for new features
5. Update logging as appropriate

### Code Style
- Follow PEP 8
- Use descriptive variable names
- Add type hints where applicable
- Document all public methods

## 🔒 Data Persistence

### JSON Storage
- Default storage method
- File: `playlists.json`
- Human-readable format
- Easy backup and version control

### MySQL Storage
- Optional high-performance storage
- JSON data type for flexibility
- Automatic table creation
- Connection pooling support

## 🆘 Troubleshooting

### MySQL Connection Issues
```python
# In config.py, switch to JSON storage:
USE_MYSQL = False
```

### Missing Dependencies
```bash
python POM.PY  # Validates environment
pip install -r requirements.txt
```

### Permission Errors
Ensure write permissions for:
- `playlists.json`
- `playlist.log`

## 📝 License

MIT - 2025

## 👤 Author

**diptanshuverma012**

## 🙏 Acknowledgments

- Built with Python 3.12+
- Uses pytest for testing
- MySQL connector for database support