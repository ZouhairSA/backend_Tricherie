#!/bin/bash

# Ensure we're in the correct directory
cd /opt/render/project/src

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db_render.py

# Start the application
gunicorn app:app --bind 0.0.0.0:$PORT
