#!/bin/bash

# Quick start script for Device Frames API

echo "🚀 Starting Device Frames API..."
echo ""
echo "API will be available at:"
echo "  - Base URL: http://localhost:8000"
echo "  - Interactive Docs: http://localhost:8000/docs"
echo "  - OpenAPI Schema: http://localhost:8000/openapi.json"
echo ""
echo "Example curl command:"
echo '  curl -X POST http://localhost:8000/apply_frame \'
echo '    -F "file=@screenshot.png" \'
echo '    -F "device_type=16 Plus" \'
echo '    -F "device_variation=Teal" \'
echo '    -o framed.png'
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
