#!/bin/bash

# SVA Terminal Kiosk Mode Setup Script
# This script configures a Raspberry Pi 4 for kiosk mode operation

set -e

echo "=========================================="
echo "SVA Terminal Kiosk Mode Setup"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (use sudo)"
    exit 1
fi

# Update system packages
echo "Updating system packages..."
apt update && apt upgrade -y

# Install required packages for kiosk mode
echo "Installing kiosk mode packages..."
apt install -y \
    chromium-browser \
    unclutter \
    xdotool \
    xinit \
    x11-xserver-utils \
    lightdm \
    openbox \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    vim \
    htop \
    screen \
    supervisor

# Install hardware-specific packages
echo "Installing hardware support packages..."
apt install -y \
    v4l-utils \
    fswebcam \
    libusb-1.0-0-dev \
    libusb-dev \
    udev

# Create SVA user if it doesn't exist
if ! id "sva" &>/dev/null; then
    echo "Creating SVA user..."
    useradd -m -s /bin/bash sva
    usermod -a -G video,audio,dialout,plugdev sva
fi

# Create kiosk directories
echo "Creating kiosk directories..."
mkdir -p /home/sva/.config/openbox
mkdir -p /home/sva/.config/chromium
mkdir -p /opt/sva_terminal
mkdir -p /var/log/sva_terminal

# Set up auto-login for SVA user
echo "Configuring auto-login..."
cat > /etc/lightdm/lightdm.conf << EOF
[Seat:*]
autologin-user=sva
autologin-user-timeout=0
user-session=openbox
EOF

# Configure Openbox for kiosk mode
echo "Configuring Openbox..."
cat > /home/sva/.config/openbox/autostart << 'EOF'
#!/bin/bash

# Disable screen blanking and power management
xset s off
xset -dpms
xset s noblank

# Hide cursor when inactive
unclutter -idle 1 &

# Wait for network connectivity
while ! ping -c 1 google.com &> /dev/null; do
    sleep 1
done

# Start SVA Terminal application
cd /opt/sva_terminal
source venv/bin/activate
python src/main.py &

# Wait for Flask server to start
sleep 10

# Start Chromium in kiosk mode
chromium-browser \
    --kiosk \
    --no-sandbox \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    --disable-background-timer-throttling \
    --disable-backgrounding-occluded-windows \
    --disable-renderer-backgrounding \
    --disable-features=TranslateUI \
    --disable-component-extensions-with-background-pages \
    --disable-extensions \
    --disable-plugins \
    --disable-sync \
    --disable-translate \
    --no-first-run \
    --fast \
    --fast-start \
    --disable-default-apps \
    --disable-popup-blocking \
    --disable-prompt-on-repost \
    --no-message-box \
    --touch-events=enabled \
    --enable-pinch \
    --overscroll-history-navigation=0 \
    --disable-pinch \
    --disable-features=VizDisplayCompositor \
    --start-fullscreen \
    http://localhost:5000
EOF

# Make autostart executable
chmod +x /home/sva/.config/openbox/autostart

# Configure Chromium preferences
echo "Configuring Chromium preferences..."
mkdir -p /home/sva/.config/chromium/Default
cat > /home/sva/.config/chromium/Default/Preferences << 'EOF'
{
   "browser": {
      "show_home_button": false
   },
   "bookmark_bar": {
      "show_on_all_tabs": false
   },
   "distribution": {
      "make_chrome_default": false,
      "make_chrome_default_for_user": false,
      "system_level": false
   },
   "first_run_tabs": [ "http://localhost:5000" ],
   "homepage": "http://localhost:5000",
   "homepage_is_newtabpage": false,
   "session": {
      "restore_on_startup": 4,
      "startup_urls": [ "http://localhost:5000" ]
   }
}
EOF

# Set up supervisor for SVA Terminal service
echo "Configuring supervisor for SVA Terminal..."
cat > /etc/supervisor/conf.d/sva_terminal.conf << 'EOF'
[program:sva_terminal]
command=/opt/sva_terminal/venv/bin/python /opt/sva_terminal/src/main.py
directory=/opt/sva_terminal
user=sva
autostart=true
autorestart=true
stderr_logfile=/var/log/sva_terminal/error.log
stdout_logfile=/var/log/sva_terminal/output.log
environment=DISPLAY=":0"
EOF

# Create systemd service for kiosk mode
echo "Creating systemd service..."
cat > /etc/systemd/system/sva-kiosk.service << 'EOF'
[Unit]
Description=SVA Terminal Kiosk Mode
After=graphical-session.target

[Service]
Type=simple
User=sva
Environment=DISPLAY=:0
ExecStart=/home/sva/.config/openbox/autostart
Restart=always
RestartSec=10

