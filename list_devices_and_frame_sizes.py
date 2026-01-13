#!/usr/bin/env python3
"""
List all devices with their frame sizes.
"""

import json
from pathlib import Path


def list_devices():
    """List all device types/variations and their frame sizes."""
    
    output_root = Path("device-frames-output")
    
    if not output_root.exists():
        print("⚠️  Output directory not found!")
        print("Run: python process_frames.py")
        return
    
    templates = sorted(output_root.rglob("template.json"))
    
    if not templates:
        print("⚠️  No templates found!")
        return
    
    # Group templates by category
    categories = {
        'android-phone': [],
        'android-tablet': [],
        'iOS': [],
        'iPad': []
    }
    
    for template_path in templates:
        with open(template_path) as f:
            template = json.load(f)
        
        frame_size = template["frameSize"]
        device_path = template_path.parent.relative_to(output_root)
        
        # Get category (first part of path)
        category = device_path.parts[0] if device_path.parts else None
        
        # Format device info
        parts = device_path.parts
        if len(parts) >= 2:
            device_type = parts[-2]
            variation = parts[-1]
            device_info = f"{device_type} - {variation}: {frame_size['width']}x{frame_size['height']}px"
        else:
            device_info = f"{device_path}: {frame_size['width']}x{frame_size['height']}px"
        
        # Add to appropriate category
        if category in categories:
            categories[category].append(device_info)
    
    # Print by category
    total_count = sum(len(devices) for devices in categories.values())
    print(f"Found {total_count} devices:\n")
    
    for category_name in ['android-phone', 'android-tablet', 'iOS', 'iPad']:
        devices = categories[category_name]
        if devices:
            print(f"{'='*60}")
            print(f"{category_name.upper()}")
            print(f"{'='*60}")
            for device in sorted(devices):
                print(device)
            print()


if __name__ == "__main__":
    list_devices()
