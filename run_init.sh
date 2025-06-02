#!/bin/bash

# Ensure we're in the correct directory
cd /opt/render/project/src

# Install dependencies
pip install -r requirements.txt

# Initialize and start the application
python run.py
