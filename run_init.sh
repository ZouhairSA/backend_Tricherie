#!/bin/bash

# Ensure we're in the correct directory
cd /opt/render/project/src

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python run.py

# Start Gunicorn with a single worker
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1
