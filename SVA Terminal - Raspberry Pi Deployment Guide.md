# SVA Terminal - Raspberry Pi Deployment Guide

## Overview

The Student Verification Assistant (SVA) Terminal is a comprehensive biometric verification system designed for examination environments. This guide covers the complete deployment process on a Raspberry Pi 4.

## System Requirements

### Hardware Requirements
- **Raspberry Pi 4** (4GB RAM recommended)
- **MicroSD Card** (32GB minimum, Class 10)
- **USB Camera** (compatible with V4L2)
- **USB Fingerprint Scanner** (compatible with libusb)
- **HDMI Display** (touchscreen recommended)
- **Ethernet/WiFi Connection**
- **Power Supply** (5V 3A)

### Software Requirements
- **Raspberry Pi OS** (Bullseye or newer)
- **Python 3.9+**
- **Node.js 16+** (for development)
- **Git** (for version control)

## Pre-Installation Setup

### 1. Prepare Raspberry Pi OS

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git python3-pip python3-venv curl wget vim
```

### 2. Enable Camera and Hardware Interfaces

```bash
# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options > Camera > Enable

# Add user to video group
sudo usermod -a -G video $USER

# Reboot to apply changes
sudo reboot
```

### 3. Configure Network (Optional)

For static IP configuration:

```bash
sudo nano /etc/dhcpcd.conf

# Add the following lines:
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

## Installation Process

### Step 1: Download SVA Terminal

```bash
# Clone the repository (or copy files)
git clone <repository-url> /tmp/sva_terminal
cd /tmp/sva_terminal

# Or copy from USB/network location
# cp -r /path/to/sva_terminal /tmp/
```

### Step 2: Run Deployment Script

```bash
# Make deployment script executable
chmod +x scripts/deploy_raspberry_pi.sh

# Run deployment as root
sudo ./scripts/deploy_raspberry_pi.sh
```

### Step 3: Copy Application Files

```bash
# Copy source code to deployment directory
sudo cp -r src/* /opt/sva_terminal/src/
sudo chown -R sva:sva /opt/sva_terminal
```

### Step 4: Verify Installation

```bash
# Run verification script
sudo /opt/sva_terminal/scripts/verify_installation.sh

# Check service status
sudo systemctl status sva-terminal
sudo systemctl status nginx
```

## Kiosk Mode Setup

### Enable Kiosk Mode

```bash
# Run kiosk setup script
sudo /opt/sva_terminal/scripts/setup_kiosk.sh

# Reboot to activate kiosk mode
sudo reboot
```

### Kiosk Mode Features
- **Auto-login** as SVA user
- **Full-screen browser** with SVA Terminal
- **Disabled desktop** environment
- **Touch-friendly** interface
- **Auto-restart** on crashes

### Exit Kiosk Mode

```bash
# Press Ctrl+Alt+F1 to access terminal
# Login as pi user
# To disable kiosk mode temporarily:
sudo systemctl stop lightdm

# To permanently disable:
sudo systemctl disable lightdm
```

## Security Hardening

### Apply Security Measures

```bash
# Run security hardening script
sudo /opt/sva_terminal/scripts/security_hardening.sh
```

### Security Features Implemented
- **Firewall (UFW)** with restricted access
- **Fail2ban** for intrusion prevention
- **SSH hardening** with secure configuration
- **Automatic security updates**
- **System monitoring** and alerting
- **Regular backups** and maintenance

### Security Best Practices

1. **Change Default Passwords**
   ```bash
   # Change pi user password
   passwd
   
   # Change sva user password
   sudo passwd sva
   ```

2. **Set Up SSH Keys** (if remote access needed)
   ```bash
   # Generate SSH key pair
   ssh-keygen -t rsa -b 4096
   
   # Copy public key to authorized_keys
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   ```

3. **Regular Updates**
   ```bash
   # Manual system update
   sudo apt update && sudo apt upgrade -y
   
   # Update SVA Terminal
   sudo /opt/sva_terminal/scripts/update_sva.sh
   ```

## Configuration

### Application Configuration

Edit `/opt/sva_terminal/config/production.py`:

```python
# Database settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/sva_terminal.db'

# Biometric thresholds
FACE_RECOGNITION_THRESHOLD = 0.7
FINGERPRINT_RECOGNITION_THRESHOLD = 0.7

# Hardware settings
CAMERA_DEVICE = 0
FINGERPRINT_DEVICE = '/dev/ttyUSB0'
```

