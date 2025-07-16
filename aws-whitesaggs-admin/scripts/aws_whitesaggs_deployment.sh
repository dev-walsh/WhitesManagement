#!/bin/bash

# AWS EC2 Deployment Script for whitesaggs.com/admin
# This script sets up Whites Management on AWS EC2 with subdirectory routing

set -e

DOMAIN="whitesaggs.com"
SUBDIRECTORY="admin"
FULL_PATH="${DOMAIN}/${SUBDIRECTORY}"
APP_DIR="/opt/whites-management"
SERVICE_NAME="whites-management"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_header "AWS EC2 Setup for ${FULL_PATH}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root"
    exit 1
fi

# Get current server IP
SERVER_IP=$(curl -s ifconfig.me)
print_status "Server IP: $SERVER_IP"

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
    htop \
    awscli \
    unzip

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

# Create Streamlit configuration for subdirectory
print_status "Configuring Streamlit for subdirectory routing..."
mkdir -p $APP_DIR/.streamlit
tee $APP_DIR/.streamlit/config.toml > /dev/null <<EOF
[server]
headless = true
address = "0.0.0.0"
port = 5000
baseUrlPath = "/${SUBDIRECTORY}"

[browser]
gatherUsageStats = false

[theme]
base = "light"
EOF

# Create systemd service
print_status "Creating systemd service..."
tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=Whites Management Application for ${FULL_PATH}
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true --server.baseUrlPath /${SUBDIRECTORY}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration for subdirectory
print_status "Configuring Nginx for ${FULL_PATH}..."
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
    
    # Root location - you can serve other content here
    location / {
        return 200 "Welcome to whitesaggs.com - Admin panel available at /admin";
        add_header Content-Type text/plain;
    }
    
    # Admin panel location
    location /${SUBDIRECTORY} {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Script-Name /${SUBDIRECTORY};
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
    
    # Static files for admin panel
    location /${SUBDIRECTORY}/static {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
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

# Configure AWS security group helper
print_status "Creating AWS security group configuration helper..."
tee /root/aws_security_group_setup.sh > /dev/null <<'AWS_EOF'
#!/bin/bash

echo "=== AWS Security Group Configuration ==="
echo ""
echo "Configure your EC2 security group with these rules:"
echo ""
echo "Inbound Rules:"
echo "1. SSH (22) - Source: Your IP only"
echo "2. HTTP (80) - Source: 0.0.0.0/0"
echo "3. HTTPS (443) - Source: 0.0.0.0/0"
echo ""
echo "AWS CLI Commands (if you have AWS CLI configured):"
echo ""
echo "# Get your security group ID"
echo "aws ec2 describe-security-groups --group-names default"
echo ""
echo "# Add HTTP rule"
echo "aws ec2 authorize-security-group-ingress --group-id sg-xxxxxxxx --protocol tcp --port 80 --cidr 0.0.0.0/0"
echo ""
echo "# Add HTTPS rule"
echo "aws ec2 authorize-security-group-ingress --group-id sg-xxxxxxxx --protocol tcp --port 443 --cidr 0.0.0.0/0"
echo ""
echo "Or configure through AWS Console:"
echo "1. Go to EC2 Dashboard"
echo "2. Security Groups"
echo "3. Select your instance's security group"
echo "4. Edit inbound rules"
echo "5. Add rules as shown above"
AWS_EOF

chmod +x /root/aws_security_group_setup.sh

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

# Create SSL setup script for subdirectory
print_status "Creating SSL setup script..."
tee /root/setup_ssl_whitesaggs_admin.sh > /dev/null <<'SSL_EOF'
#!/bin/bash

DOMAIN="whitesaggs.com"
SUBDIRECTORY="admin"
EMAIL="admin@whitesaggs.com"

echo "Setting up SSL certificate for $DOMAIN with admin panel at /$SUBDIRECTORY..."

# Stop nginx temporarily
systemctl stop nginx

# Get certificate
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    -d "www.$DOMAIN"

# Update nginx configuration for SSL with subdirectory
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
    
    # Root location - customize as needed
    location / {
        return 200 "Welcome to whitesaggs.com - Admin panel available at /admin";
        add_header Content-Type text/plain;
    }
    
    # Admin panel location
    location /admin {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Script-Name /admin;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
    
    # Static files for admin panel
    location /admin/static {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check
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
echo "Your admin panel is now available at: https://whitesaggs.com/admin"
SSL_EOF

chmod +x /root/setup_ssl_whitesaggs_admin.sh

# Create backup script
print_status "Creating backup system..."
tee $APP_DIR/backup_whitesaggs_admin.sh > /dev/null <<'BACKUP_EOF'
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/whites-management/backups"
mkdir -p $BACKUP_DIR

# Backup data directory
if [ -d "/opt/whites-management/data" ]; then
    tar -czf $BACKUP_DIR/whitesaggs_admin_data_$DATE.tar.gz /opt/whites-management/data/
    echo "Backup completed: whitesaggs_admin_data_$DATE.tar.gz"
else
    echo "No data directory found"
fi

# Keep only last 30 days of backups
find $BACKUP_DIR -name "whitesaggs_admin_data_*.tar.gz" -mtime +30 -delete

# Log backup
echo "$(date): Admin panel backup completed" >> /opt/whites-management/backup.log
BACKUP_EOF

chmod +x $APP_DIR/backup_whitesaggs_admin.sh
chown www-data:www-data $APP_DIR/backup_whitesaggs_admin.sh

# Setup daily backup cron
print_status "Setting up daily backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/whites-management/backup_whitesaggs_admin.sh") | crontab -

# Create upload helper
print_status "Creating upload helper script..."
tee /root/upload_whitesaggs_admin_files.sh > /dev/null <<'UPLOAD_EOF'
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
echo "Your admin panel is now available at: http://whitesaggs.com/admin"
echo "To setup SSL, run: /root/setup_ssl_whitesaggs_admin.sh"
UPLOAD_EOF

chmod +x /root/upload_whitesaggs_admin_files.sh

# Create status check script
tee /root/check_whitesaggs_admin_status.sh > /dev/null <<'STATUS_EOF'
#!/bin/bash

echo "=== Whites Management Admin Panel Status for whitesaggs.com/admin ==="
echo ""

# Get server info
echo "Server Information:"
echo "Public IP: $(curl -s ifconfig.me)"
echo "Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id 2>/dev/null || echo 'Not available')"
echo "Instance Type: $(curl -s http://169.254.169.254/latest/meta-data/instance-type 2>/dev/null || echo 'Not available')"
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
    echo "✓ Application is responding on port 5000"
else
    echo "✗ Application is not responding on port 5000"
fi

if curl -s http://localhost/admin > /dev/null; then
    echo "✓ Admin panel is accessible via proxy"
else
    echo "✗ Admin panel is not accessible via proxy"
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

# Check security group
echo "Security Group Check:"
echo "Make sure your AWS security group allows:"
echo "- Port 22 (SSH) from your IP"
echo "- Port 80 (HTTP) from 0.0.0.0/0"
echo "- Port 443 (HTTPS) from 0.0.0.0/0"
echo ""

# Check recent logs
echo "Recent Application Logs:"
journalctl -u whites-management --no-pager -n 5
STATUS_EOF

chmod +x /root/check_whitesaggs_admin_status.sh

# Create Route 53 helper
print_status "Creating Route 53 DNS helper..."
tee /root/aws_route53_setup.sh > /dev/null <<'ROUTE53_EOF'
#!/bin/bash

DOMAIN="whitesaggs.com"
SERVER_IP=$(curl -s ifconfig.me)

echo "=== AWS Route 53 DNS Configuration ==="
echo "Domain: $DOMAIN"
echo "Server IP: $SERVER_IP"
echo ""

echo "If you're using Route 53 for DNS, create these records:"
echo ""
echo "1. A Record for root domain:"
echo "   Name: $DOMAIN"
echo "   Type: A"
echo "   Value: $SERVER_IP"
echo "   TTL: 300"
echo ""
echo "2. A Record for www subdomain:"
echo "   Name: www.$DOMAIN"
echo "   Type: A"
echo "   Value: $SERVER_IP"
echo "   TTL: 300"
echo ""

echo "AWS CLI Commands (if you have AWS CLI configured):"
echo ""
echo "# Get hosted zone ID"
echo "aws route53 list-hosted-zones-by-name --dns-name $DOMAIN"
echo ""
echo "# Create A record for root domain"
echo "aws route53 change-resource-record-sets --hosted-zone-id Z123456789 --change-batch '{
    \"Changes\": [{
        \"Action\": \"UPSERT\",
        \"ResourceRecordSet\": {
            \"Name\": \"$DOMAIN\",
            \"Type\": \"A\",
            \"TTL\": 300,
            \"ResourceRecords\": [{\"Value\": \"$SERVER_IP\"}]
        }
    }]
}'"
echo ""
echo "# Create A record for www subdomain"
echo "aws route53 change-resource-record-sets --hosted-zone-id Z123456789 --change-batch '{
    \"Changes\": [{
        \"Action\": \"UPSERT\",
        \"ResourceRecordSet\": {
            \"Name\": \"www.$DOMAIN\",
            \"Type\": \"A\",
            \"TTL\": 300,
            \"ResourceRecords\": [{\"Value\": \"$SERVER_IP\"}]
        }
    }]
}'"
echo ""
echo "Replace Z123456789 with your actual hosted zone ID"
ROUTE53_EOF

