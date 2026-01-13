#!/usr/bin/env python3
"""
Example: Batch processing multiple screenshots with different device frames
"""

from pathlib import Path
from engine import apply_frame_to_screenshot, find_template, parse_color

# Configuration
SCREENSHOT = Path("test-screenshots/iphone16plus.png")
OUTPUT_DIR = Path("examples")
OUTPUT_DIR.mkdir(exist_ok=True)

# Device configurations to process
devices = [
    ("16 Plus", "Teal", None),
    ("16 Plus", "Black", None),
    ("16 Pro Max", "Natural Titanium", "#FFFFFF"),
    ("16 Pro Max", "Black Titanium", "#000000"),
]

print("🎨 Batch Processing Device Frames\n")

for device_type, variation, bg_color in devices:
    print(f"Processing: {device_type} - {variation}")
    
    # Find template
    template_path, _ = find_template(
        Path("device-frames-output"),
        device_type,
        variation
    )
    
    if not template_path:
        print(f"  ❌ Template not found")
        continue
    
    # Parse background color
    bg = parse_color(bg_color or "")
    
    # Generate output filename
    output_name = f"{device_type.replace(' ', '-')}-{variation.replace(' ', '-')}.png"
    output_path = OUTPUT_DIR / output_name
    
    # Apply frame
    try:
        apply_frame_to_screenshot(
            screenshot_path=SCREENSHOT,
            template_path=template_path,
            output_path=output_path,
            background_color=bg
        )
        print(f"  ✅ Saved to {output_path}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print()

print("✨ Done!")
