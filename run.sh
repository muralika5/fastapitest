#!/bin/bash

# Activate the virtual environment if it exists
workon fastapi

# Run the FastAPI app
echo "Starting FastAPI server..."
uvicorn main:app --reload 