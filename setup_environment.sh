#!/bin/bash

# Script to set up the virtual environment and install dependencies

# Navigate to the project root directory
cd "$(dirname "$0")" || exit

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo "Environment setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"