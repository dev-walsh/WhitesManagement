#!/bin/bash

# Whitesaggs.com Deployment Script for Whites Management
# This script sets up the Whites Management system on whitesaggs.com

set -e

DOMAIN="whitesaggs.com"
APP_DIR="/opt/whites-management"
SERVICE_NAME="whites-management"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Setting up Whites Management for $DOMAIN"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root"
    exit 1
fi

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install dependencies
print_status "Installing required packages..."
apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nginx \
    git \
    curl \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop

# Create application directory
print_status "Creating application directory..."
mkdir -p $APP_DIR
cd $APP_DIR

# Create virtual environment
print_status "Setting up Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install streamlit pandas plotly xlsxwriter

# Create systemd service
print_status "Creating systemd service..."
tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=Whites Management Application for $DOMAIN
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
print_status "Configuring Nginx for $DOMAIN..."
tee /etc/nginx/sites-available/${SERVICE_NAME} > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # File upload size limit
    client_max_body_size 50M;
    
    # Main application
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
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable nginx site
ln -sf /etc/nginx/sites-available/${SERVICE_NAME} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
if nginx -t; then
    print_status "Nginx configuration is valid"
else
    print_error "Nginx configuration failed"
    exit 1
fi

# Configure firewall
print_status "Configuring firewall..."
ufw --force reset
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

# Set permissions
print_status "Setting permissions..."
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

# Enable services
print_status "Enabling services..."
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl enable nginx
systemctl start nginx

# Create SSL setup script
print_status "Creating SSL setup script..."
tee /root/setup_ssl_whitesaggs.sh > /dev/null <<'SSL_EOF'
#!/bin/bash

DOMAIN="whitesaggs.com"
EMAIL="admin@whitesaggs.com"

echo "Setting up SSL certificate for $DOMAIN..."

# Stop nginx temporarily
systemctl stop nginx

# Get certificate
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    -d "www.$DOMAIN"

# Update nginx configuration for SSL
tee /etc/nginx/sites-available/whites-management > /dev/null <<'NGINX_SSL_EOF'
server {
    listen 80;
    server_name whitesaggs.com www.whitesaggs.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name whitesaggs.com www.whitesaggs.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/whitesaggs.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/whitesaggs.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
NGINX_SSL_EOF

# Start nginx
systemctl start nginx
systemctl reload nginx

# Setup auto-renewal
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "SSL certificate installed successfully!"
echo "Your site is now available at: https://whitesaggs.com"
SSL_EOF

chmod +x /root/setup_ssl_whitesaggs.sh

# Create backup script
print_status "Creating backup system..."
tee $APP_DIR/backup_whitesaggs.sh > /dev/null <<'BACKUP_EOF'
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/whites-management/backups"
mkdir -p $BACKUP_DIR

# Backup data directory
if [ -d "/opt/whites-management/data" ]; then
    tar -czf $BACKUP_DIR/whitesaggs_data_$DATE.tar.gz /opt/whites-management/data/
    echo "Backup completed: whitesaggs_data_$DATE.tar.gz"
else
    echo "No data directory found"
fi

# Keep only last 30 days of backups
find $BACKUP_DIR -name "whitesaggs_data_*.tar.gz" -mtime +30 -delete

# Log backup
echo "$(date): Backup completed" >> /opt/whites-management/backup.log
BACKUP_EOF

chmod +x $APP_DIR/backup_whitesaggs.sh
chown www-data:www-data $APP_DIR/backup_whitesaggs.sh

# Setup daily backup cron
print_status "Setting up daily backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/whites-management/backup_whitesaggs.sh") | crontab -

# Create upload helper
print_status "Creating upload helper script..."
tee /root/upload_whitesaggs_files.sh > /dev/null <<'UPLOAD_EOF'
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-whites-management-files>"
    echo "Example: $0 /home/user/whites-management-files"
    exit 1
fi

SOURCE_DIR="$1"
DEST_DIR="/opt/whites-management"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Directory $SOURCE_DIR does not exist"
    exit 1
fi

echo "Stopping service..."
systemctl stop whites-management

echo "Copying files..."
cp -r "$SOURCE_DIR"/* "$DEST_DIR/"

echo "Setting permissions..."
chown -R www-data:www-data "$DEST_DIR"
chmod -R 755 "$DEST_DIR"

echo "Starting service..."
systemctl start whites-management

echo "Checking service status..."
systemctl status whites-management --no-pager

echo ""
echo "Files uploaded successfully!"
echo "Your application is now available at: http://whitesaggs.com"
echo "To setup SSL, run: /root/setup_ssl_whitesaggs.sh"
UPLOAD_EOF

chmod +x /root/upload_whitesaggs_files.sh

# Create status check script
tee /root/check_whitesaggs_status.sh > /dev/null <<'STATUS_EOF'
#!/bin/bash

echo "=== Whites Management Status for whitesaggs.com ==="
echo ""

# Check service status
echo "Service Status:"
systemctl status whites-management --no-pager
echo ""

# Check nginx status
echo "Nginx Status:"
systemctl status nginx --no-pager
echo ""

# Check if app is responding
echo "Application Health Check:"
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✓ Application is responding"
else
    echo "✗ Application is not responding"
fi
echo ""

# Check SSL certificate
echo "SSL Certificate Status:"
if [ -f "/etc/letsencrypt/live/whitesaggs.com/fullchain.pem" ]; then
    echo "✓ SSL certificate exists"
    openssl x509 -in /etc/letsencrypt/live/whitesaggs.com/fullchain.pem -text -noout | grep "Not After"
else
    echo "✗ No SSL certificate found"
fi
echo ""

# Check disk space
echo "Disk Space:"
df -h /
echo ""

# Check recent logs
echo "Recent Application Logs:"
journalctl -u whites-management --no-pager -n 5
STATUS_EOF

chmod +x /root/check_whitesaggs_status.sh

print_status "=== Setup Complete for whitesaggs.com ==="
echo ""
echo "Next steps:"
echo "1. Upload your Whites Management files:"
echo "   /root/upload_whitesaggs_files.sh /path/to/your/whites-management-files"
echo ""
echo "2. Configure your DNS:"
echo "   Point whitesaggs.com A record to this server's IP: $(curl -s ifconfig.me)"
echo "   Point www.whitesaggs.com A record to this server's IP: $(curl -s ifconfig.me)"
echo ""
echo "3. Setup SSL certificate (after DNS propagation):"
echo "   /root/setup_ssl_whitesaggs.sh"
echo ""
echo "4. Check status anytime:"
echo "   /root/check_whitesaggs_status.sh"
echo ""
echo "Your application will be available at:"
echo "  HTTP: http://whitesaggs.com"
echo "  HTTPS: https://whitesaggs.com (after SSL setup)"
echo ""
echo "Server IP: $(curl -s ifconfig.me)"
echo "Backup location: /opt/whites-management/backups/"
echo ""
print_status "whitesaggs.com deployment ready!"