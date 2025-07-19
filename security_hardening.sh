#!/bin/bash

# SVA Terminal Security Hardening Script
# This script implements security measures for the SVA terminal

set -e

echo "=========================================="
echo "SVA Terminal Security Hardening"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (use sudo)"
    exit 1
fi

# Update system and install security packages
echo "Installing security packages..."
apt update
apt install -y \
    fail2ban \
    ufw \
    rkhunter \
    chkrootkit \
    lynis \
    unattended-upgrades \
    apt-listchanges

# Configure firewall
echo "Configuring firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (if needed for remote management)
ufw allow 22/tcp

# Allow local Flask application
ufw allow from 127.0.0.1 to any port 5000

# Allow local network access (adjust as needed)
ufw allow from 192.168.1.0/24 to any port 5000

# Enable firewall
ufw --force enable

# Configure fail2ban
echo "Configuring fail2ban..."
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
backend = systemd

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s

[sva-terminal]
enabled = true
port = 5000
logpath = /var/log/sva_terminal/error.log
maxretry = 5
bantime = 1800
findtime = 300
filter = sva-terminal

[nginx-http-auth]
enabled = false
EOF

# Create fail2ban filter for SVA Terminal
cat > /etc/fail2ban/filter.d/sva-terminal.conf << 'EOF'
[Definition]
failregex = ^.*\[.*\] ".*" 40[0-9] .*$
            ^.*authentication failed.*$
            ^.*verification failed.*$
ignoreregex =
EOF

# Configure automatic security updates
echo "Configuring automatic security updates..."
cat > /etc/apt/apt.conf.d/50unattended-upgrades << 'EOF'
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::DevRelease "false";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
EOF

cat > /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

# Secure SSH configuration
echo "Securing SSH configuration..."
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

cat > /etc/ssh/sshd_config << 'EOF'
# SVA Terminal SSH Configuration
Port 22
Protocol 2

# Authentication
PermitRootLogin no
PasswordAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Security settings
PermitEmptyPasswords no
MaxAuthTries 3
MaxSessions 2
ClientAliveInterval 300
ClientAliveCountMax 2

# Disable unused features
X11Forwarding no
AllowTcpForwarding no
GatewayPorts no
PermitTunnel no

# Restrict users
AllowUsers pi sva

# Logging
SyslogFacility AUTH
LogLevel INFO
EOF

# Set file permissions
echo "Setting secure file permissions..."
chmod 700 /home/sva/.ssh 2>/dev/null || true
chmod 600 /home/sva/.ssh/authorized_keys 2>/dev/null || true
chmod 700 /home/pi/.ssh 2>/dev/null || true
chmod 600 /home/pi/.ssh/authorized_keys 2>/dev/null || true

