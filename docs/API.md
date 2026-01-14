# Device Frames - API Documentation

## Overview

Device Frames provides both a Python engine and HTTP API for applying device frames to screenshots. The project has been refactored into a clean, production-ready structure that separates frame application logic from HTTP/CLI concerns.

## Project Structure

```
device-frames/
├── engine/                    # Pure frame application logic (no HTTP dependencies)
│   ├── __init__.py
│   ├── apply_frame.py        # Core frame application function
│   ├── color.py              # Color parsing utilities
│   └── templates.py          # Template discovery utilities
│
├── api/                       # FastAPI HTTP service
│   ├── main.py               # FastAPI app instance
│   └── routes.py             # /apply_frame endpoint
│
├── device-frames-output/     # Device templates (frame.png, mask.png, template.json)
├── apply_frame.py            # CLI script (uses engine)
└── requirements.txt          # Dependencies
```

## Installation

```bash
pip install -r requirements.txt
```

## CLI Usage

```bash
python apply_frame.py \
  --screenshot test-screenshots/iphone16plus.png \
  --device-type "16 Plus" \
  --device-variation "Teal" \
  --output marketing/hero-image.png \
  --background-color "#FF0000"
```

### CLI Options

- `--screenshot`: Path to screenshot image (required)
- `--device-type`: Device model name, e.g., "16 Plus", "16 Pro Max" (required)
- `--device-variation`: Device color/variant, e.g., "Teal", "Blue Titanium" (required)
- `--output`: Output path (optional, defaults to `<device>-<variation>-framed.png`)
- `--background-color`: Hex color for background, e.g., "#RRGGBB" or "#RRGGBBAA" (optional, default: transparent)

## API Usage

### Starting the Server

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Interactive API documentation (Swagger UI): `http://localhost:8000/docs`

### API Endpoints

#### GET /frames/{path}

Access static device frame assets (PNG images) directly via HTTP.

##### Path Parameters

- `path`: Relative path to the frame file (e.g., `iOS/16 Plus/Teal/frame.png`)

##### Examples

```bash
# Access a specific frame PNG
curl https://device-frames.fly.dev/frames/iOS/16%20Plus/Teal/frame.png -o frame.png

# Or for Android
curl https://device-frames.fly.dev/frames/android-phone/Pixel%208%20Pro/Black/frame.png -o frame.png
```

Note: Spaces in URLs must be percent-encoded as `%20`.

---

#### GET /list_devices

List all available device frames with their metadata and frame sizes.

##### Request

No parameters required.

##### Response

Returns a nested JSON structure organizing devices by category, device type, and variation:

```json
{
  "category": {
    "device_type": {
      "variation": {
        "frame_png": "path/to/frame.png",
        "template": { /* full template.json content */ },
        "frame_size": {
          "width": 1234,
          "height": 5678
        }
      }
    }
  }
}
```

**Categories:**
- `iOS` - iPhones
- `iPad` - iPads (all models)
- `android-phone` - Android phones (Pixel, etc.)
- `android-tablet` - Android tablets

**Response Fields:**
- `frame_png`: URL path to access the device frame PNG file (e.g., `/frames/iOS/16 Plus/Teal/frame.png`)
- `frame_png_path`: Relative file path within the device-frames-output directory
- `template`: Complete template.json data including frameSize, screenArea, radius, etc.
- `frame_size`: Quick access to frame dimensions (width × height in pixels)

##### Example Response

```json
{
  "iOS": {
    "16 Plus": {
      "Teal": {
        "frame_png": "/frames/iOS/16 Plus/Teal/frame.png",
        "frame_png_path": "iOS/16 Plus/Teal/frame.png",
        "template": {
          "frameSize": {"width": 1366, "height": 2830},
          "screenArea": {"x": 83, "y": 83, "width": 1200, "height": 2664},
          "radius": 165
        },
        "frame_size": {"width": 1366, "height": 2830}
      }
    },
    "16 Pro Max": {
      "Black Titanium": {
        "frame_png": "/frames/iOS/16 Pro Max/Black Titanium/frame.png",
        "frame_png_path": "iOS/16 Pro Max/Black Titanium/frame.png",
        "template": {
          "frameSize": {"width": 1426, "height": 3092},
          "screenArea": {"x": 83, "y": 83, "width": 1260, "height": 2796},
          "radius": 181
        },
        "frame_size": {"width": 1426, "height": 3092}
      }
    }
  },
  "android-phone": {
    "Pixel 8": {
      "Hazel": {
        "frame_png": "/frames/android-phone/Pixel 8/Hazel/frame.png",
        "frame_png_path": "android-phone/Pixel 8/Hazel/frame.png",
        "template": { /* ... */ },
        "frame_size": {"width": 1234, "height": 2700}
      }
    }
  }
}
```

##### Example with curl

```bash
curl http://localhost:8000/list_devices | python3 -m json.tool
```

##### Example with Python requests