chmod +x /root/aws_route53_setup.sh

print_header "Setup Complete for whitesaggs.com/admin"
echo ""
echo "AWS EC2 Configuration:"
echo "  Server IP: $SERVER_IP"
echo "  Instance: $(curl -s http://169.254.169.254/latest/meta-data/instance-id 2>/dev/null || echo 'Not available')"
echo ""
echo "Next steps:"
echo "1. Configure AWS Security Group:"
echo "   /root/aws_security_group_setup.sh"
echo ""
echo "2. Upload your Whites Management files:"
echo "   /root/upload_whitesaggs_admin_files.sh /path/to/your/whites-management-files"
echo ""
echo "3. Configure DNS (choose one):"
echo "   - Route 53: /root/aws_route53_setup.sh"
echo "   - Other registrar: Point A record to $SERVER_IP"
echo ""
echo "4. Setup SSL certificate (after DNS propagation):"
echo "   /root/setup_ssl_whitesaggs_admin.sh"
echo ""
echo "5. Check status anytime:"
echo "   /root/check_whitesaggs_admin_status.sh"
echo ""
echo "Your admin panel will be available at:"
echo "  HTTP: http://whitesaggs.com/admin"
echo "  HTTPS: https://whitesaggs.com/admin (after SSL setup)"
echo ""
echo "Backup location: /opt/whites-management/backups/"
echo ""
print_status "AWS deployment ready for whitesaggs.com/admin!"