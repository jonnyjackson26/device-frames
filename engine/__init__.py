"""
Device Frame Engine

Pure rendering logic for applying device frames to screenshots.
No HTTP, CLI, or I/O dependencies.
"""

from .render import apply_frame_to_screenshot
from .color import parse_color
from .templates import find_template, sanitize_filename

__all__ = [
    'apply_frame_to_screenshot',
    'parse_color',
    'find_template',
    'sanitize_filename',
]