```python
import requests

response = requests.get("http://localhost:8000/list_devices")
devices = response.json()

# List all iOS devices
for device_type, variations in devices["iOS"].items():
    print(f"\n{device_type}:")
    for variation, data in variations.items():
        size = data["frame_size"]
        print(f"  - {variation}: {size['width']}×{size['height']}px")
```

##### Example with JavaScript (fetch)

```javascript
fetch('http://localhost:8000/list_devices')
  .then(response => response.json())
  .then(devices => {
    // Build a device selector dropdown
    const category = devices.iOS;
    for (const [deviceType, variations] of Object.entries(category)) {
      for (const [variation, data] of Object.entries(variations)) {
        console.log(`${deviceType} - ${variation}: ${data.frame_size.width}×${data.frame_size.height}`);
      }
    }
  });
```

---

#### POST /apply_frame

Apply a device frame to an uploaded screenshot.

#### Request

Content-Type: `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | Screenshot image (PNG, JPEG, or WebP) |
| `device_type` | String | Yes | Device model name (e.g., "16 Plus") |
| `device_variation` | String | Yes | Device color/variant (e.g., "Teal") |
| `background_color` | String | No | Hex color for background (e.g., "#RRGGBB" or "#RRGGBBAA"). Default: transparent |

#### Response

- **Success (200)**: Returns the framed image as a PNG file
- **Bad Request (400)**: Invalid color format or unsupported file type
- **Not Found (404)**: Device template not found

#### Example with curl

```bash
# Basic usage
curl -X POST http://localhost:8000/apply_frame \
  -F "file=@screenshot.png" \
  -F "device_type=16 Plus" \
  -F "device_variation=Teal" \
  -o output.png

# With custom background color
curl -X POST http://localhost:8000/apply_frame \
  -F "file=@screenshot.png" \
  -F "device_type=16 Pro Max" \
  -F "device_variation=Black Titanium" \
  -F "background_color=#FF0000" \
  -o output.png
```

#### Example with Python requests

```python
import requests

url = "http://localhost:8000/apply_frame"

with open("screenshot.png", "rb") as f:
    files = {"file": f}
    data = {
        "device_type": "16 Plus",
        "device_variation": "Teal",
        "background_color": "#FF0000"  # Optional
    }
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        with open("output.png", "wb") as out:
            out.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.json()}")
```

#### Example with JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('device_type', '16 Plus');
formData.append('device_variation', 'Teal');
formData.append('background_color', '#FF0000'); // Optional

fetch('http://localhost:8000/apply_frame', {
  method: 'POST',
  body: formData
})
  .then(response => response.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    // Display or download the image
  });
```

## Engine Usage (Programmatic)

The engine can be used directly in Python code:

```python
from pathlib import Path
from engine import apply_frame_to_screenshot, parse_color, find_template

# Find device template
output_root = Path("device-frames-output")
template_path, _ = find_template(output_root, "16 Plus", "Teal")

if template_path:
    # Apply frame
    result = apply_frame_to_screenshot(
        screenshot_path=Path("screenshot.png"),
        template_path=template_path,
        output_path=Path("output.png"),
        background_color=parse_color("#FF0000")  # Optional, default: (0,0,0,0)
    )
    print(f"Saved to: {result}")
```

## Supported Devices

The API supports any device template in the `device-frames-output/` directory:

- **iOS**: iPhone 13 mini, 14 Pro Max, 15 Pro Max, 16, 16 Plus, 16 Pro, 16 Pro Max, 17 Pro, 17 Pro Max, Air
- **iPad**: iPad Air (various models), iPad Pro (various models), iPad mini
- **Android Phones**: Pixel 8, Pixel 8 Pro, Pixel 9 Pro, Pixel 9 Pro XL
- **Android Tablets**: Pixel Tablet, Samsung Galaxy Tab S11 Ultra

Use the exact folder names for `device_type` and `device_variation`.

## Design Principles

### Engine Module
- **Pure functions**: No side effects, deterministic behavior
- **No HTTP dependencies**: Can be used in any Python context
- **No CLI parsing**: Accepts only Python data types
- **Minimal logging**: No print statements, returns Paths

### API Module
- **Clean separation**: HTTP concerns only (validation, file handling, responses)
- **Multipart form-data**: Efficient binary file streaming
- **Proper error handling**: HTTP status codes for all error cases
- **Temporary files**: No long-term storage, cleanup after response

## Why This Architecture?

This structure enables future:
- ✅ Web applications
- ✅ Public APIs
- ✅ Python SDKs
- ✅ NPM/JavaScript SDKs
- ✅ React components
- ✅ Mobile apps
- ✅ Batch processing
- ✅ Video frame application

All powered by the same frame application engine.

## Limitations

- **No URL support**: The API does not accept image URLs (SSRF prevention, latency control)
- **No authentication**: Add your own auth layer if needed
- **Single image only**: No batch processing yet (coming soon)

## Contributing

When adding new features:
- Frame application logic → `engine/`
- HTTP endpoints → `api/`
- CLI options → `apply_frame.py`

Keep the separation clean!
