# Device Frame Processing - Usage Examples

This document shows practical examples of how to use the generated device frame templates.

## 1. Load Template Metadata

```python
import json
from pathlib import Path

# Load template
template_path = Path("output/android-phone/Pixel 9 Pro/Hazel/template.json")
with open(template_path) as f:
    template = json.load(f)

# Access data
screen = template["screen"]
frame_size = template["frameSize"]

print(f"Frame: {frame_size['width']}x{frame_size['height']}")
print(f"Screen: {screen['width']}x{screen['height']} at ({screen['x']}, {screen['y']})")
```

## 2. Extract Screen Content

```python
from PIL import Image

# Load frame and mask
frame = Image.open("output/android-phone/Pixel 9 Pro/Hazel/frame.png")
mask = Image.open("output/android-phone/Pixel 9 Pro/Hazel/mask.png")

# Using bounding box
screen = template["screen"]
screen_bbox = (screen['x'], screen['y'], 
               screen['x'] + screen['width'], 
               screen['y'] + screen['height'])
screen_content = frame.crop(screen_bbox)

# Or using mask for precise edges
frame_masked = frame.copy()
frame_masked.putalpha(mask)
frame_masked.save("screenshot_with_frame.png")
```

## 3. Overlay Content on Screen

```python
from PIL import Image

# Load base frame
frame = Image.open("output/iOS/16/Black/frame.png")
screenshot = Image.open("my_screenshot.png")

# Get screen bounds
template = json.load(open("output/iOS/16/Black/template.json"))
screen = template["screen"]

# Resize screenshot to match screen dimensions
screenshot_resized = screenshot.resize(
    (screen['width'], screen['height']),
    Image.Resampling.LANCZOS
)

# Composite onto frame
frame_copy = frame.copy()
frame_copy.paste(screenshot_resized, (screen['x'], screen['y']))
frame_copy.save("framed_screenshot.png")
```

## 4. Batch Process Directories

```python
from pathlib import Path
import json

output_root = Path("output")

# Iterate all device templates
for template_path in sorted(output_root.rglob("template.json")):
    with open(template_path) as f:
        template = json.load(f)
    
    # Get device info from path
    parts = template_path.relative_to(output_root).parts
    device_type = parts[0]  # android-phone, iOS, iPad, etc.
    device_model = parts[1]  # Pixel 9 Pro, iPhone 16, etc.
    color = parts[2]        # Hazel, Black, etc.
    
    frame_path = template_path.parent / "frame.png"
    
    print(f"{device_type}/{device_model}/{color}")
    print(f"  Screen: {template['screen']['width']}x{template['screen']['height']}")
```

## 5. Create Responsive Frame Mockup

```python
from PIL import Image

def create_mockup(screenshot_path, device_template_path, output_path):
    """Create framed screenshot for device."""
    
    # Load template
    with open(device_template_path) as f:
        template = json.load(f)
    
    frame_dir = device_template_path.parent
    
    # Load images
    frame = Image.open(frame_dir / template["frame"])
    mask = Image.open(frame_dir / template["mask"])
    screenshot = Image.open(screenshot_path)
    
    # Resize screenshot to screen dimensions
    screen = template["screen"]
    screenshot_resized = screenshot.resize(
        (screen["width"], screen["height"]),
        Image.Resampling.LANCZOS
    )
    
    # Composite screenshot onto frame
    frame_copy = frame.copy()
    frame_copy.paste(screenshot_resized, (screen["x"], screen["y"]))
    
    # Apply mask for clean edges
    frame_copy.putalpha(mask)
    
    frame_copy.save(output_path)
    return output_path

# Usage
create_mockup(
    "my_app_screenshot.png",
    "output/iOS/16/Black/template.json",
    "mockup_iphone16.png"
)
```

## 6. Compare Device Screen Sizes

```python
from pathlib import Path
import json

output_root = Path("output")
devices = {}

# Collect all devices
for template_path in sorted(output_root.rglob("template.json")):
    with open(template_path) as f:
        template = json.load(f)
    
    parts = template_path.relative_to(output_root).parts
    device_key = f"{parts[0]}/{parts[1]}"
    
    screen = template["screen"]
    dimensions = f"{screen['width']}x{screen['height']}"
    
    if device_key not in devices:
        devices[device_key] = set()
    
    devices[device_key].add(dimensions)

# Display results
for device, dimensions_set in sorted(devices.items()):
    dims = list(dimensions_set)[0]
    print(f"{device:40s} {dims}")
```

