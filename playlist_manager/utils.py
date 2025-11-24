"""
Utility functions for Playlist Manager
Includes logging setup and helper functions.
"""

import logging
import sys
from pathlib import Path

# Global logger instance
_logger = None


def setup_logging(log_file='playlist.log', level=logging.INFO):
    """
    Configure logging for the application.

    Args:
        log_file: Path to log file (default: 'playlist.log')
        level: Logging level (default: logging.INFO)

    Returns:
        Configured logger instance
    """
    global _logger

    if _logger is not None:
        return _logger

    # Create logger
    _logger = logging.getLogger('playlist_manager')
    _logger.setLevel(level)

    # Prevent duplicate handlers
    if _logger.handlers:
        return _logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler - detailed logs
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(detailed_formatter)
    _logger.addHandler(file_handler)

    # Console handler - simple logs (optional, for debugging)
    # Uncomment if you want to see logs in console as well
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setLevel(logging.WARNING)
    # console_handler.setFormatter(simple_formatter)
    # _logger.addHandler(console_handler)

    _logger.info("="*50)
    _logger.info("Playlist Manager started")
    _logger.info("="*50)

    return _logger


def get_logger():
    """
    Get the application logger instance.

    Returns:
        Logger instance (creates one if not exists)
    """
    global _logger
    if _logger is None:
        return setup_logging()
    return _logger


def safe_int_input(prompt, min_value=None, max_value=None, logger=None):
    """
    Get an integer from user with validation.

    Args:
        prompt: Input prompt to display
        min_value: Minimum allowed value (optional)
        max_value: Maximum allowed value (optional)
        logger: Logger instance for logging errors (optional)

    Returns:
        Valid integer input from user
    """
    if logger is None:
        logger = get_logger()

    while True:
        val = input(prompt).strip()
        try:
            i = int(val)
        except ValueError:
            error_msg = "Please enter a valid integer."
            print(f"❌ {error_msg}")
            logger.warning(f"Invalid integer input: {val}")
            continue

        if (min_value is not None and i < min_value) or (max_value is not None and i > max_value):
            error_msg = f"Please enter a number between {min_value} and {max_value}."
            print(f"❌ {error_msg}")
            logger.warning(f"Input out of range: {i} (expected {min_value}-{max_value})")
            continue

        return i


def log_error(message, exception=None):
    """
    Log an error message with optional exception.

    Args:
        message: Error message
        exception: Exception object (optional)
    """
    logger = get_logger()
    if exception:
        logger.error(f"{message}: {str(exception)}", exc_info=True)
    else:
        logger.error(message)


def log_info(message):
    """
    Log an informational message.

    Args:
        message: Info message
    """
    logger = get_logger()
    logger.info(message)


def log_warning(message):
    """
    Log a warning message.

    Args:
        message: Warning message
    """
    logger = get_logger()
    logger.warning(message)
