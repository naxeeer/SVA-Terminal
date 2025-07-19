# Student Verification Assistant (SVA) Terminal

## Complete Project Documentation

**Version:** 1.0  
**Date:** July 2025  
**Platform:** Raspberry Pi 4  
**Author:** SVA Development Team  

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Hardware Requirements](#hardware-requirements)
4. [Software Components](#software-components)
5. [Installation Guide](#installation-guide)
6. [Configuration](#configuration)
7. [User Manual](#user-manual)
8. [Administrator Guide](#administrator-guide)
9. [API Documentation](#api-documentation)
10. [Security Features](#security-features)
11. [Troubleshooting](#troubleshooting)
12. [Maintenance](#maintenance)
13. [Development Guide](#development-guide)
14. [Testing](#testing)
15. [Appendices](#appendices)

---


## 1. Project Overview

### 1.1 Introduction

The Student Verification Assistant (SVA) Terminal is a comprehensive biometric verification system designed specifically for examination environments in educational institutions. The system provides secure, reliable, and efficient student identity verification through dual biometric authentication using face recognition and fingerprint scanning technologies.

### 1.2 Purpose and Scope

The SVA Terminal addresses the critical need for accurate student identification during examinations, preventing impersonation and ensuring academic integrity. The system operates in a kiosk mode environment on Raspberry Pi 4 hardware, providing a cost-effective and scalable solution for educational institutions of all sizes.

**Key Objectives:**
- Eliminate examination fraud through biometric verification
- Streamline the student check-in process for examinations
- Provide comprehensive audit trails for verification activities
- Ensure system reliability and security in examination environments
- Offer an intuitive interface for both students and administrators

### 1.3 Key Features

**Student Verification Features:**
- **Dual Biometric Authentication**: Face recognition and fingerprint scanning for enhanced security
- **Real-time Verification**: Instant identity confirmation with detailed feedback
- **Course Registration Validation**: Automatic verification of student enrollment in examination courses
- **User-friendly Interface**: Step-by-step verification process with clear visual guidance
- **Accessibility Support**: Touch-screen compatible interface with large, clear buttons

**Administrative Features:**
- **Student Management**: Complete CRUD operations for student records
- **Course Management**: Course creation, modification, and enrollment tracking
- **Exam Session Management**: Scheduling and activation of examination sessions
- **Verification Logging**: Comprehensive audit trails with detailed verification records
- **Biometric Enrollment**: Secure enrollment of student biometric data
- **Real-time Monitoring**: Live dashboard showing system status and verification activities

**System Features:**
- **Kiosk Mode Operation**: Secure, locked-down environment preventing unauthorized access
- **Offline Capability**: Local database storage ensuring operation without internet dependency
- **Security Hardening**: Multiple layers of security including firewall, intrusion detection, and access controls
- **Automatic Backup**: Scheduled data backup and recovery procedures
- **Performance Monitoring**: System health monitoring with automated alerts

### 1.4 Target Users

**Primary Users:**
- **Students**: Individuals taking examinations who need identity verification
- **Examination Proctors**: Staff members supervising examination sessions
- **Academic Administrators**: Personnel responsible for examination management and student records

**Secondary Users:**
- **IT Administrators**: Technical staff responsible for system maintenance and support
- **Security Personnel**: Staff involved in academic integrity and security oversight
- **Institutional Management**: Leadership requiring verification reports and system analytics

### 1.5 System Benefits

**For Educational Institutions:**
- **Enhanced Security**: Virtually eliminates examination impersonation
- **Improved Efficiency**: Reduces manual verification time and effort
- **Comprehensive Auditing**: Complete verification records for compliance and investigation
- **Cost-effective Solution**: Low-cost hardware with high-value security benefits
- **Scalable Implementation**: Easy deployment across multiple examination venues

**For Students:**
- **Quick Verification**: Fast, contactless identity confirmation
- **Reduced Wait Times**: Streamlined check-in process
- **Privacy Protection**: Secure biometric data handling with local storage
- **User-friendly Experience**: Intuitive interface requiring minimal technical knowledge

**For Administrators:**
- **Centralized Management**: Single interface for all verification and student management tasks
- **Real-time Insights**: Live monitoring of verification activities and system status
- **Flexible Configuration**: Customizable settings for different examination scenarios
- **Automated Reporting**: Comprehensive reports for analysis and compliance

### 1.6 Technology Stack

**Hardware Platform:**
- **Raspberry Pi 4**: Primary computing platform with 4GB RAM
- **USB Camera**: High-resolution camera for face recognition
- **USB Fingerprint Scanner**: Professional-grade fingerprint capture device
- **Touchscreen Display**: Interactive display for user interface
- **Network Connectivity**: Ethernet and WiFi support for data synchronization

**Software Components:**
- **Operating System**: Raspberry Pi OS (Debian-based Linux)
- **Backend Framework**: Flask (Python) with SQLAlchemy ORM
- **Database**: SQLite for local data storage
- **Frontend**: HTML5, CSS3, JavaScript with responsive design
- **Biometric Processing**: OpenCV and MediaPipe for computer vision
- **Security**: UFW firewall, Fail2ban intrusion detection, SSH hardening
- **System Services**: Systemd for service management, Nginx for web serving

**Development Tools:**
- **Programming Languages**: Python 3.11, JavaScript ES6, HTML5, CSS3
- **Version Control**: Git for source code management
- **Testing Framework**: Python unittest for automated testing
- **Documentation**: Markdown for comprehensive documentation
- **Deployment**: Automated scripts for production deployment

### 1.7 Compliance and Standards

The SVA Terminal is designed to comply with relevant educational and data protection standards:

- **FERPA Compliance**: Student privacy protection in accordance with Family Educational Rights and Privacy Act
- **Data Protection**: Local data storage minimizing privacy risks
- **Accessibility Standards**: Interface design following WCAG guidelines
- **Security Standards**: Implementation of industry-standard security practices
- **Academic Integrity**: Support for institutional academic integrity policies

### 1.8 Project Deliverables

**Software Deliverables:**
- Complete SVA Terminal application with source code
- Comprehensive documentation including user manuals and technical guides
- Automated deployment scripts for Raspberry Pi
- Security hardening and kiosk mode configuration scripts
- Testing suite with automated system tests

**Documentation Deliverables:**
- System architecture documentation
- Installation and deployment guides
- User manuals for students and administrators
- API documentation for developers
- Security configuration and best practices guide
- Troubleshooting and maintenance procedures

**Support Materials:**
- Hardware procurement guide
- Training materials for administrators
- System monitoring and backup procedures
- Performance optimization guidelines
- Future enhancement roadmap



## 2. System Architecture

### 2.1 Overall Architecture

The SVA Terminal follows a modular, three-tier architecture designed for reliability, security, and maintainability. The system is built on a foundation of proven technologies and follows industry best practices for embedded systems and web applications.

**Architecture Layers:**

1. **Presentation Layer**: Web-based user interface with responsive design
2. **Application Layer**: Flask-based backend with business logic and API endpoints
3. **Data Layer**: SQLite database with biometric data storage and management

### 2.2 System Components

**Core Components:**

**Frontend Interface:**
- **Student Verification Interface**: Step-by-step verification workflow
- **Administrative Panel**: Comprehensive management interface with tabbed navigation
- **Real-time Feedback**: Dynamic status updates and user guidance
- **Responsive Design**: Touch-screen optimized interface supporting various display sizes

**Backend Services:**
- **Flask Application Server**: Main application logic and request handling
- **RESTful API**: Standardized endpoints for all system operations
- **Database ORM**: SQLAlchemy for database abstraction and management
- **Biometric Services**: Specialized modules for face and fingerprint processing
- **Authentication System**: Secure session management and access control

**Data Management:**
- **SQLite Database**: Local storage for all application data
- **Biometric Data Storage**: Secure storage of face encodings and fingerprint templates
- **Audit Logging**: Comprehensive logging of all verification activities
- **Backup System**: Automated data backup and recovery procedures

**Hardware Integration:**
- **Camera Interface**: USB camera integration for face capture
- **Fingerprint Scanner**: USB fingerprint device integration
- **Display Management**: Touchscreen interface control
- **Network Services**: Ethernet and WiFi connectivity management

### 2.3 Data Flow Architecture

**Student Verification Workflow:**

1. **Initiation**: Student approaches terminal and initiates verification
2. **Face Capture**: System captures and processes facial image
3. **Face Recognition**: Comparison against enrolled biometric templates
4. **Student Identification**: Retrieval of student information and course enrollment
5. **Course Validation**: Verification of enrollment in active examination course
6. **Fingerprint Verification**: Secondary biometric confirmation
7. **Result Processing**: Final verification decision and logging
8. **User Feedback**: Display of verification results and next steps

**Administrative Workflow:**

1. **Authentication**: Administrator access to management interface
2. **Data Management**: CRUD operations on students, courses, and exam sessions
3. **Biometric Enrollment**: Secure capture and storage of biometric templates
4. **System Monitoring**: Real-time status monitoring and log review
5. **Configuration Management**: System settings and parameter adjustment
6. **Report Generation**: Verification reports and system analytics

### 2.4 Database Schema

**Core Tables:**

**Students Table:**
- `id`: Primary key (auto-increment)
- `student_id`: Unique student identifier
- `name`: Full student name
- `class_name`: Academic class or year
- `department`: Academic department
- `faculty`: Faculty or school
- `face_encoding`: Biometric face template (Base64 encoded)
- `fingerprint_template`: Biometric fingerprint template (Base64 encoded)
- `created_at`: Record creation timestamp
- `updated_at`: Last modification timestamp

**Courses Table:**
- `id`: Primary key (auto-increment)
- `course_code`: Unique course identifier
- `course_name`: Full course name
- `description`: Course description
- `created_at`: Record creation timestamp

**Exam Sessions Table:**
- `id`: Primary key (auto-increment)
- `course_id`: Foreign key to courses table
- `exam_date`: Scheduled examination date
- `start_time`: Examination start time
- `end_time`: Examination end time
- `duration`: Examination duration in minutes
- `location`: Examination venue
- `is_active`: Session activation status
- `created_at`: Record creation timestamp

**Verification Logs Table:**
- `id`: Primary key (auto-increment)
- `student_id`: Foreign key to students table
- `exam_session_id`: Foreign key to exam sessions table
- `verification_time`: Timestamp of verification attempt
- `face_match_score`: Face recognition confidence score
- `fingerprint_match_score`: Fingerprint recognition confidence score
- `verification_status`: Overall verification result (approved/rejected)
- `error_message`: Error details for failed verifications
- `created_at`: Record creation timestamp

**Enrollment Table:**
- `id`: Primary key (auto-increment)
- `student_id`: Foreign key to students table
- `course_id`: Foreign key to courses table
- `enrollment_date`: Date of course enrollment
- `status`: Enrollment status (active/inactive)

### 2.5 Security Architecture

**Multi-layered Security Approach:**

**Network Security:**
- **Firewall Protection**: UFW firewall with restrictive rules
- **Intrusion Detection**: Fail2ban monitoring for suspicious activities
- **Network Isolation**: Limited network access with specific port restrictions
- **SSH Hardening**: Secure remote access configuration

**Application Security:**
- **Input Validation**: Comprehensive validation of all user inputs
- **SQL Injection Prevention**: Parameterized queries and ORM protection
- **Cross-Site Scripting (XSS) Protection**: Input sanitization and output encoding
- **Session Management**: Secure session handling with timeout controls
- **Access Control**: Role-based access to administrative functions

**Data Security:**
- **Local Storage**: All sensitive data stored locally to minimize exposure
- **Biometric Encryption**: Encrypted storage of biometric templates
- **Database Security**: File-level permissions and access controls
- **Backup Encryption**: Encrypted backup files with secure storage
- **Audit Logging**: Comprehensive logging of all security-relevant events

**Physical Security:**
- **Kiosk Mode**: Locked-down system preventing unauthorized access
- **Hardware Protection**: Secure mounting and cable management
- **Display Security**: Automatic screen locking and timeout controls
- **USB Port Management**: Controlled access to USB devices

### 2.6 Performance Architecture

**Optimization Strategies:**

**Frontend Performance:**
- **Responsive Design**: Efficient CSS and JavaScript for fast rendering
- **Image Optimization**: Compressed images and efficient loading
- **Caching Strategy**: Browser caching for static resources
- **Minimal Dependencies**: Lightweight libraries and frameworks

**Backend Performance:**
- **Database Optimization**: Indexed queries and efficient schema design
- **Memory Management**: Optimized Python code with proper resource cleanup
- **Concurrent Processing**: Efficient handling of multiple requests
- **Biometric Processing**: Optimized algorithms for real-time recognition

**System Performance:**
- **Resource Monitoring**: Continuous monitoring of CPU, memory, and storage
- **Process Management**: Efficient service management and resource allocation
- **Network Optimization**: Optimized network configuration for local operations
- **Storage Management**: Efficient file system usage and cleanup procedures

### 2.7 Scalability Considerations

**Horizontal Scaling:**
- **Multiple Terminals**: Support for multiple SVA terminals in large institutions
- **Load Distribution**: Distributed verification load across multiple devices
- **Data Synchronization**: Centralized data management with local caching
- **Network Architecture**: Scalable network design for institutional deployment

**Vertical Scaling:**
- **Hardware Upgrades**: Support for enhanced Raspberry Pi models
- **Memory Optimization**: Efficient memory usage for larger datasets
- **Storage Expansion**: Support for external storage devices
- **Processing Power**: Optimized algorithms for improved performance

### 2.8 Integration Architecture

**External System Integration:**
- **Student Information Systems**: API integration with institutional SIS
- **Learning Management Systems**: Integration with LMS platforms
- **Identity Management**: LDAP/Active Directory integration capabilities
- **Reporting Systems**: Data export for institutional reporting tools

**Hardware Integration:**
- **Camera Systems**: Support for various USB camera models
- **Fingerprint Scanners**: Compatibility with multiple scanner types
- **Display Devices**: Support for various touchscreen displays
- **Network Hardware**: Ethernet and WiFi adapter compatibility

**Software Integration:**
- **Operating System**: Deep integration with Raspberry Pi OS
- **System Services**: Integration with systemd for service management
- **Monitoring Tools**: Integration with system monitoring utilities
- **Backup Solutions**: Integration with external backup systems


## 3. Hardware Requirements

### 3.1 Minimum System Requirements

**Primary Computing Platform:**
- **Raspberry Pi 4 Model B**: 4GB RAM (recommended), 2GB RAM (minimum)
- **MicroSD Card**: 32GB Class 10 (minimum), 64GB Class 10 (recommended)
- **Power Supply**: Official Raspberry Pi 4 Power Supply (5V 3A USB-C)
- **Cooling**: Heat sink and fan (recommended for continuous operation)

**Biometric Hardware:**
- **USB Camera**: 1080p resolution minimum, autofocus capability preferred
  - Recommended models: Logitech C920, C922, or equivalent
  - Requirements: USB 2.0/3.0 compatible, UVC (USB Video Class) driver support
- **USB Fingerprint Scanner**: Optical or capacitive sensor
  - Recommended models: Digital Persona U.are.U 4500, ZKTeco SLK20R
  - Requirements: USB 2.0 compatible, libusb driver support

**Display and Input:**
- **Touchscreen Display**: 7-inch minimum, 10-inch recommended
  - Resolution: 1024x600 minimum, 1920x1080 preferred
  - Touch Technology: Capacitive multi-touch preferred
  - Interface: HDMI with USB touch interface
- **Alternative**: Standard HDMI monitor with USB mouse/keyboard

**Connectivity:**
- **Network**: Ethernet port (built-in) or WiFi adapter
- **USB Ports**: Minimum 2 available ports for camera and fingerprint scanner
- **Storage**: Additional USB storage for backups (optional)

### 3.2 Recommended Hardware Configuration

**Enhanced Performance Setup:**
- **Raspberry Pi 4 Model B 8GB**: Maximum RAM for optimal performance
- **High-Speed MicroSD**: SanDisk Extreme Pro 64GB A2 V30
- **USB 3.0 Hub**: Powered hub for multiple USB devices
- **Professional Camera**: Higher resolution camera with manual focus control
- **Enterprise Fingerprint Scanner**: FBI-certified scanner for maximum accuracy

**Kiosk Enclosure:**
- **Protective Case**: Secure mounting case with ventilation
- **Cable Management**: Organized cable routing and protection
- **Mounting Hardware**: VESA mount compatibility for wall/desk mounting
- **Security Features**: Lockable enclosure with tamper detection

**Environmental Considerations:**
- **Operating Temperature**: 0°C to 40°C (32°F to 104°F)
- **Humidity**: 20% to 80% relative humidity, non-condensing
- **Ventilation**: Adequate airflow for continuous operation
- **Power Protection**: UPS or surge protector recommended

### 3.3 Hardware Compatibility Matrix

**Tested Camera Models:**
| Model | Resolution | Autofocus | Compatibility | Notes |
|-------|------------|-----------|---------------|-------|
| Logitech C920 | 1080p | Yes | Excellent | Recommended |
| Logitech C922 | 1080p | Yes | Excellent | Streaming optimized |
| Microsoft LifeCam HD-3000 | 720p | No | Good | Budget option |
| Raspberry Pi Camera Module V2 | 1080p | No | Good | Requires ribbon cable |

**Tested Fingerprint Scanners:**
| Model | Technology | Interface | Compatibility | Notes |
|-------|------------|-----------|---------------|-------|
| Digital Persona U.are.U 4500 | Optical | USB 2.0 | Excellent | FBI certified |
| ZKTeco SLK20R | Capacitive | USB 2.0 | Good | Cost-effective |
| Futronic FS80 | Optical | USB 2.0 | Good | Compact design |

**Display Compatibility:**
| Type | Size | Resolution | Touch | Compatibility |
|------|------|------------|-------|---------------|
| Official RPi Touchscreen | 7" | 800x480 | Capacitive | Excellent |
| Waveshare 10.1" HDMI LCD | 10.1" | 1024x600 | Capacitive | Excellent |
| Generic HDMI Monitor | Various | Various | External | Good |

### 3.4 Installation and Setup

**Physical Installation:**
1. **Secure Mounting**: Install Raspberry Pi in protective case
2. **Camera Positioning**: Mount camera at eye level for optimal face capture
3. **Fingerprint Scanner**: Position scanner at comfortable height and angle
4. **Display Setup**: Install touchscreen at appropriate viewing angle
5. **Cable Management**: Organize and secure all cables
6. **Power Connection**: Connect power supply with surge protection

**Hardware Configuration:**
1. **Enable Camera**: Use `raspi-config` to enable camera interface
2. **USB Permissions**: Configure udev rules for biometric devices
3. **Display Calibration**: Calibrate touchscreen for accurate input
4. **Network Setup**: Configure Ethernet or WiFi connectivity
5. **Audio Disable**: Disable audio if not required to free resources

## 4. Software Components

### 4.1 Operating System

**Raspberry Pi OS (Debian-based):**
- **Version**: Bullseye or newer (64-bit recommended)
- **Kernel**: Linux 5.15+ with hardware acceleration support
- **Desktop Environment**: Minimal installation for kiosk mode
- **Package Management**: APT package manager for system updates

**System Services:**
- **Systemd**: Service management and process supervision
- **NetworkManager**: Network configuration and management
- **UFW**: Uncomplicated Firewall for network security
- **Fail2ban**: Intrusion detection and prevention system

### 4.2 Backend Framework

**Flask Web Framework:**
- **Version**: Flask 2.3+ with Werkzeug WSGI server
- **Extensions**: Flask-SQLAlchemy, Flask-CORS for API support
- **Database**: SQLAlchemy ORM with SQLite backend
- **Security**: Secure session management and CSRF protection

**Python Dependencies:**
```python
flask==2.3.3
flask-cors==4.0.0
flask-sqlalchemy==3.0.5
opencv-python-headless==4.8.1.78
mediapipe==0.10.7
numpy==1.24.3
pillow==10.0.1
requests==2.31.0
python-dateutil==2.8.2
```

### 4.3 Frontend Technologies

**Web Technologies:**
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Responsive design with Flexbox and Grid layouts
- **JavaScript ES6**: Modern JavaScript with async/await patterns
- **Progressive Web App**: Offline capability and app-like experience

**UI Framework:**
- **Custom CSS**: Tailored design for kiosk environment
- **Responsive Design**: Mobile-first approach with touch optimization
- **Icon Library**: SVG icons for crisp display at any resolution
- **Animation**: Smooth transitions and user feedback

### 4.4 Biometric Processing

**Computer Vision:**
- **OpenCV**: Image processing and computer vision algorithms
- **MediaPipe**: Google's framework for face detection and landmarks
- **NumPy**: Numerical computing for biometric data processing
- **Pillow**: Python Imaging Library for image manipulation

**Face Recognition Pipeline:**
1. **Face Detection**: MediaPipe Face Detection for robust face localization
2. **Face Landmarks**: 468 facial landmarks for precise feature extraction
3. **Face Encoding**: 128-dimensional feature vectors for comparison
4. **Similarity Matching**: Cosine similarity for face verification

**Fingerprint Processing:**
1. **Image Capture**: High-resolution fingerprint image acquisition
2. **Preprocessing**: Image enhancement and noise reduction
3. **Minutiae Extraction**: Ridge ending and bifurcation point detection
4. **Template Creation**: Compact biometric template generation
5. **Matching Algorithm**: Minutiae-based comparison for verification

### 4.5 Database System

**SQLite Database:**
- **Version**: SQLite 3.40+ with JSON support
- **Features**: ACID compliance, concurrent read access
- **Performance**: Optimized for embedded systems
- **Backup**: File-based backup with atomic operations

**Database Schema Management:**
- **SQLAlchemy ORM**: Object-relational mapping for Python
- **Migration Support**: Schema versioning and upgrade procedures
- **Data Validation**: Model-level validation and constraints
- **Indexing**: Optimized indexes for query performance

### 4.6 Security Components

**Network Security:**
- **UFW Firewall**: Stateful packet filtering firewall
- **Fail2ban**: Log monitoring and intrusion prevention
- **SSH Hardening**: Secure remote access configuration
- **SSL/TLS**: HTTPS encryption for web communications

**Application Security:**
- **Input Validation**: Comprehensive data validation and sanitization
- **Session Security**: Secure session management with timeout
- **CSRF Protection**: Cross-site request forgery prevention
- **XSS Prevention**: Cross-site scripting attack mitigation

**Data Protection:**
- **Local Storage**: All data stored locally for privacy protection
- **Encryption**: Biometric data encryption at rest
- **Access Control**: File-level permissions and user restrictions
- **Audit Logging**: Comprehensive security event logging

### 4.7 System Monitoring

**Performance Monitoring:**
- **System Metrics**: CPU, memory, disk, and network monitoring
- **Application Metrics**: Request processing and response times
- **Biometric Performance**: Recognition accuracy and processing speed
- **Error Tracking**: Comprehensive error logging and alerting

**Health Monitoring:**
- **Service Status**: Automatic service health checks
- **Hardware Status**: Temperature, voltage, and component monitoring
- **Network Connectivity**: Connection status and quality monitoring
- **Storage Monitoring**: Disk usage and health monitoring

### 4.8 Backup and Recovery

**Backup System:**
- **Automated Backups**: Scheduled data backup procedures
- **Incremental Backups**: Efficient storage of changes only
- **Compression**: Backup file compression for storage efficiency
- **Verification**: Backup integrity checking and validation

**Recovery Procedures:**
- **System Recovery**: Complete system restoration from backup
- **Data Recovery**: Selective data restoration procedures
- **Configuration Recovery**: System configuration restoration
- **Emergency Procedures**: Disaster recovery protocols

### 4.9 Development Tools

**Development Environment:**
- **Python 3.11**: Modern Python with type hints and async support
- **Git**: Version control system for source code management
- **Virtual Environment**: Isolated Python environment for dependencies
- **Code Quality**: Linting and formatting tools for code consistency

**Testing Framework:**
- **unittest**: Python's built-in testing framework
- **Integration Tests**: End-to-end testing of system workflows
- **Performance Tests**: Load testing and performance validation
- **Security Tests**: Vulnerability scanning and security validation

**Deployment Tools:**
- **Automated Scripts**: Deployment automation for production systems
- **Configuration Management**: Centralized configuration management
- **Service Management**: Systemd service configuration and management
- **Monitoring Integration**: Integration with system monitoring tools


## 5. Installation Guide

### 5.1 Pre-Installation Preparation

**Hardware Setup:**
1. **Assemble Hardware**: Connect Raspberry Pi, camera, fingerprint scanner, and display
2. **Install Raspberry Pi OS**: Flash latest Raspberry Pi OS to microSD card
3. **Initial Boot**: Complete initial setup wizard and enable SSH if needed
4. **Update System**: Run `sudo apt update && sudo apt upgrade -y`
5. **Enable Interfaces**: Enable camera and other required interfaces via `raspi-config`

**Network Configuration:**
1. **Connect to Network**: Configure Ethernet or WiFi connectivity
2. **Set Static IP** (optional): Configure static IP for consistent access
3. **Test Connectivity**: Verify internet access for package downloads
4. **Configure DNS**: Set reliable DNS servers (8.8.8.8, 8.8.4.4)

### 5.2 Automated Installation

**Quick Installation Method:**
```bash
# Download and run the automated installer
curl -sSL https://raw.githubusercontent.com/your-repo/sva-terminal/main/install.sh | bash

# Or manual download and execution
wget https://raw.githubusercontent.com/your-repo/sva-terminal/main/install.sh
chmod +x install.sh
sudo ./install.sh
```

**What the Installer Does:**
- Downloads and installs all required system packages
- Creates the SVA user and sets up permissions
- Installs Python dependencies in a virtual environment
- Configures system services and security settings
- Sets up the database and initial configuration
- Configures kiosk mode and auto-startup

### 5.3 Manual Installation

**Step 1: System Dependencies**
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y python3-pip python3-venv git curl wget vim
sudo apt install -y nginx supervisor sqlite3
sudo apt install -y v4l-utils fswebcam libusb-1.0-0-dev

# Install build dependencies for Python packages
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libgtk2.0-dev libcanberra-gtk-module
```

**Step 2: Create SVA User**
```bash
# Create dedicated user for SVA Terminal
sudo useradd -m -s /bin/bash sva
sudo usermod -a -G video,audio,dialout,plugdev sva

# Create application directory
sudo mkdir -p /opt/sva_terminal
sudo chown sva:sva /opt/sva_terminal
```

**Step 3: Download and Install Application**
```bash
# Switch to SVA user
sudo su - sva

# Clone the repository (or copy files)
cd /opt/sva_terminal
git clone https://github.com/your-repo/sva-terminal.git .

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4: Database Setup**
```bash
# Initialize the database
cd /opt/sva_terminal
source venv/bin/activate
python -c "
from src.main import create_app
app = create_app()
with app.app_context():
    from src.models.user import db
    db.create_all()
    print('Database initialized successfully')
"
```

**Step 5: System Services**
```bash
# Exit SVA user back to sudo user
exit

# Copy service files
sudo cp /opt/sva_terminal/scripts/sva-terminal.service /etc/systemd/system/
sudo cp /opt/sva_terminal/scripts/nginx.conf /etc/nginx/sites-available/sva-terminal

# Enable services
sudo systemctl daemon-reload
sudo systemctl enable sva-terminal
sudo systemctl enable nginx

# Configure nginx
sudo ln -sf /etc/nginx/sites-available/sva-terminal /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
```

### 5.4 Security Configuration

**Run Security Hardening Script:**
```bash
sudo /opt/sva_terminal/scripts/security_hardening.sh
```

**Manual Security Configuration:**
```bash
# Configure firewall
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow from 127.0.0.1 to any port 5000
sudo ufw --force enable

# Configure fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Set up automatic updates
sudo systemctl enable unattended-upgrades
```

### 5.5 Kiosk Mode Setup

**Run Kiosk Configuration Script:**
```bash
sudo /opt/sva_terminal/scripts/setup_kiosk.sh
```

**Manual Kiosk Configuration:**
```bash
# Install kiosk packages
sudo apt install -y chromium-browser unclutter xdotool xinit
sudo apt install -y x11-xserver-utils lightdm openbox

# Configure auto-login
sudo tee /etc/lightdm/lightdm.conf << EOF
[Seat:*]
autologin-user=sva
autologin-user-timeout=0
user-session=openbox
EOF

# Configure openbox autostart
sudo mkdir -p /home/sva/.config/openbox
sudo tee /home/sva/.config/openbox/autostart << 'EOF'
#!/bin/bash
xset s off
xset -dpms
xset s noblank
unclutter -idle 1 &
sleep 10
chromium-browser --kiosk --no-sandbox --disable-infobars http://localhost:5000
EOF

sudo chmod +x /home/sva/.config/openbox/autostart
sudo chown -R sva:sva /home/sva/.config
```

### 5.6 Hardware Configuration

**Camera Configuration:**
```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Test camera
v4l2-ctl --list-devices
fswebcam test.jpg

# Set camera permissions
sudo usermod -a -G video sva
```

**Fingerprint Scanner Configuration:**
```bash
# Create udev rules for fingerprint scanner
sudo tee /etc/udev/rules.d/99-fingerprint.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", GROUP="plugdev", MODE="0664"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Test fingerprint scanner
lsusb | grep -i fingerprint
```

### 5.7 Final Configuration and Testing

**Start Services:**
```bash
# Start all services
sudo systemctl start sva-terminal
sudo systemctl start nginx

# Check service status
sudo systemctl status sva-terminal
sudo systemctl status nginx

# Test web interface
curl http://localhost:5000
```

**Verification:**
```bash
# Run system verification
sudo /opt/sva_terminal/scripts/verify_installation.sh

# Check logs
sudo journalctl -u sva-terminal -f
tail -f /var/log/sva_terminal/app.log
```

**Reboot for Kiosk Mode:**
```bash
# Reboot to activate kiosk mode
sudo reboot
```

## 6. Configuration

### 6.1 Application Configuration

**Main Configuration File: `/opt/sva_terminal/config/production.py`**

```python
class ProductionConfig:
    # Flask settings
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = False
    TESTING = False
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/sva_terminal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    SESSION_COOKIE_SECURE = False  # Set to True for HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Biometric settings
    FACE_RECOGNITION_THRESHOLD = 0.7
    FINGERPRINT_RECOGNITION_THRESHOLD = 0.7
    
    # Hardware settings
    CAMERA_DEVICE = 0
    FINGERPRINT_DEVICE = '/dev/ttyUSB0'
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/sva_terminal/app.log'
```

### 6.2 Biometric Configuration

**Face Recognition Settings:**
```python
# Face recognition parameters
FACE_DETECTION_CONFIDENCE = 0.5
FACE_RECOGNITION_THRESHOLD = 0.7
FACE_ENCODING_MODEL = 'large'  # 'small' or 'large'
MAX_FACE_DISTANCE = 0.6

# Face capture settings
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
CAPTURE_FPS = 30
FACE_QUALITY_THRESHOLD = 0.8
```

**Fingerprint Settings:**
```python
# Fingerprint scanner parameters
FINGERPRINT_TIMEOUT = 10  # seconds
FINGERPRINT_QUALITY_THRESHOLD = 60
MINUTIAE_THRESHOLD = 12
FINGERPRINT_MATCH_THRESHOLD = 0.7

# Scanner device settings
SCANNER_VENDOR_ID = 0x1234
SCANNER_PRODUCT_ID = 0x5678
SCANNER_INTERFACE = 0
```

### 6.3 System Configuration

**Service Configuration: `/etc/systemd/system/sva-terminal.service`**
```ini
[Unit]
Description=SVA Terminal Application
After=network.target

[Service]
Type=simple
User=sva
Group=sva
WorkingDirectory=/opt/sva_terminal
Environment=PATH=/opt/sva_terminal/venv/bin
Environment=FLASK_APP=src/main.py
Environment=FLASK_ENV=production
ExecStart=/opt/sva_terminal/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration: `/etc/nginx/sites-available/sva-terminal`**
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/sva_terminal/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 6.4 Security Configuration

**Firewall Rules:**
```bash
# UFW firewall configuration
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (adjust port as needed)
sudo ufw allow 22/tcp

# Allow local web access
sudo ufw allow from 127.0.0.1 to any port 5000
sudo ufw allow from 192.168.1.0/24 to any port 80

# Enable firewall
sudo ufw --force enable
```

**Fail2ban Configuration: `/etc/fail2ban/jail.local`**
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s

[sva-terminal]
enabled = true
port = 5000
logpath = /var/log/sva_terminal/error.log
maxretry = 5
bantime = 1800
```

### 6.5 Kiosk Mode Configuration

**Openbox Autostart: `/home/sva/.config/openbox/autostart`**
```bash
#!/bin/bash

# Disable screen blanking
xset s off
xset -dpms
xset s noblank

# Hide cursor when inactive
unclutter -idle 1 &

# Wait for network and services
sleep 10

# Start Chromium in kiosk mode
chromium-browser \
    --kiosk \
    --no-sandbox \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    --start-fullscreen \
    --touch-events=enabled \
    http://localhost:5000
```

**Boot Configuration: `/boot/config.txt`**
```ini
# SVA Terminal configuration
disable_splash=1
gpu_mem=128
start_x=1
dtparam=audio=off

# HDMI settings
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
```

### 6.6 Logging Configuration

**Application Logging:**
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        RotatingFileHandler(
            '/var/log/sva_terminal/app.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)
```

**System Log Rotation: `/etc/logrotate.d/sva_terminal`**
```
/var/log/sva_terminal/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 sva sva
}
```

### 6.7 Performance Tuning

**System Optimization:**
```bash
# GPU memory split
echo "gpu_mem=128" | sudo tee -a /boot/config.txt

# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable cups
sudo systemctl disable avahi-daemon

# Optimize swappiness
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
```

**Application Optimization:**
```python
# Flask configuration for performance
SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
PERMANENT_SESSION_LIFETIME = 1800     # 30 minutes
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB

# Database optimization
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}
```

