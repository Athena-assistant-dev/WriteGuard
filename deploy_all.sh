#!/bin/bash

set -e

echo "🔐 Starting WriteGuard Full Stack (API + Dashboard)"

# Load env vars
export $(cat .env | xargs)

# Install Python deps
pip install -r requirements.txt || true
pip install flask python-dotenv pyyaml redbaron jsonpatch pillow python-docx python-pptx openpyxl ruamel.yaml

# Start API
cd app/v0.0.2 &
nohup python3 writeguard_api.py > ../../logs/api.log 2>&1 &
nohup python3 pro_dashboard_ui.py > ../../logs/dashboard.log 2>&1 &

cd ../..
echo "✅ WriteGuard API: http://localhost:$PORT"
echo "✅ Pro Dashboard: http://localhost:5151"