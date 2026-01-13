"""
Color parsing utilities.
"""

from typing import Union, Tuple


def parse_color(color_str: str) -> Union[Tuple[int, int, int, int], Tuple[int, int, int]]:
    """
    Parse a color string to RGBA or RGB tuple.
    
    Supports:
    - Empty string or 'transparent': RGBA with alpha=0
    - Hex colors: '#RRGGBB' or '#RRGGBBAA'
    
    Args:
        color_str: Color string to parse
        
    Returns:
        RGB or RGBA tuple
        
    Raises:
        ValueError: If color format is invalid
    """
    color_str = color_str.strip()
    
    if not color_str or color_str.lower() == 'transparent':
        return (0, 0, 0, 0)
    
    if color_str.startswith('#'):
        color_str = color_str.lstrip('#')
        if len(color_str) == 6:
            r, g, b = tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
            return (r, g, b)
        elif len(color_str) == 8:
            r, g, b, a = tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4, 6))
            return (r, g, b, a)
    
    raise ValueError(f"Invalid color: {color_str}. Use hex (#RRGGBB or #RRGGBBAA) or empty/transparent")
