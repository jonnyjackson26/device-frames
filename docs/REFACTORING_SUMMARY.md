
### ✅ HTTP API Features

**Endpoint**: `POST /apply_frame`

**Accepts**:
- `file`: Image upload (PNG, JPEG, WebP)
- `device_type`: Device model name
- `device_variation`: Device color/variant
- `background_color`: Optional hex color

**Returns**: Framed image as PNG file

**Error Handling**:
- 400: Invalid color, unsupported file type
- 404: Device template not found

### ✅ Documentation

- **API.md**: Comprehensive API documentation with examples
- **README.md**: Updated with quick start for all three usage modes
- **Code Comments**: Docstrings for all functions
- **Examples**: Batch processing script demonstrating engine usage

## 🧪 Testing Results

### CLI Testing
```bash
✅ python apply_frame.py --screenshot test-screenshots/iphone16plus.png \
    --device-type "16 Plus" --device-variation "Teal" \
    --output marketing/hero-image.png
```

### 2. HTTP API
```bash
curl -X POST http://localhost:8000/apply_frame \
  -F "file=@image.png" \
  -F "device_type=16 Pro Max" \
  -F "device_variation=Natural Titanium" \
  -F "background_color=#FFFFFF" \
  -o framed.png
```

### 3. Python Engine
```python
from pathlib import Path
from engine import apply_frame_to_screenshot, find_template

template_path, _ = find_template(
    Path("device-frames-output"),
    "16 Pro Max",
    "Natural Titanium"
)

apply_frame_to_screenshot(
    screenshot_path=Path("image.png"),
    template_path=template_path,
    output_path=Path("framed.png"),
    background_color=(255, 255, 255)
)
```

```bash
python apply_frame.py --screenshot ... --device-type ... --device-variation ...
```

### For New API Users
Start the server and use the HTTP endpoint:
```bash
./start_api.sh
```

### For Library Users
Import the engine directly:
```python
from engine import apply_frame_to_screenshot
```
