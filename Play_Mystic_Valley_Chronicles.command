#!/bin/bash
cd "$(dirname "$0")"

# 1. Automatic first-time setup: Create venv and install dependencies if missing
if [ ! -d "venv" ]; then
    echo "=================================================="
    echo " 🌲 First-Time Setup: Creating Virtual Env...    "
    echo "=================================================="
    python3 -m venv venv
    echo "Installing required game dependencies (pygame-ce)..."
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt || ./venv/bin/pip install pygame-ce
fi

# 2. Activate virtual environment and boot the game
echo "=================================================="
    echo " 🎮 Launching Mystic Valley Chronicles...       "
echo "=================================================="
source ./venv/bin/activate
python main.py
