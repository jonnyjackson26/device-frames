#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from engine import apply_frame_to_screenshot, parse_color, find_template, sanitize_filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply a device frame to a screenshot using generated templates.")
    parser.add_argument("--screenshot", required=True, type=Path, help="Path to the screenshot image")
    parser.add_argument("--device-type", required=True, help="Device type directory name (e.g. '16 Pro Max')")
    parser.add_argument("--device-variation", required=True, help="Device variation directory name (e.g. 'Blue Titanium')")
    parser.add_argument("--output", type=Path, help="Output image path (default: mockup/<device>-<variation>-framed.png)")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent, help="Directory for output if --output is not provided")
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent / "device-frames-output", help="Root output directory containing device templates")
    parser.add_argument("--background-color", type=str, default="", help="Background color as hex (#RRGGBB or #RRGGBBAA). Default: transparent")
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

    try:
        background_color = parse_color(args.background_color)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    print("Applying frame...")
    print(f"Screenshot: {screenshot_path}")
    print(f"Template:   {template_path}")
    print(f"Output:     {output_path}")
    print(f"Background: {args.background_color}")
    print()

    result_path = apply_frame_to_screenshot(screenshot_path, template_path, output_path, background_color)
    
    print(f"\nFramed screenshot saved to: {result_path}")

