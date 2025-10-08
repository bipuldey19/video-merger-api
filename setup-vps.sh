#!/bin/bash

# Production VPS Setup Script for Video Merger API
# Run this script on your Ubuntu/Debian VPS

set -e

echo "🚀 Setting up Video Merger API for Production"
echo "============================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    nginx \
    supervisor \
    git \
    curl \
    htop \
    ufw

# Create application user
echo "👤 Creating application user..."
sudo useradd -m -s /bin/bash videoapi || true
sudo usermod -aG sudo videoapi || true

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/video-merger-api
sudo chown videoapi:videoapi /opt/video-merger-api

# Create log directory
echo "📝 Setting up logging..."
sudo mkdir -p /var/log/video-merger-api
sudo chown videoapi:videoapi /var/log/video-merger-api

# Clone or copy application (assumes you'll upload your code)
echo "💾 Application code should be placed in /opt/video-merger-api"
echo "   You can use: scp -r /path/to/your/code/* user@your-vps:/opt/video-merger-api/"

# Create Python virtual environment
echo "🐍 Setting up Python virtual environment..."
sudo -u videoapi python3 -m venv /opt/video-merger-api/venv
sudo -u videoapi /opt/video-merger-api/venv/bin/pip install --upgrade pip

# Install Python dependencies (will be done after code upload)
echo "📋 Install dependencies after uploading your code:"
echo "   sudo -u videoapi /opt/video-merger-api/venv/bin/pip install -r /opt/video-merger-api/requirements.txt"

echo "✅ System setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Upload your code to /opt/video-merger-api/"
echo "2. Run: sudo -u videoapi /opt/video-merger-api/venv/bin/pip install -r /opt/video-merger-api/requirements.txt"
echo "3. Run: sudo ./setup-services.sh"
echo "4. Configure your domain/firewall as needed"