### Hardware Configuration

#### Camera Setup
```bash
# Test camera
v4l2-ctl --list-devices

# Adjust camera settings
v4l2-ctl --set-ctrl brightness=128
v4l2-ctl --set-ctrl contrast=128
```

#### Fingerprint Scanner Setup
```bash
# Check USB devices
lsusb

# Set device permissions
sudo nano /etc/udev/rules.d/99-sva-devices.rules
# Add device-specific rules
```

## Operation and Maintenance

### Daily Operations

1. **System Monitoring**
   ```bash
   # Check system status
   /opt/sva_terminal/scripts/monitor_sva.sh
   
   # Check security status
   /opt/sva_terminal/scripts/security_status.sh
   ```

2. **View Logs**
   ```bash
   # Application logs
   tail -f /var/log/sva_terminal/app.log
   
   # System logs
   journalctl -u sva-terminal -f
   ```

3. **Backup Data**
   ```bash
   # Manual backup
   /opt/sva_terminal/scripts/backup_system.sh
   
   # Automated backups run weekly via cron
   ```

### Maintenance Tasks

#### Weekly Maintenance
- Review security logs
- Check system updates
- Verify backup integrity
- Monitor disk usage

#### Monthly Maintenance
- Full system backup
- Security audit
- Performance review
- Hardware inspection

### Troubleshooting

#### Common Issues

1. **Application Won't Start**
   ```bash
   # Check service status
   sudo systemctl status sva-terminal
   
   # Check logs
   journalctl -u sva-terminal --no-pager
   
   # Restart service
   sudo systemctl restart sva-terminal
   ```

2. **Camera Not Working**
   ```bash
   # Check camera device
   ls /dev/video*
   
   # Test camera
   fswebcam test.jpg
   
   # Check permissions
   groups $USER | grep video
   ```

3. **Fingerprint Scanner Issues**
   ```bash
   # Check USB connection
   lsusb | grep -i fingerprint
   
   # Check device permissions
   ls -la /dev/ttyUSB*
   
   # Restart udev
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

4. **Network Connectivity**
   ```bash
   # Check network status
   ip addr show
   
   # Test connectivity
   ping google.com
   
   # Restart networking
   sudo systemctl restart networking
   ```

#### Performance Optimization

1. **Memory Optimization**
   ```bash
   # Increase GPU memory split
   sudo nano /boot/config.txt
   # Add: gpu_mem=128
   ```

2. **Storage Optimization**
   ```bash
   # Clean temporary files
   sudo apt autoremove
   sudo apt autoclean
   
   # Rotate logs
   sudo logrotate -f /etc/logrotate.conf
   ```

## Backup and Recovery

### Backup Strategy

1. **Automatic Backups**
   - Daily: Application data and logs
   - Weekly: Full system configuration
   - Monthly: Complete system image

2. **Manual Backup**
   ```bash
   # Create full backup
   /opt/sva_terminal/scripts/backup_system.sh
   
   # Backup to external storage
   rsync -av /home/sva/backups/ /media/usb/sva_backups/
   ```

### Recovery Procedures

1. **Application Recovery**
   ```bash
   # Restore from backup
   sudo systemctl stop sva-terminal
   cp -r /home/sva/backups/latest/database/* /opt/sva_terminal/src/database/
   sudo systemctl start sva-terminal
   ```

2. **System Recovery**
   ```bash
   # Restore configuration
   sudo cp /home/sva/backups/latest/config/* /etc/
   sudo systemctl daemon-reload
   ```

## Support and Documentation

### Log Locations
- Application logs: `/var/log/sva_terminal/`
- System logs: `/var/log/syslog`
- Security logs: `/var/log/auth.log`

### Configuration Files
- Application: `/opt/sva_terminal/config/`
- System services: `/etc/systemd/system/`
- Security: `/etc/fail2ban/`, `/etc/ufw/`

### Useful Commands

```bash
# Service management
sudo systemctl start|stop|restart|status sva-terminal

# View real-time logs
journalctl -u sva-terminal -f

# Check system resources
htop
df -h
free -h

# Network diagnostics
netstat -tulpn
ss -tulpn
```

## Conclusion

This deployment guide provides a comprehensive setup for the SVA Terminal on Raspberry Pi 4. The system is designed for reliability, security, and ease of maintenance in examination environments.

For additional support or customization requirements, refer to the technical documentation or contact the development team.

