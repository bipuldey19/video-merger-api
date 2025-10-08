# 🚀 Production VPS Deployment Guide

## Prerequisites

- **VPS Requirements:**
  - Ubuntu 20.04+ or Debian 11+ (recommended)
  - Minimum 2GB RAM, 2 CPU cores
  - 20GB+ storage
  - Root or sudo access

## 📋 Step-by-Step Deployment

### 1. Prepare Your VPS

```bash
# Connect to your VPS
ssh root@your-vps-ip

# Or if using a user account:
ssh username@your-vps-ip
```

### 2. Upload Project Files

**Option A: Using SCP**
```bash
# From your local machine
scp -r /path/to/video-merger-api/* username@your-vps-ip:/tmp/video-merger-api/
```

**Option B: Using Git**
```bash
# On your VPS
git clone https://github.com/yourusername/video-merger-api.git /tmp/video-merger-api
```

### 3. Run Setup Scripts

```bash
# Copy uploaded files to VPS
sudo cp -r /tmp/video-merger-api /opt/
sudo chown -R root:root /opt/video-merger-api

# Make scripts executable
chmod +x /opt/video-merger-api/setup-vps.sh
chmod +x /opt/video-merger-api/setup-services.sh

# Run system setup
sudo /opt/video-merger-api/setup-vps.sh

# Move application files to correct location
sudo cp -r /opt/video-merger-api/* /opt/video-merger-api/
sudo chown -R videoapi:videoapi /opt/video-merger-api

# Install Python dependencies
sudo -u videoapi /opt/video-merger-api/venv/bin/pip install -r /opt/video-merger-api/requirements.txt

# Setup services
sudo /opt/video-merger-api/setup-services.sh
```

### 4. Configure Domain (Optional)

Edit Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/video-merger-api
```

Replace `your-domain.com` with your actual domain or server IP.

### 5. SSL Certificate (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate (replace your-domain.com)
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## 🔧 Service Management

### Start/Stop/Restart API
```bash
# Using Supervisor (recommended)
sudo supervisorctl start video-merger-api
sudo supervisorctl stop video-merger-api
sudo supervisorctl restart video-merger-api
sudo supervisorctl status video-merger-api

# Using Systemd (alternative)
sudo systemctl start video-merger-api
sudo systemctl stop video-merger-api
sudo systemctl restart video-merger-api
sudo systemctl status video-merger-api
```

### View Logs
```bash
# Application logs
sudo tail -f /var/log/video-merger-api/error.log
sudo tail -f /var/log/video-merger-api/access.log

# Supervisor logs
sudo tail -f /var/log/supervisor/supervisord.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🧪 Testing Your Deployment

### Health Check
```bash
curl http://your-server-ip/health
# Should return: {"status": "healthy"}
```

### Format Validation Test
```bash
curl -X POST "http://your-server-ip/test-endpoint" \
  -H "Content-Type: application/json" \
  -d '[{"title": "Test", "author_fullname": "test", "secure_media": {"reddit_video": {"hls_url": "https://test.m3u8"}}, "url": "https://test.com"}]'
```

### Full Processing Test
```bash
curl -X POST "http://your-server-ip/merge-videos" \
  -H "Content-Type: application/json" \
  -d '[{"title": "The plot twist of all plot twists!", "author_fullname": "t2_1gnm5bvcxf", "secure_media": {"reddit_video": {"hls_url": "https://v.redd.it/ugqge1h9lotf1/HLSPlaylist.m3u8?a=1762493081%2CZjUxMGJmODc2NmE1ZGY4OWVhMTYwOWFjNzNiZDIxNDY1NTFhMjAyYTViNGUyNWRhOWZmNTdhZjViMDdhYWQ4OA%3D%3D&v=1&f=sd"}}, "url": "https://v.redd.it/ugqge1h9lotf1"}]' \
  --output test-video.mp4
```

## 🎯 Production Configuration

### Environment Variables
Create `/opt/video-merger-api/.env`:
```bash
# Production settings
ENVIRONMENT=production
LOG_LEVEL=info
MAX_CONCURRENT_VIDEOS=5
TEMP_DIR=/tmp/video-processing
```

### Performance Tuning

**Gunicorn Workers:**
Edit `/opt/video-merger-api/gunicorn.conf.py`:
```python
# Adjust based on your VPS specs
workers = 4  # For 2-core VPS
workers = 8  # For 4-core VPS
```

**Nginx Buffer Sizes:**
Edit `/etc/nginx/sites-available/video-merger-api`:
```nginx
client_max_body_size 500M;  # For larger video files
proxy_read_timeout 1200s;   # 20 minutes for long processing
```

## 🔒 Security Considerations

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw deny 8000  # Don't expose Gunicorn directly
sudo ufw enable
```

### Rate Limiting (Optional)
Add to Nginx configuration:
```nginx
# Limit requests per IP
limit_req_zone $binary_remote_addr zone=api:10m rate=5r/m;

server {
    # ... other config ...
    
    location /merge-videos {
        limit_req zone=api burst=2 nodelay;
        # ... proxy config ...
    }
}
```

## 📊 Monitoring

### System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor resources
htop                    # CPU/Memory usage
sudo iotop             # Disk I/O
sudo nethogs           # Network usage
```

### Log Rotation
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/video-merger-api
```

Add:
```
/var/log/video-merger-api/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 videoapi videoapi
    postrotate
        supervisorctl restart video-merger-api
    endscript
}
```

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Stop the service
sudo supervisorctl stop video-merger-api

# Backup current version
sudo cp -r /opt/video-merger-api /opt/video-merger-api.backup.$(date +%Y%m%d)

# Update code (via git pull or file upload)
cd /opt/video-merger-api
sudo -u videoapi git pull  # if using git

# Install any new dependencies
sudo -u videoapi /opt/video-merger-api/venv/bin/pip install -r requirements.txt

# Restart the service
sudo supervisorctl start video-merger-api
```

### Backup Strategy
```bash
# Create backup script
sudo nano /opt/backup-video-api.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/video-merger-api_$DATE.tar.gz /opt/video-merger-api
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete  # Keep 7 days of backups
```

## 🎉 Your API is Now Production Ready!

### Access Your API:
- **Health Check:** `http://your-server-ip/health`
- **API Documentation:** `http://your-server-ip/docs`
- **Main Endpoint:** `POST http://your-server-ip/merge-videos`

### n8n Integration:
Use `http://your-server-ip/merge-videos` as the webhook URL in your n8n workflow with your 14-video JSON format.

**Processing Capacity:**
- **14 videos:** ~5-10 minutes processing time
- **Output:** 1080x1920 MP4 with titles and transitions  
- **Concurrent requests:** Handled by multiple Gunicorn workers
- **Automatic cleanup:** Temporary files deleted after processing