#!/bin/bash

# Service Configuration Script
# Run after setup-vps.sh and uploading your code

set -e

echo "🔧 Configuring production services..."
echo "====================================="

# Create Supervisor configuration for the API
echo "📋 Creating Supervisor configuration..."
sudo tee /etc/supervisor/conf.d/video-merger-api.conf > /dev/null <<EOF
[program:video-merger-api]
command=/opt/video-merger-api/venv/bin/gunicorn -c /opt/video-merger-api/gunicorn.conf.py main:app
directory=/opt/video-merger-api
user=videoapi
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/video-merger-api/supervisor.log
environment=PATH="/opt/video-merger-api/venv/bin"
stopwaitsecs=600
EOF

# Create Nginx configuration
echo "🌐 Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/video-merger-api > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain
    client_max_body_size 100M;
    client_body_timeout 600s;
    client_header_timeout 600s;
    proxy_read_timeout 600s;
    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Important for video processing
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
EOF

# Create systemd service (alternative to Supervisor)
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/video-merger-api.service > /dev/null <<EOF
[Unit]
Description=Video Merger API
After=network.target

[Service]
Type=exec
User=videoapi
Group=videoapi
WorkingDirectory=/opt/video-merger-api
Environment=PATH=/opt/video-merger-api/venv/bin
ExecStart=/opt/video-merger-api/venv/bin/gunicorn -c /opt/video-merger-api/gunicorn.conf.py main:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3
TimeoutStopSec=600

[Install]
WantedBy=multi-user.target
EOF

# Enable Nginx site
echo "🔗 Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/video-merger-api /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Test Nginx configuration
echo "✅ Testing Nginx configuration..."
sudo nginx -t

# Reload services
echo "🔄 Reloading services..."
sudo systemctl reload nginx
sudo supervisorctl reread
sudo supervisorctl update

# Start the API service
echo "🚀 Starting Video Merger API..."
sudo supervisorctl start video-merger-api

# Enable systemd service (alternative)
sudo systemctl daemon-reload
sudo systemctl enable video-merger-api

echo "✅ Services configured successfully!"
echo ""
echo "📋 Service management commands:"
echo "  sudo supervisorctl status video-merger-api"
echo "  sudo supervisorctl restart video-merger-api"
echo "  sudo supervisorctl stop video-merger-api"
echo "  sudo supervisorctl start video-merger-api"
echo ""
echo "📋 Log locations:"
echo "  Application: /var/log/video-merger-api/"
echo "  Nginx: /var/log/nginx/"
echo "  Supervisor: /var/log/supervisor/"
echo ""
echo "🌐 Your API should be available at: http://your-server-ip/"
echo "   Don't forget to update 'server_name' in /etc/nginx/sites-available/video-merger-api"