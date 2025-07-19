#!/bin/bash

# SVA Terminal Raspberry Pi Deployment Script
# This script deploys the SVA Terminal application to a Raspberry Pi 4

set -e

echo "=========================================="
echo "SVA Terminal Raspberry Pi Deployment"
echo "=========================================="

# Configuration variables
SVA_USER="sva"
SVA_HOME="/home/$SVA_USER"
SVA_APP_DIR="/opt/sva_terminal"
BACKUP_DIR="$SVA_HOME/backups"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (use sudo)"
    exit 1
fi

# Create backup of existing installation
if [ -d "$SVA_APP_DIR" ]; then
    echo "Creating backup of existing installation..."
    BACKUP_NAME="sva_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp -r "$SVA_APP_DIR" "$BACKUP_DIR/$BACKUP_NAME"
    echo "Backup created: $BACKUP_DIR/$BACKUP_NAME"
fi

# Create application directory
echo "Setting up application directory..."
mkdir -p "$SVA_APP_DIR"
cd "$SVA_APP_DIR"

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip

# Core Flask dependencies
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install flask-sqlalchemy==3.0.5

# Biometric dependencies
pip install opencv-python-headless==4.8.1.78
pip install mediapipe==0.10.7
pip install numpy==1.24.3

# Additional utilities
pip install requests==2.31.0
pip install pillow==10.0.1
pip install python-dateutil==2.8.2

# Create requirements.txt
pip freeze > requirements.txt

# Set up directory structure
echo "Setting up directory structure..."
mkdir -p src/{models,routes,utils,static,database}
mkdir -p scripts
mkdir -p logs
mkdir -p config

# Create systemd service file
echo "Creating systemd service..."
cat > /etc/systemd/system/sva-terminal.service << EOF
[Unit]
Description=SVA Terminal Application
After=network.target

[Service]
Type=simple
User=$SVA_USER
Group=$SVA_USER
WorkingDirectory=$SVA_APP_DIR
Environment=PATH=$SVA_APP_DIR/venv/bin
Environment=FLASK_APP=src/main.py
Environment=FLASK_ENV=production
ExecStart=$SVA_APP_DIR/venv/bin/python src/main.py
Restart=always
RestartSec=10

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$SVA_APP_DIR

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration for reverse proxy (optional)
echo "Creating nginx configuration..."
apt install -y nginx