## 7. Generate Web-Ready Mockups

```python
from PIL import Image
from pathlib import Path
import json

def create_web_mockups(screenshot_path, output_dir):
    """Create mockups for all devices."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    for template_path in Path("output").rglob("template.json"):
        with open(template_path) as f:
            template = json.load(f)
        
        # Build output filename
        parts = template_path.relative_to("output").parts
        filename = f"{parts[0]}_{parts[1]}_{parts[2]}.png"
        
        # Create mockup
        create_mockup(
            screenshot_path,
            template_path,
            output_dir / filename
        )
        
        print(f"✓ Created {filename}")

# Usage
create_web_mockups("app_screenshot.png", "mockups/")
```

## 8. Filter Devices by Screen Size

```python
from pathlib import Path
import json

def find_devices_by_size(min_width, max_width, min_height, max_height):
    """Find devices matching screen size range."""
    
    matching = []
    
    for template_path in Path("output").rglob("template.json"):
        with open(template_path) as f:
            template = json.load(f)
        
        screen = template["screen"]
        w, h = screen["width"], screen["height"]
        
        if (min_width <= w <= max_width and 
            min_height <= h <= max_height):
            
            parts = template_path.relative_to("output").parts
            matching.append(f"{parts[0]}/{parts[1]}/{parts[2]}")
    
    return matching

# Find all phones with screen width between 1000-1200 pixels
phones = find_devices_by_size(1000, 1200, 2000, 3000)
for phone in phones:
    print(f"  {phone}")
```

## 9. Calculate Frame Padding

```python
import json
from pathlib import Path

def get_padding(template_path):
    """Calculate padding (frame border) for a device."""
    
    with open(template_path) as f:
        template = json.load(f)
    
    screen = template["screen"]
    frame = template["frameSize"]
    
    padding = {
        "top": screen["y"],
        "left": screen["x"],
        "bottom": frame["height"] - (screen["y"] + screen["height"]),
        "right": frame["width"] - (screen["x"] + screen["width"]),
    }
    
    return padding

# Usage
padding = get_padding("output/iPhone 16/Black/template.json")
print(f"Frame padding: top={padding['top']}, left={padding['left']}, "
      f"bottom={padding['bottom']}, right={padding['right']}")
```

## 10. Template Validation

```python
import json
from pathlib import Path
from PIL import Image

def validate_template(template_path):
    """Validate template and assets."""
    
    template_dir = template_path.parent
    
    with open(template_path) as f:
        template = json.load(f)
    
    errors = []
    
    # Check frame file
    frame_path = template_dir / template["frame"]
    if not frame_path.exists():
        errors.append(f"Frame not found: {frame_path}")
    
    # Check mask file
    mask_path = template_dir / template["mask"]
    if not mask_path.exists():
        errors.append(f"Mask not found: {mask_path}")
    
    # Validate dimensions
    screen = template["screen"]
    frame_size = template["frameSize"]
    
    if screen["width"] <= 0 or screen["height"] <= 0:
        errors.append("Screen dimensions invalid")
    
    if screen["x"] < 0 or screen["y"] < 0:
        errors.append("Screen position invalid")
    
    if (screen["x"] + screen["width"] > frame_size["width"] or
        screen["y"] + screen["height"] > frame_size["height"]):
        errors.append("Screen exceeds frame bounds")
    
    # Validate image sizes match
    if frame_path.exists():
        frame = Image.open(frame_path)
        if frame.size != (frame_size["width"], frame_size["height"]):
            errors.append(f"Frame size mismatch: {frame.size} vs {frame_size}")
    
    return len(errors) == 0, errors

# Usage
is_valid, errors = validate_template(Path("output/iOS/16/Black/template.json"))
if is_valid:
    print("✓ Template valid")
else:
    for error in errors:
        print(f"✗ {error}")
```

## Command Line Usage

Process all frames:
```bash
python process_frames.py
```

See processing summary:
```bash
cat PROCESSING_SUMMARY.md
```

Run quickstart examples:
```bash
python quickstart.py
```
