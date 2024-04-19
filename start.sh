#!/bin/bash

# Directory for the virtual environment
VENV_DIR="venv"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    # Create a Python virtual environment if it doesn't exist
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the trading_bot.py program in the background
nohup python ./trading_bot/trading_bot.py > /dev/null 2>&1 &
