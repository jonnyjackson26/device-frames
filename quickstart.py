#!/usr/bin/env python3
"""
Quick start guide for device frame processing.
"""

import json
from pathlib import Path
from PIL import Image

def example_usage():
    """Example: Load template and display screen info."""
    
    # Path to a generated template
    template_path = Path("output/android-phone/Pixel 8/Hazel/template.json")
    
    # Load template metadata
    with open(template_path) as f:
        template = json.load(f)
    
    # Access screen region
    screen = template["screen"]
    frame_size = template["frameSize"]
    
    print(f"Device: Pixel 8 - Hazel")
    print(f"Frame size: {frame_size['width']}x{frame_size['height']}px")
    print(f"Screen bounds: ({screen['x']}, {screen['y']}) - {screen['width']}x{screen['height']}px")
    
    # Load and inspect mask
    mask_path = Path("output/android-phone/Pixel 8/Hazel/mask.png")
    mask = Image.open(mask_path)
    
    print(f"Mask size: {mask.size}")
    print(f"Mask mode: {mask.mode}")
    
    # Load frame
    frame_path = Path("output/android-phone/Pixel 8/Hazel/frame.png")
    frame = Image.open(frame_path)
    
    print(f"Frame size: {frame.size}")
    print(f"Frame mode: {frame.mode}")


def example_screen_extraction():
    """Example: Extract screen content from frame using mask."""
    
    from PIL import Image, ImageOps
    import numpy as np
    import json
    
    # Load template
    template_path = Path("output/android-phone/Pixel 8/Hazel/template.json")
    with open(template_path) as f:
        template = json.load(f)
    
    screen = template["screen"]
    
    # Load mask
    mask_path = Path("output/android-phone/Pixel 8/Hazel/mask.png")
    mask = Image.open(mask_path)
    
    # Load frame
    frame_path = Path("output/android-phone/Pixel 8/Hazel/frame.png")
    frame = Image.open(frame_path)
    
    # Extract screen region using bounding box
    x, y, w, h = screen["x"], screen["y"], screen["width"], screen["height"]
    screen_bbox = (x, y, x + w, y + h)
    
    screen_content = frame.crop(screen_bbox)
    screen_content.save("screen_extracted.png")
    
    print(f"Extracted screen: {screen_content.size}")
    print(f"Saved to: screen_extracted.png")
    
    # Alternative: Use mask for precise screen with transparency outside
    frame_with_mask = frame.copy()
    frame_with_mask.putalpha(mask)
    frame_with_mask.save("frame_with_mask.png")
    
    print(f"Saved frame with mask to: frame_with_mask.png")


def example_batch_templates():
    """Example: Iterate through all generated templates."""
    
    import json
    from pathlib import Path
    
    output_root = Path("output")
    
    templates_count = 0
    total_screen_area = 0
    
    for template_path in sorted(output_root.rglob("template.json")):
        with open(template_path) as f:
            template = json.load(f)
        
        screen = template["screen"]
        screen_area = screen["width"] * screen["height"]
        
        total_screen_area += screen_area
        templates_count += 1
        
        # Display info
        device_path = template_path.relative_to(output_root)
        print(f"{device_path}: {screen['width']}x{screen['height']}")
    
    print(f"\nTotal templates: {templates_count}")
    print(f"Average screen area: {total_screen_area // templates_count:,} px²")


if __name__ == "__main__":
    from pathlib import Path
    
    print("=" * 60)
    print("DEVICE FRAME PROCESSING - QUICK START")
    print("=" * 60)
    
    # Check if output exists
    if not Path("output").exists():
        print("\n⚠️  Output directory not found!")
        print("Run: python process_frames.py")
        exit(1)
    
    print("\n1. Load and inspect template metadata:")
    print("-" * 60)
    example_usage()
    
    print("\n2. Extract screen content from frame:")
    print("-" * 60)
    example_screen_extraction()
    
    print("\n3. Iterate through all templates:")
    print("-" * 60)
    example_batch_templates()
