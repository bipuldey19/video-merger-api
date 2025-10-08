# Gunicorn configuration for production deployment
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Timeout settings (important for video processing)
timeout = 600  # 10 minutes for video processing
keepalive = 30
graceful_timeout = 30

# Logging
accesslog = "/var/log/video-merger-api/access.log"
errorlog = "/var/log/video-merger-api/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'video-merger-api'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Preload application for better performance
preload_app = True

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Environment variables
raw_env = [
    'PYTHONPATH=.',
]