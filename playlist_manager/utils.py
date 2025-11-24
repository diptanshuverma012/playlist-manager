"""
Utility functions for the Playlist Manager.
Contains helper functions used throughout the application.
"""

import logging

logger = logging.getLogger(__name__)


def safe_int_input(prompt, min_value=None, max_value=None):
    """
    Get an integer from user with validation.
    
    Args:
        prompt: String to display to the user
        min_value: Optional minimum acceptable value
        max_value: Optional maximum acceptable value
    
    Returns:
        int: Valid integer input from user
    """
    while True:
        val = input(prompt).strip()
        try:
            i = int(val)
        except ValueError:
            logger.error("Invalid integer input")
            print("❌ Please enter a valid integer.")
            continue
        if (min_value is not None and i < min_value) or (max_value is not None and i > max_value):
            logger.error(f"Integer out of range: {i} (min={min_value}, max={max_value})")
            print(f"❌ Please enter a number between {min_value} and {max_value}.")
            continue
        return i
