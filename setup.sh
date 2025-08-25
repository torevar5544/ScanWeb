#!/bin/bash

echo "=============================="
echo "Website Security Scanner Setup"
echo "=============================="

# Update system
echo "[*] Updating system packages..."
sudo apt update -y && sudo apt upgrade -y

# Install Python3 and pip if missing
echo "[*] Installing Python3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install system tools: nmap, mtr, openssl
echo "[*] Installing system tools..."
sudo apt install -y nmap mtr openssl

# Finish
echo "[✓] Setup completed!"
echo "To start the scanner, activate the virtual environment:"
echo "source venv/bin/activate"
echo "python ScanWeb.py"
