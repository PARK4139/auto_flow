#!/bin/bash

echo "Updating system..."
sudo apt update -y

echo "Installing Python 3.8 and dependencies..."
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.8 python3.8-venv python3.8-distutils python3.8-dev

echo "Installing pip for Python 3.8..."
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.8

echo "Installing uv..."
python3.8 -m pip install uv
python -m pip install uv

echo "Verifying installation..."
uv --version && echo "✅ uv installed successfully." || echo "❌ uv installation failed."