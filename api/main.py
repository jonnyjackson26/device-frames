"""
FastAPI application instance.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Device Frame API",
    description="Apply device frames to screenshots via HTTP",
    version="1.0.0",
)

# Import routes to register them
from . import routes
