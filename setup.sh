#!/bin/bash



# Install or upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. To run the application, use ./run.sh"
echo "To activate the environment manually, run: source venv/bin/activate" 