"""Audio Tutor FastAPI application.

This module exposes a minimal FastAPI app as a placeholder. The interactive
voice tutoring experience currently runs via the CLI in
`server/services/app.py`. Future work may wire REST/WebSocket endpoints here.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Health-check endpoint.

    Returns:
        dict: A simple payload indicating the API is up.
    """
    return {"message": "Hello World"}