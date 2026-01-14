"""
Core frame application logic for applying device frames to screenshots.
"""

import json
from pathlib import Path
from typing import Union, Tuple
from PIL import Image, ImageFilter


def apply_frame_to_screenshot(
    screenshot_path: Path, 
    template_path: Path, 
    output_path: Path, 
    background_color: Union[Tuple[int, int, int, int], Tuple[int, int, int]] = (0, 0, 0, 0)
) -> Path:
    """
    Apply device frame to screenshot.
    
    This function:
    1. Loads the template configuration (frame, mask, screen bounds)
    2. Resizes the screenshot to match the screen dimensions
    3. Applies the mask to cut the screenshot to the device's screen shape
    4. Composites the masked screenshot onto a background
    5. Overlays the device frame
    
    Args:
        screenshot_path: Path to the screenshot image
        template_path: Path to the device template.json
        output_path: Path to save the framed screenshot
        background_color: Background color as RGBA or RGB tuple (default: transparent)
        
    Returns:
        Path to the saved output image
        
    Raises:
        FileNotFoundError: If template, frame, mask, or screenshot files are missing
        ValueError: If template structure is invalid
    """
    # Load template
    with open(template_path) as f:
        template = json.load(f)
    
    frame_dir = template_path.parent
    
    # Load images
    frame = Image.open(frame_dir / template["frame"])
    mask = Image.open(frame_dir / template["mask"])
    screenshot = Image.open(screenshot_path)
    
    # Get screen bounds
    screen = template["screen"]
    
    # Resize screenshot to match screen dimensions
    screenshot_resized = screenshot.resize(
        (screen["width"], screen["height"]),
        Image.Resampling.LANCZOS
    )
    
    # Convert screenshot to RGBA for proper alpha blending
    if screenshot_resized.mode != 'RGBA':
        screenshot_resized = screenshot_resized.convert('RGBA')
    
    # Extract the mask region for the screenshot area
    mask_region = mask.crop((
        screen["x"], 
        screen["y"], 
        screen["x"] + screen["width"], 
        screen["y"] + screen["height"]
    ))

    # Slightly dilate the mask to avoid subpixel gaps at rounded corners / notches
    mask_region = mask_region.filter(ImageFilter.MaxFilter(3))
    
    # Apply the mask to the screenshot as its alpha channel (cuts screenshot to frame shape)
    screenshot_resized.putalpha(mask_region)
    
    # Create composite: canvas with background color, paste masked screenshot, paste frame on top
    composite = Image.new(
        'RGBA', 
        (template['frameSize']['width'], template['frameSize']['height']), 
        background_color
    )
    composite.paste(screenshot_resized, (screen["x"], screen["y"]), screenshot_resized)
    composite.paste(frame, (0, 0), frame)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save result
    composite.save(output_path)
    
    return output_path
