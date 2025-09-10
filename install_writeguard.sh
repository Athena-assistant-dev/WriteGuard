#!/bin/bash

set -e

echo "🔧 Installing WriteGuard (v0.0.2)"

# Install Python deps
python3 -m pip install --upgrade pip
pip install flask python-dotenv pyyaml redbaron jsonpatch pillow python-docx python-pptx openpyxl ruamel.yaml

# Run API
cd app/v0.0.2
export $(cat ../../.env | xargs)
echo "✅ Starting WriteGuard API on port $PORT"
python3 writeguard_api.py