[Install]
WantedBy=graphical-session.target
EOF

# Configure udev rules for hardware devices
echo "Configuring udev rules..."
cat > /etc/udev/rules.d/99-sva-devices.rules << 'EOF'
# USB Camera devices
SUBSYSTEM=="video4linux", GROUP="video", MODE="0664"
KERNEL=="video[0-9]*", GROUP="video", MODE="0664"

# USB Fingerprint scanner devices
SUBSYSTEM=="usb", ATTR{idVendor}=="1234", ATTR{idProduct}=="5678", GROUP="plugdev", MODE="0664"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", GROUP="plugdev", MODE="0664"

# Generic USB devices for biometric scanners
SUBSYSTEM=="usb", ATTR{bDeviceClass}=="ff", GROUP="plugdev", MODE="0664"
EOF

# Set up log rotation
echo "Configuring log rotation..."
cat > /etc/logrotate.d/sva_terminal << 'EOF'
/var/log/sva_terminal/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 sva sva
}
EOF

# Configure network settings for stability
echo "Configuring network settings..."
cat >> /etc/dhcpcd.conf << 'EOF'

# SVA Terminal network configuration
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4

# Disable power management for WiFi
interface wlan0
nohook wpa_supplicant
EOF

# Disable unnecessary services
echo "Disabling unnecessary services..."
systemctl disable bluetooth
systemctl disable cups
systemctl disable avahi-daemon
systemctl disable triggerhappy

# Configure boot options
echo "Configuring boot options..."
cat >> /boot/config.txt << 'EOF'

# SVA Terminal configuration
# Disable rainbow splash screen
disable_splash=1

# Set GPU memory split
gpu_mem=128

# Enable camera
start_x=1

# Disable audio (if not needed)
dtparam=audio=off

# Set HDMI mode (adjust as needed)
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
EOF

# Configure cmdline.txt for faster boot
sed -i 's/$/ quiet splash loglevel=1 logo.nologo vt.global_cursor_default=0/' /boot/cmdline.txt

# Set ownership of SVA files
chown -R sva:sva /home/sva
chown -R sva:sva /var/log/sva_terminal

# Create installation script for SVA Terminal
cat > /opt/install_sva_terminal.sh << 'EOF'
#!/bin/bash

# SVA Terminal Installation Script
echo "Installing SVA Terminal application..."

# Clone or copy SVA Terminal application
if [ -d "/opt/sva_terminal" ]; then
    echo "SVA Terminal directory already exists"
else
    echo "Creating SVA Terminal directory..."
    mkdir -p /opt/sva_terminal
fi

# Set up Python virtual environment
cd /opt/sva_terminal
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install flask flask-cors flask-sqlalchemy opencv-python-headless mediapipe numpy

echo "SVA Terminal installation completed!"
echo "Copy your SVA Terminal application files to /opt/sva_terminal/"
EOF

chmod +x /opt/install_sva_terminal.sh

# Create maintenance scripts
mkdir -p /opt/sva_terminal/scripts

cat > /opt/sva_terminal/scripts/restart_kiosk.sh << 'EOF'
#!/bin/bash
# Restart kiosk mode
sudo systemctl restart lightdm
EOF

cat > /opt/sva_terminal/scripts/update_app.sh << 'EOF'
#!/bin/bash
# Update SVA Terminal application
cd /opt/sva_terminal
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart supervisor
EOF

cat > /opt/sva_terminal/scripts/backup_data.sh << 'EOF'
#!/bin/bash
# Backup SVA Terminal data
BACKUP_DIR="/home/sva/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /opt/sva_terminal/src/database "$BACKUP_DIR/"
cp /var/log/sva_terminal/*.log "$BACKUP_DIR/"
echo "Backup created in $BACKUP_DIR"
EOF

chmod +x /opt/sva_terminal/scripts/*.sh

# Enable services
systemctl enable supervisor
systemctl enable lightdm

# Reload udev rules
udevadm control --reload-rules
udevadm trigger

echo "=========================================="
echo "Kiosk mode setup completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy your SVA Terminal application to /opt/sva_terminal/"
echo "2. Run: /opt/install_sva_terminal.sh"
echo "3. Reboot the system: sudo reboot"
echo ""
echo "Maintenance scripts available in /opt/sva_terminal/scripts/:"
echo "- restart_kiosk.sh: Restart kiosk mode"
echo "- update_app.sh: Update application"
echo "- backup_data.sh: Backup data"
echo ""
echo "The system will automatically start in kiosk mode after reboot."
echo "To exit kiosk mode, press Ctrl+Alt+F1 and login as pi user."

