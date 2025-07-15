#!/bin/bash

# AWS EC2 Ubuntu Automated Setup Script for Whites Management
# Run this script on a fresh Ubuntu 22.04 EC2 instance

set -e  # Exit on any error

echo "=== Whites Management EC2 Setup Script ==="
echo "Setting up Whites Management on Ubuntu EC2 instance"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Run as ubuntu user."
   exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
print_status "Installing required packages..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nginx \
    git \
    curl \
    unzip \
    build-essential \
    python3.11-dev \
    htop \
    ufw \
    certbot \
    python3-certbot-nginx

# Create application user
print_status "Creating application user 'whites'..."
if ! id "whites" &>/dev/null; then
    sudo useradd -m -s /bin/bash whites
    sudo usermod -aG sudo whites
    print_status "User 'whites' created successfully"
else
    print_warning "User 'whites' already exists"
fi

# Create application directory
print_status "Setting up application directory..."
sudo mkdir -p /opt/whites-management
sudo chown whites:whites /opt/whites-management

# Setup Python virtual environment
print_status "Creating Python virtual environment..."
cd /opt/whites-management
sudo -u whites python3.11 -m venv venv
sudo -u whites ./venv/bin/pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python packages..."
sudo -u whites ./venv/bin/pip install streamlit pandas plotly xlsxwriter

# Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/whites-management.service > /dev/null <<EOF
[Unit]
Description=Whites Management Streamlit Application
After=network.target

[Service]
Type=simple
User=whites
Group=whites
WorkingDirectory=/opt/whites-management
Environment=PATH=/opt/whites-management/venv/bin
ExecStart=/opt/whites-management/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Get domain/IP for Nginx configuration
echo ""
echo "Enter your domain name (e.g., yourdomain.com) or EC2 public IP:"
read -r DOMAIN

if [[ -z "$DOMAIN" ]]; then
    print_error "Domain/IP is required"
    exit 1
fi

# Create Nginx configuration
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/whites-management > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
if sudo nginx -t; then
    print_status "Nginx configuration is valid"
    sudo systemctl reload nginx
else
    print_error "Nginx configuration failed"
    exit 1
fi

# Create backup script
print_status "Setting up backup system..."
sudo tee /opt/whites-management/backup.sh > /dev/null <<'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/whites-management/backups"
mkdir -p $BACKUP_DIR

# Backup data directory if it exists
if [ -d "/opt/whites-management/data" ]; then
    tar -czf $BACKUP_DIR/whites_data_$DATE.tar.gz /opt/whites-management/data/
    echo "Backup completed: whites_data_$DATE.tar.gz"
else
    echo "No data directory found, skipping backup"
fi

# Keep only last 30 days of backups
find $BACKUP_DIR -name "whites_data_*.tar.gz" -mtime +30 -delete
EOF

sudo chmod +x /opt/whites-management/backup.sh
sudo chown whites:whites /opt/whites-management/backup.sh

# Setup cron job for backups
print_status "Setting up daily backups..."
(sudo -u whites crontab -l 2>/dev/null; echo "0 2 * * * /opt/whites-management/backup.sh >> /opt/whites-management/backup.log 2>&1") | sudo -u whites crontab -

# Configure UFW firewall
print_status "Configuring firewall..."
sudo ufw --force reset
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Enable systemd services
print_status "Enabling services..."
sudo systemctl daemon-reload
sudo systemctl enable whites-management
sudo systemctl enable nginx

# Create upload helper script
print_status "Creating upload helper script..."
tee /home/ubuntu/upload_whites_files.sh > /dev/null <<'EOF'
#!/bin/bash
# Helper script to upload Whites Management files
# Usage: ./upload_whites_files.sh /path/to/whites-management-files

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-whites-management-files>"
    echo "Example: $0 ./whites-management"
    exit 1
fi

SOURCE_DIR="$1"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Directory $SOURCE_DIR does not exist"
    exit 1
fi

echo "Copying files to /opt/whites-management..."
sudo cp -r "$SOURCE_DIR"/* /opt/whites-management/
sudo chown -R whites:whites /opt/whites-management

echo "Starting Whites Management service..."
sudo systemctl start whites-management

echo "Checking service status..."
sudo systemctl status whites-management --no-pager

echo ""
echo "Upload complete! Your application should be accessible at:"
echo "http://$(curl -s ifconfig.me)"
echo "or http://$DOMAIN (if DNS is configured)"
EOF

chmod +x /home/ubuntu/upload_whites_files.sh

# Create SSL setup script
print_status "Creating SSL setup script..."
tee /home/ubuntu/setup_ssl.sh > /dev/null <<EOF
#!/bin/bash
# SSL Certificate Setup Script
# Run this after your domain DNS is pointing to this server

echo "Setting up SSL certificate for $DOMAIN..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

if [ \$? -eq 0 ]; then
    echo "SSL certificate installed successfully!"
    echo "Your site is now available at https://$DOMAIN"
else
    echo "SSL setup failed. Please check your domain DNS configuration."
fi
EOF

chmod +x /home/ubuntu/setup_ssl.sh

# Final instructions
echo ""
print_status "=== EC2 Setup Complete! ==="
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo "1. Upload your Whites Management files:"
echo "   ./upload_whites_files.sh /path/to/your/whites-management-files"
echo ""
echo "2. Configure your domain DNS (if using a domain):"
echo "   Point A record for $DOMAIN to this server's IP: $(curl -s ifconfig.me)"
echo ""
echo "3. Setup SSL certificate (after DNS is configured):"
echo "   ./setup_ssl.sh"
echo ""
echo -e "${GREEN}Useful Commands:${NC}"
echo "  Check service status: sudo systemctl status whites-management"
echo "  View logs: sudo journalctl -u whites-management -f"
echo "  Restart service: sudo systemctl restart whites-management"
echo "  Check backups: ls -la /opt/whites-management/backups/"
echo ""
echo -e "${GREEN}Your server is ready!${NC}"
echo "EC2 Public IP: $(curl -s ifconfig.me)"
echo "Access your application at: http://$(curl -s ifconfig.me)"
echo ""
print_warning "Remember to upload your application files before the service will work!"