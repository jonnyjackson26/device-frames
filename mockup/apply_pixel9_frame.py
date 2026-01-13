#!/usr/bin/env python3
"""
Apply Pixel 9 Pro XL Rose Quartz frame to a screenshot.

This script reads a screenshot and composites it with the 
Pixel 9 Pro XL Rose Quartz device frame.
"""

import json
from pathlib import Path
from PIL import Image


def apply_frame_to_screenshot(screenshot_path, template_path, output_path):
    """
    Apply device frame to screenshot.
    
    Args:
        screenshot_path: Path to the screenshot image
        template_path: Path to the device template.json
        output_path: Path to save the framed screenshot
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
    
    print(f"Frame size: {template['frameSize']['width']}x{template['frameSize']['height']}")
    print(f"Screen region: {screen['width']}x{screen['height']} at ({screen['x']}, {screen['y']})")
    print(f"Original screenshot: {screenshot.size}")
    
    # Resize screenshot to match screen dimensions
    screenshot_resized = screenshot.resize(
        (screen["width"], screen["height"]),
        Image.Resampling.LANCZOS
    )
    
    print(f"Resized screenshot: {screenshot_resized.size}")
    
    # Create composite with proper layering and masking
    # 1. Create a transparent canvas the size of the frame
    composite = Image.new('RGBA', (template['frameSize']['width'], template['frameSize']['height']), (0, 0, 0, 0))
    
    # 2. Paste the screenshot at the screen position, using mask to control visibility
    # This ensures screenshot only shows in the screen area defined by the mask
    composite.paste(screenshot_resized, (screen["x"], screen["y"]))
    
    # 3. Apply the mask to the entire composite (mask defines screen area)
    composite.putalpha(mask)
    
    # 4. Paste the frame on top (frame has transparency in screen area)
    composite.paste(frame, (0, 0), frame)
    
    # Save result
    composite.save(output_path)
    print(f"\nFramed screenshot saved to: {output_path}")
    print(f"Output size: {composite.size}")
    
    return output_path


if __name__ == "__main__":
    # Define paths
    screenshot_path = Path("/workspaces/device-frames/test-screenshots/pixel-9-pro-xl.png")
    template_path = Path("/workspaces/device-frames/output/android-phone/Pixel 9 Pro XL/Rose Quartz/template.json")
    output_path = Path("/workspaces/device-frames/mockup/pixel-9-pro-xl-rose-quartz-framed.png")
    
    # Check if screenshot exists
    if not screenshot_path.exists():
        print(f"Error: Screenshot not found at {screenshot_path}")
        exit(1)
    
    # Check if template exists
    if not template_path.exists():
        print(f"Error: Template not found at {template_path}")
        print("Please run process_frames.py first to generate device templates.")
        exit(1)
    
    # Apply frame
    print("Applying Pixel 9 Pro XL Rose Quartz frame...")
    print(f"Screenshot: {screenshot_path}")
    print(f"Template: {template_path}")
    print()
    
    apply_frame_to_screenshot(screenshot_path, template_path, output_path)
