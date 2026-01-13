#!/usr/bin/env python3


import json
from pathlib import Path
from PIL import Image, ImageFilter


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
    
    # Convert screenshot to RGBA for proper alpha blending
    if screenshot_resized.mode != 'RGBA':
        screenshot_resized = screenshot_resized.convert('RGBA')
    
    print(f"Resized screenshot: {screenshot_resized.size}")
    
    # Extract the mask region for the screenshot area
    mask_region = mask.crop((screen["x"], screen["y"], 
                              screen["x"] + screen["width"], 
                              screen["y"] + screen["height"]))

    # Slightly dilate the mask to avoid subpixel gaps at rounded corners / notches
    mask_region = mask_region.filter(ImageFilter.MaxFilter(3))
    
    # Apply the mask to the screenshot as its alpha channel (cuts screenshot to frame shape)
    screenshot_resized.putalpha(mask_region)
    
    # Create composite: transparent canvas, paste masked screenshot, paste frame on top
    composite = Image.new('RGBA', (template['frameSize']['width'], template['frameSize']['height']), (0, 0, 0, 0))
    composite.paste(screenshot_resized, (screen["x"], screen["y"]), screenshot_resized)
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
