"""
API route handlers.
"""

import tempfile
from pathlib import Path
from typing import Optional

from fastapi import File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from engine import apply_frame_to_screenshot, find_template, parse_color
from .main import app


# Supported image formats
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/webp'}


@app.post("/apply_frame")
async def apply_frame(
    file: UploadFile = File(..., description="Screenshot image file (PNG, JPEG, or WebP)"),
    device_type: str = Form(..., description="Device type (e.g., '16 Pro Max')"),
    device_variation: str = Form(..., description="Device variation (e.g., 'Blue Titanium')"),
    background_color: Optional[str] = Form("", description="Background color as hex (#RRGGBB or #RRGGBBAA). Default: transparent"),
):
    """
    Apply a device frame to an uploaded screenshot.
    
    Accepts:
    - file: Image file via multipart/form-data
    - device_type: Device model name
    - device_variation: Device color/variant name
    - background_color: Optional hex color for background
    
    Returns:
    - Framed image as PNG file
    """
    # Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: PNG, JPEG, WebP"
        )
    
    # Extract file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension: {file_ext}. Allowed: .png, .jpg, .jpeg, .webp"
        )
    
    # Parse background color
    try:
        bg_color = parse_color(background_color)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Find device template
    output_root = Path(__file__).resolve().parent.parent / "device-frames-output"
    template_path, candidates = find_template(output_root, device_type, device_variation)
    
    if not template_path:
        raise HTTPException(
            status_code=404,
            detail=f"Template not found for device '{device_type}' variation '{device_variation}'"
        )
    
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_input:
        content = await file.read()
        tmp_input.write(content)
        tmp_input_path = Path(tmp_input.name)
    
    # Create temporary output file
    tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp_output_path = Path(tmp_output.name)
    tmp_output.close()
    
    try:
        # Apply the frame
        result_path = apply_frame_to_screenshot(
            screenshot_path=tmp_input_path,
            template_path=template_path,
            output_path=tmp_output_path,
            background_color=bg_color
        )
        
        # Return the framed image
        return FileResponse(
            path=result_path,
            media_type="image/png",
            filename=f"{device_type}-{device_variation}-framed.png",
            background=None  # Don't delete file immediately, let FileResponse handle cleanup
        )
    
    finally:
        # Clean up input file
        if tmp_input_path.exists():
            tmp_input_path.unlink()
