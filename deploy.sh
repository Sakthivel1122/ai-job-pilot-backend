#!/bin/bash

echo "Pulling latest code from main..."
git pull origin main

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Restarting FastAPI service..."
sudo systemctl restart ai_job_pilot.service

echo "Deployment completed successfully!"