# Secure important directories
chmod 750 /opt/sva_terminal
chmod 640 /opt/sva_terminal/src/database/*.db 2>/dev/null || true
chmod 750 /var/log/sva_terminal

# Configure system limits
echo "Configuring system limits..."
cat >> /etc/security/limits.conf << 'EOF'

# SVA Terminal security limits
* soft nofile 1024
* hard nofile 2048
* soft nproc 512
* hard nproc 1024
sva soft nofile 2048
sva hard nofile 4096
EOF

# Disable unnecessary network services
echo "Disabling unnecessary services..."
systemctl disable avahi-daemon 2>/dev/null || true
systemctl disable cups 2>/dev/null || true
systemctl disable bluetooth 2>/dev/null || true
systemctl disable triggerhappy 2>/dev/null || true

# Configure kernel parameters for security
echo "Configuring kernel security parameters..."
cat >> /etc/sysctl.conf << 'EOF'

# SVA Terminal security settings
# Disable IP forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Disable source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Disable ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# Enable SYN flood protection
net.ipv4.tcp_syncookies = 1

# Ignore ping requests
net.ipv4.icmp_echo_ignore_all = 1

# Log suspicious packets
net.ipv4.conf.all.log_martians = 1

# Disable IPv6 if not needed
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
EOF

# Create security monitoring script
cat > /opt/sva_terminal/scripts/security_check.sh << 'EOF'
#!/bin/bash

# SVA Terminal Security Check Script
echo "=========================================="
echo "SVA Terminal Security Check"
echo "Date: $(date)"
echo "=========================================="

# Check system updates
echo "Checking for system updates..."
apt list --upgradable 2>/dev/null | grep -v "WARNING" | wc -l | xargs echo "Available updates:"

# Check failed login attempts
echo "Recent failed login attempts:"
grep "Failed password" /var/log/auth.log | tail -5 2>/dev/null || echo "No recent failed attempts"

# Check firewall status
echo "Firewall status:"
ufw status

# Check running services
echo "Critical services status:"
systemctl is-active sva_terminal supervisor lightdm

# Check disk usage
echo "Disk usage:"
df -h / | tail -1

# Check memory usage
echo "Memory usage:"
free -h | grep Mem

# Check for rootkits (quick scan)
echo "Quick rootkit scan:"
chkrootkit -q 2>/dev/null | head -5 || echo "Rootkit scanner not available"

# Check log file sizes
echo "Log file sizes:"
du -sh /var/log/sva_terminal/* 2>/dev/null || echo "No log files found"

echo "=========================================="
echo "Security check completed"
echo "=========================================="
EOF

chmod +x /opt/sva_terminal/scripts/security_check.sh

# Create backup and recovery script
cat > /opt/sva_terminal/scripts/backup_system.sh << 'EOF'
#!/bin/bash

# SVA Terminal System Backup Script
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/sva/backups/system_$BACKUP_DATE"

echo "Creating system backup in $BACKUP_DIR..."
mkdir -p "$BACKUP_DIR"

# Backup application data
cp -r /opt/sva_terminal/src/database "$BACKUP_DIR/" 2>/dev/null || echo "No database found"

# Backup configuration files
mkdir -p "$BACKUP_DIR/config"
cp /etc/ssh/sshd_config "$BACKUP_DIR/config/" 2>/dev/null
cp /etc/fail2ban/jail.local "$BACKUP_DIR/config/" 2>/dev/null
cp /etc/ufw/user.rules "$BACKUP_DIR/config/" 2>/dev/null
cp /home/sva/.config/openbox/autostart "$BACKUP_DIR/config/" 2>/dev/null

# Backup logs
mkdir -p "$BACKUP_DIR/logs"
cp /var/log/sva_terminal/*.log "$BACKUP_DIR/logs/" 2>/dev/null || echo "No logs found"

# Create system info
echo "System backup created on $(date)" > "$BACKUP_DIR/backup_info.txt"
echo "Hostname: $(hostname)" >> "$BACKUP_DIR/backup_info.txt"
echo "Kernel: $(uname -r)" >> "$BACKUP_DIR/backup_info.txt"
echo "Uptime: $(uptime)" >> "$BACKUP_DIR/backup_info.txt"

# Compress backup
cd /home/sva/backups
tar -czf "system_$BACKUP_DATE.tar.gz" "system_$BACKUP_DATE"
rm -rf "system_$BACKUP_DATE"

echo "System backup completed: system_$BACKUP_DATE.tar.gz"
EOF

chmod +x /opt/sva_terminal/scripts/backup_system.sh

# Set up cron jobs for maintenance
echo "Setting up maintenance cron jobs..."
cat > /tmp/sva_crontab << 'EOF'
# SVA Terminal maintenance cron jobs
# Daily security check at 2 AM
0 2 * * * /opt/sva_terminal/scripts/security_check.sh >> /var/log/sva_terminal/security_check.log 2>&1

# Weekly system backup at 3 AM on Sundays
0 3 * * 0 /opt/sva_terminal/scripts/backup_system.sh >> /var/log/sva_terminal/backup.log 2>&1

# Daily log cleanup at 4 AM
0 4 * * * find /var/log/sva_terminal -name "*.log" -mtime +7 -delete

# Monthly rootkit scan at 1 AM on 1st of month
0 1 1 * * rkhunter --check --sk --nocolors >> /var/log/sva_terminal/rkhunter.log 2>&1
EOF

crontab -u sva /tmp/sva_crontab
rm /tmp/sva_crontab

# Configure log monitoring
echo "Configuring log monitoring..."
cat > /etc/rsyslog.d/50-sva-terminal.conf << 'EOF'
# SVA Terminal log configuration
if $programname == 'sva_terminal' then /var/log/sva_terminal/sva.log
& stop
EOF

# Restart services
echo "Restarting security services..."
systemctl restart fail2ban
systemctl restart ssh
systemctl restart rsyslog

# Enable services
systemctl enable fail2ban
systemctl enable ufw
systemctl enable unattended-upgrades

# Apply sysctl settings
sysctl -p

# Create security status script
cat > /opt/sva_terminal/scripts/security_status.sh << 'EOF'
#!/bin/bash

echo "SVA Terminal Security Status"
echo "============================"
echo "Firewall: $(ufw status | head -1)"
echo "Fail2ban: $(systemctl is-active fail2ban)"
echo "SSH: $(systemctl is-active ssh)"
echo "Auto-updates: $(systemctl is-active unattended-upgrades)"
echo "Last security check: $(ls -la /var/log/sva_terminal/security_check.log 2>/dev/null | awk '{print $6, $7, $8}' || echo 'Never')"
echo "Last backup: $(ls -la /home/sva/backups/*.tar.gz 2>/dev/null | tail -1 | awk '{print $6, $7, $8}' || echo 'Never')"
EOF

chmod +x /opt/sva_terminal/scripts/security_status.sh

echo "=========================================="
echo "Security hardening completed!"
echo "=========================================="
echo ""
echo "Security measures implemented:"
echo "- Firewall (UFW) configured and enabled"
echo "- Fail2ban configured for intrusion prevention"
echo "- SSH hardened with secure configuration"
echo "- Automatic security updates enabled"
echo "- System limits and kernel parameters configured"
echo "- Security monitoring and backup scripts created"
echo "- Cron jobs set up for maintenance"
echo ""
echo "Security scripts available:"
echo "- /opt/sva_terminal/scripts/security_check.sh"
echo "- /opt/sva_terminal/scripts/backup_system.sh"
echo "- /opt/sva_terminal/scripts/security_status.sh"
echo ""
echo "Run security_status.sh to check current security status."

