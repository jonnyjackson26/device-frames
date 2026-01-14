"""
FastAPI application instance.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Device Frame API",
    description="Apply device frames to screenshots via HTTP",
    version="1.0.0",
)

# Mount static files for device frames
device_frames_path = Path(__file__).resolve().parent.parent / "device-frames-output"
if device_frames_path.exists():
    app.mount("/frames", StaticFiles(directory=str(device_frames_path)), name="frames")

# Import routes to register them
from . import routes
