"""
Utility functions for the thermal processor module.
"""

import os
from pathlib import Path

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path (str or Path): Path to the directory
        
    Returns:
        Path: Path to the directory
    """
    directory = Path(directory_path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def get_file_info(file_path):
    """
    Get information about a file.
    
    Args:
        file_path (str or Path): Path to the file
        
    Returns:
        dict: Dictionary containing file information
    """
    path = Path(file_path)
    
    return {
        'path': str(path),
        'name': path.name,
        'stem': path.stem,
        'extension': path.suffix,
        'size': path.stat().st_size if path.exists() else None,
        'directory': str(path.parent),
        'exists': path.exists()
    }

def format_file_size(size_in_bytes):
    """
    Format file size in human-readable format.
    
    Args:
        size_in_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"