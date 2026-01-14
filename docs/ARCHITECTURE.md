# Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
├─────────────────┬────────────────┬──────────────────────────┤
│   CLI Script    │   HTTP Client  │   Python Code            │
│  apply_frame.py │   (curl, JS)   │   (your_app.py)          │
└────────┬────────┴────────┬───────┴──────────┬───────────────┘
         │                 │                  │
         │                 │                  │
┌────────▼─────────────────▼──────────────────▼───────────────┐
│                  INTERFACE LAYER                            │
├────────────────────┬────────────────────────────────────────┤
│   CLI Interface    │        HTTP API Interface              │
│                    │   ┌─────────────────────────────────┐  │
│  • argparse        │   │  FastAPI (api/)                 │  │
│  • print messages  │   │  • POST /apply_frame           │  │
│  • file I/O        │   │  • multipart/form-data          │  │
│                    │   │  • FileResponse                 │  │
│                    │   │  • Error handling (400, 404)    │  │
│                    │   │  • Temp file management         │  │
│                    │   └─────────────────────────────────┘  │
└────────────────────┴────────────────────────────────────────┘
                              │
                              │ Uses
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      ENGINE LAYER                           │
│                   Pure Python (engine/)                     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  apply_frame.py                                    │  │
│  │  • apply_frame_to_screenshot()                       │  │
│  │    - Load template, frame, mask                      │  │
│  │    - Resize screenshot                               │  │
│  │    - Apply mask (alpha channel)                      │  │
│  │    - Composite (background + screenshot + frame)     │  │
│  │    - Return output path                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  color.py                                            │  │
│  │  • parse_color() - Hex to RGB/RGBA                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  templates.py                                        │  │
│  │  • find_template() - Discover device templates       │  │
│  │  • sanitize_filename() - Clean filenames             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Constraints:                                               │
│  ✅ No HTTP imports (FastAPI, requests, etc.)              │
│  ✅ No CLI imports (argparse)                              │
│  ✅ No print statements                                    │
│  ✅ Pure functions (Path in, Path out)                     │
│  ✅ Zero side effects                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Uses
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DEPENDENCIES                             │
│  • Pillow (PIL) - Image manipulation                        │
│  • pathlib - File path handling                             │
│  • json - Template parsing                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Operates on
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                             │
│  device-frames-output/                                      │
│  ├── {device-type}/                                         │
│  │   └── {variant}/                                         │
│  │       ├── frame.png      (Device frame PNG)             │
│  │       ├── mask.png       (Screen mask PNG)              │
│  │       └── template.json  (Metadata)                     │
└─────────────────────────────────────────────────────────────┘


DATA FLOW EXAMPLE:

1. HTTP Request
   POST /apply_frame
   ├── file: screenshot.png
   ├── device_type: "16 Plus"
   ├── device_variation: "Teal"
   └── background_color: "#FF0000"
            │
            ▼
2. API Layer (api/routes.py)
   ├── Validate inputs
   ├── Save uploaded file → /tmp/xxxxx.png
   ├── Parse color → (255, 0, 0)
   └── Find template → device-frames-output/iOS/16 Plus/Teal/
            │
            ▼
3. Engine Layer (engine/apply_frame.py)
   ├── Load template.json
   ├── Load frame.png + mask.png
   ├── Resize screenshot to screen bounds
   ├── Apply mask to screenshot
   ├── Composite: background + screenshot + frame
   └── Save → /tmp/output.png
            │
            ▼
4. API Response
   Return FileResponse(output.png)
   └── Clean up temp files


KEY PRINCIPLES:

1. Separation of Concerns
   - Engine: Pure image processing
   - API: HTTP/networking
   - CLI: User interaction

2. Dependency Direction
   CLI ──→ Engine ←── API
   (Both depend on Engine, Engine depends on nothing)

3. Reusability
   Engine can be used in:
   - Web apps (via API)
   - Desktop apps (direct import)
   - Mobile backends (API)
   - Batch scripts (direct import)
   - CI/CD pipelines (any method)

4. Testability
   - Engine: Unit tests (pure functions)
   - API: Integration tests (HTTP endpoints)
   - CLI: E2E tests (subprocess)
```
