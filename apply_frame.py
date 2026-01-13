#!/usr/bin/env python3


import argparse
import json
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image, ImageFilter


def apply_frame_to_screenshot(screenshot_path: Path, template_path: Path, output_path: Path):
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


def find_template(output_root: Path, device_type: str, device_variation: str) -> Tuple[Optional[Path], List[Path]]:
    pattern = f"{device_type}/{device_variation}/template.json"
    matches = list(output_root.rglob(pattern))
    if not matches:
        return None, []
    return matches[0], matches


def sanitize_filename(text: str) -> str:
    return text.replace(" ", "-")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply a device frame to a screenshot using generated templates.")
    parser.add_argument("--screenshot", required=True, type=Path, help="Path to the screenshot image")
    parser.add_argument("--device-type", required=True, help="Device type directory name (e.g. '16 Pro Max')")
    parser.add_argument("--device-variation", required=True, help="Device variation directory name (e.g. 'Blue Titanium')")
    parser.add_argument("--output", type=Path, help="Output image path (default: mockup/<device>-<variation>-framed.png)")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent, help="Directory for output if --output is not provided")
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent.parent / "device-frames-output", help="Root output directory containing device templates")
    args = parser.parse_args()

    screenshot_path = args.screenshot.expanduser().resolve()
    if not screenshot_path.exists():
        print(f"Error: Screenshot not found at {screenshot_path}")
        exit(1)

    template_path, candidates = find_template(args.output_root, args.device_type, args.device_variation)
    if not template_path:
        print(f"Error: template.json not found for device '{args.device_type}' variation '{args.device_variation}' under {args.output_root}")
        exit(1)
    if len(candidates) > 1:
        print("Warning: multiple templates found; using the first match:")
        for p in candidates:
            print(f" - {p}")

    if args.output:
        output_path = args.output.expanduser().resolve()
    else:
        filename = f"{sanitize_filename(args.device_type)}-{sanitize_filename(args.device_variation)}-framed.png"
        output_dir = args.output_dir.expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

    print("Applying frame...")
    print(f"Screenshot: {screenshot_path}")
    print(f"Template:   {template_path}")
    print(f"Output:     {output_path}")
    print()

    apply_frame_to_screenshot(screenshot_path, template_path, output_path)