cat > /etc/nginx/sites-available/sva-terminal << 'EOF'
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static {
        alias /opt/sva_terminal/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
EOF

# Enable nginx site
ln -sf /etc/nginx/sites-available/sva-terminal /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Create configuration file
echo "Creating application configuration..."
cat > config/production.py << 'EOF'
import os

class ProductionConfig:
    """Production configuration for SVA Terminal"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sva-terminal-production-key-2024'
    DEBUG = False
    TESTING = False
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/sva_terminal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Security settings
    SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Biometric settings
    FACE_RECOGNITION_THRESHOLD = 0.7
    FINGERPRINT_RECOGNITION_THRESHOLD = 0.7
    
    # Hardware settings
    CAMERA_DEVICE = 0
    FINGERPRINT_DEVICE = '/dev/ttyUSB0'
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/sva_terminal/app.log'
EOF

# Create startup script
echo "Creating startup script..."
cat > scripts/start_sva.sh << 'EOF'
#!/bin/bash

# SVA Terminal Startup Script
cd /opt/sva_terminal
source venv/bin/activate

# Check database
if [ ! -f "src/database/sva_terminal.db" ]; then
    echo "Initializing database..."
    python -c "
from src.main import create_app
app = create_app()
with app.app_context():
    from src.models.user import db
    db.create_all()
    print('Database initialized')
"
fi

# Start application
echo "Starting SVA Terminal..."
python src/main.py
EOF

chmod +x scripts/start_sva.sh

# Create monitoring script
cat > scripts/monitor_sva.sh << 'EOF'
#!/bin/bash

# SVA Terminal Monitoring Script
echo "SVA Terminal System Status"
echo "========================="
echo "Date: $(date)"
echo "Uptime: $(uptime -p)"
echo ""

# Check services
echo "Service Status:"
echo "- SVA Terminal: $(systemctl is-active sva-terminal)"
echo "- Nginx: $(systemctl is-active nginx)"
echo "- SSH: $(systemctl is-active ssh)"
echo ""

# Check resources
echo "System Resources:"
echo "- CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "- Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "- Disk Usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"
echo "- Temperature: $(vcgencmd measure_temp 2>/dev/null | cut -d'=' -f2 || echo 'N/A')"
echo ""

# Check network
echo "Network Status:"
echo "- Interface: $(ip route | grep default | awk '{print $5}' | head -1)"
echo "- IP Address: $(hostname -I | awk '{print $1}')"
echo "- Internet: $(ping -c 1 8.8.8.8 >/dev/null 2>&1 && echo 'Connected' || echo 'Disconnected')"
echo ""

# Check application
echo "Application Status:"
if curl -s http://localhost:5000 >/dev/null; then
    echo "- Web Interface: Accessible"
else
    echo "- Web Interface: Not accessible"
fi

# Check logs
echo "- Last Error: $(tail -1 /var/log/sva_terminal/error.log 2>/dev/null || echo 'No errors')"
echo "- Log Size: $(du -sh /var/log/sva_terminal/ 2>/dev/null | cut -f1 || echo '0')"
EOF

chmod +x scripts/monitor_sva.sh

# Create update script
cat > scripts/update_sva.sh << 'EOF'
#!/bin/bash

# SVA Terminal Update Script
echo "Updating SVA Terminal..."

# Stop services
sudo systemctl stop sva-terminal
sudo systemctl stop nginx

# Backup current version
BACKUP_DIR="/home/sva/backups/update_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /opt/sva_terminal/src/database "$BACKUP_DIR/" 2>/dev/null || true

# Update application code (if using git)
cd /opt/sva_terminal
# git pull origin main

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Run database migrations if needed
python -c "
from src.main import create_app
app = create_app()
with app.app_context():
    from src.models.user import db
    db.create_all()
    print('Database updated')
"

# Restart services
sudo systemctl start sva-terminal
sudo systemctl start nginx

echo "Update completed!"
EOF

chmod +x scripts/update_sva.sh

# Set proper ownership
echo "Setting file permissions..."
chown -R $SVA_USER:$SVA_USER "$SVA_APP_DIR"
chown -R $SVA_USER:$SVA_USER "$SVA_HOME"

# Create log directory
mkdir -p /var/log/sva_terminal
chown $SVA_USER:$SVA_USER /var/log/sva_terminal

# Enable and start services
echo "Enabling services..."
systemctl daemon-reload
systemctl enable sva-terminal
systemctl enable nginx

# Test nginx configuration
nginx -t

# Create desktop shortcut for admin access
cat > "$SVA_HOME/Desktop/SVA Admin.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=SVA Admin
Comment=SVA Terminal Administration
Exec=chromium-browser http://localhost:5000
Icon=applications-system
Terminal=false
Categories=System;
EOF

chmod +x "$SVA_HOME/Desktop/SVA Admin.desktop"
chown $SVA_USER:$SVA_USER "$SVA_HOME/Desktop/SVA Admin.desktop"

# Create installation verification script
cat > scripts/verify_installation.sh << 'EOF'
#!/bin/bash

echo "SVA Terminal Installation Verification"
echo "====================================="

# Check Python environment
echo "Python Environment:"
source /opt/sva_terminal/venv/bin/activate
python --version
echo "Flask: $(python -c 'import flask; print(flask.__version__)')"
echo "OpenCV: $(python -c 'import cv2; print(cv2.__version__)')"
echo "MediaPipe: $(python -c 'import mediapipe; print(mediapipe.__version__)')"
echo ""

# Check services
echo "Services:"
systemctl status sva-terminal --no-pager -l
systemctl status nginx --no-pager -l
echo ""

# Check network
echo "Network Test:"
curl -s http://localhost:5000 >/dev/null && echo "✓ Application accessible" || echo "✗ Application not accessible"
curl -s http://localhost/api/students >/dev/null && echo "✓ API accessible" || echo "✗ API not accessible"
echo ""

# Check hardware
echo "Hardware:"
ls /dev/video* 2>/dev/null && echo "✓ Camera devices found" || echo "✗ No camera devices"
lsusb | grep -i fingerprint && echo "✓ Fingerprint scanner found" || echo "✗ No fingerprint scanner"
echo ""

echo "Installation verification completed!"
EOF

chmod +x scripts/verify_installation.sh

echo "=========================================="
echo "SVA Terminal deployment completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy your application source code to $SVA_APP_DIR/src/"
echo "2. Run: $SVA_APP_DIR/scripts/verify_installation.sh"
echo "3. Start services: sudo systemctl start sva-terminal nginx"
echo "4. Access the application at: http://localhost"
echo ""
echo "Management scripts:"
echo "- Start: $SVA_APP_DIR/scripts/start_sva.sh"
echo "- Monitor: $SVA_APP_DIR/scripts/monitor_sva.sh"
echo "- Update: $SVA_APP_DIR/scripts/update_sva.sh"
echo "- Verify: $SVA_APP_DIR/scripts/verify_installation.sh"
echo ""
echo "For kiosk mode, run: $SVA_APP_DIR/scripts/setup_kiosk.sh"
echo "For security hardening, run: $SVA_APP_DIR/scripts/security_hardening.sh"

