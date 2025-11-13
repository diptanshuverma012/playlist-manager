# Playlist Manager - Refactored

A well-structured, maintainable, and testable playlist management application with MySQL and JSON storage support.

## Project Structure

```
playlist-manager/
├── playlist_manager/          # Main package
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Application entry point
│   ├── user.py               # User class with playlist operations
│   ├── storage.py            # Data persistence (MySQL/JSON)
│   ├── ui.py                 # User interface functions
│   └── utils.py              # Utility functions and logging
│
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_add_delete_song.py
│   ├── test_create_mood.py
│   ├── test_rename_mood.py
│   ├── test_search_song.py
│   └── test_surprise_me.py
│
├── config.py                 # Configuration settings
├── database.py              # MySQL database handler
├── POM.PY                   # Project Object Model with validation
├── run.py                   # Simple entry point script
├── requirements.txt         # Python dependencies
└── playlist.log            # Application logs
```

## Features

### Improved Maintainability
- **Modular Architecture**: Separated concerns into logical modules
- **Clear Separation**: User logic, storage, UI, and utilities are distinct
- **Single Responsibility**: Each module has a specific purpose

### Enhanced Testability
- **76 Unit Tests**: Comprehensive test coverage
- **Pytest Framework**: Industry-standard testing
- **Isolated Tests**: Each test is independent and reproducible
- **Fixtures**: Reusable test data and setup

### Better Structure
- **Package Organization**: Proper Python package structure
- **Type Hints**: Clear function signatures (where appropriate)
- **Docstrings**: Comprehensive documentation for all functions
- **Error Handling**: Robust exception handling throughout

### Logging System
- **File Logging**: All operations logged to `playlist.log`
- **Structured Logs**: Timestamp, level, and detailed messages
- **Error Tracking**: Comprehensive error logging with context
- **User Action Logs**: Track all user operations

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd playlist-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Validate environment** (optional)
   ```bash
   python POM.PY
   ```

## Running the Application

### Option 1: Using the run script
```bash
python run.py
```

### Option 2: Running the module directly
```bash
python -m playlist_manager.main
```

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_add_delete_song.py -v
```

### Run with coverage report
```bash
pytest tests/ --cov=playlist_manager --cov-report=html
```

## Configuration

Edit `config.py` to customize:

- **Storage Type**: Set `USE_MYSQL = False` for JSON, `True` for MySQL
- **MySQL Settings**: Configure host, user, password, database
- **JSON File Path**: Customize the JSON storage location
- **Default Playlists**: Modify the default mood categories and songs
- **Logging Level**: Adjust logging verbosity

## Module Descriptions

### `playlist_manager/user.py`
Contains the `User` class with all playlist operations:
- `create_mood()`: Create new mood/playlist
- `add_song()`: Add songs to playlists
- `delete_song()`: Remove songs from playlists
- `rename_song()`: Rename existing songs
- `rename_mood()`: Rename mood categories
- `search_song()`: Search across all playlists
- `surprise_me()`: Get random song
- `playlist_statistics()`: Get playlist stats
- Export functions (TXT, CSV, JSON)

### `playlist_manager/storage.py`
Handles data persistence:
- `load_data()`: Load user data from storage
- `save_data()`: Save user data to storage
- `close_storage()`: Close database connections
- Automatic fallback from MySQL to JSON

### `playlist_manager/ui.py`
User interface functions:
- `login()`: User authentication
- `playlist_manager()`: Main playlist menu
- `update_password()`: Password management
- `show_all_playlists()`: Display all playlists

### `playlist_manager/utils.py`
Utility functions:
- `setup_logging()`: Initialize logging system
- `get_logger()`: Get logger instance
- `safe_int_input()`: Validated integer input
- Helper functions for logging

### `playlist_manager/main.py`
Application orchestration:
- Initializes logging
- Loads configuration
- Handles main menu loop
- Manages application lifecycle

## POM (Project Object Model)

The `POM.PY` module provides:

### `validate_environment()`
Validates that the environment meets all requirements:
- Checks Python version (3.8+)
- Verifies runtime dependencies
- Checks testing dependencies
- Reports development dependencies

### `generate_requirements()`
Automatically generates `requirements.txt` from dependency definitions.

## Logging

All operations are logged to `playlist.log` with:
- Timestamp
- Log level (INFO, WARNING, ERROR)
- Detailed message with context
- User actions and operations
- Error traces for debugging

Example log entries:
```
2025-11-13 10:30:15 - playlist_manager - INFO - User 'john' logged in successfully
2025-11-13 10:31:22 - playlist_manager - INFO - User 'john' added song 'New Song' to mood 'happy'
2025-11-13 10:32:05 - playlist_manager - WARNING - User 'john' attempted to add duplicate song
```

## Test Coverage

**76 tests** covering:

1. **Add/Delete Songs** (15 tests)
   - Add songs to moods
   - Delete by index
   - Duplicate detection
   - Empty playlist handling

2. **Create Mood** (13 tests)
   - Create new moods
   - Duplicate prevention
   - Case-insensitive handling
   - Special characters

3. **Rename Mood** (17 tests)
   - Rename moods
   - Preserve songs
   - Collision detection
   - Chain renaming

4. **Search Songs** (15 tests)
   - Keyword search
   - Case-insensitive
   - Partial matches
   - Cross-mood search

5. **Surprise Me** (16 tests)
   - Random song selection
   - Specific mood selection
   - All moods selection
   - Empty playlist handling

## Benefits of Refactoring

### Before
- Monolithic 750+ line file
- Mixed concerns (UI, logic, storage)
- Difficult to test
- Hard to maintain
- No logging
- No unit tests

### After
- Modular package structure
- Clear separation of concerns
- 76 comprehensive unit tests
- Easy to extend and maintain
- Complete logging system
- Type hints and documentation

## Development

### Adding New Features

1. **Add functionality** to appropriate module:
   - User operations → `user.py`
   - Storage operations → `storage.py`
   - UI/menus → `ui.py`
   - Utilities → `utils.py`

2. **Write tests** in `tests/` directory

3. **Run tests** to ensure everything works:
   ```bash
   pytest tests/ -v
   ```

4. **Update documentation** as needed

### Code Style

- Follow PEP 8 guidelines
- Use docstrings for all functions
- Add type hints where appropriate
- Keep functions focused and small
- Use meaningful variable names

## Troubleshooting

### MySQL Connection Issues
If MySQL is not available, the application automatically falls back to JSON storage. Set `USE_MYSQL = False` in `config.py` to disable MySQL attempts.

### Import Errors
Ensure you're running from the project root directory and have installed all dependencies.

### Test Failures
Run tests with verbose output to identify issues:
```bash
pytest tests/ -v
```

## License

See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Version History

### v1.0.0 (Current)
- Refactored modular architecture
- Added comprehensive unit tests (76 tests)
- Implemented logging system
- Enhanced POM with validation
- Improved error handling
- Better documentation
