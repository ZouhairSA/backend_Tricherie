#!/bin/bash

# Ensure we're in the correct directory
cd /opt/render/project/src

# Install dependencies
pip install -r requirements.txt

# Initialize and start the application
python run.py &

# Wait for initialization to complete
sleep 2

# Start Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
