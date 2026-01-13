"""
Template discovery utilities.
"""

from pathlib import Path
from typing import List, Optional, Tuple


def find_template(output_root: Path, device_type: str, device_variation: str) -> Tuple[Optional[Path], List[Path]]:
    """
    Find template.json for a specific device type and variation.
    
    Args:
        output_root: Root directory containing device templates
        device_type: Device type directory name (e.g., '16 Pro Max')
        device_variation: Device variation directory name (e.g., 'Blue Titanium')
        
    Returns:
        Tuple of (first matching template path or None, all matching template paths)
    """
    pattern = f"{device_type}/{device_variation}/template.json"
    matches = list(output_root.rglob(pattern))
    if not matches:
        return None, []
    return matches[0], matches


def sanitize_filename(text: str) -> str:
    """
    Sanitize text for use in filenames.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text with spaces replaced by hyphens
    """
    return text.replace(" ", "-")
