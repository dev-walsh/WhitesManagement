#!/bin/bash

# Hostinger VPS Setup Script for Whites Management
# Run this script on your Hostinger VPS server after SSH connection

echo "=== Whites Management Hostinger Setup ==="
echo "This script will setup the Whites Management system on your Hostinger VPS"
echo ""

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing Python, Nginx, and other dependencies..."
sudo apt install python3 python3-pip python3-venv nginx git curl -y

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /var/www/whites-management
sudo chown -R $USER:$USER /var/www/whites-management

# Setup virtual environment
echo "Creating Python virtual environment..."
cd /var/www/whites-management
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install streamlit pandas plotly xlsxwriter

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/whites-management.service > /dev/null <<EOF
[Unit]
Description=Whites Management Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/whites-management
Environment=PATH=/var/www/whites-management/venv/bin
ExecStart=/var/www/whites-management/venv/bin/streamlit run app.py --server.port 8501 --server.address 127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
echo "Enter your domain name (e.g., yourdomain.com):"
read DOMAIN

sudo tee /etc/nginx/sites-available/whites-management > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable nginx site
sudo ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Create data directory with proper permissions
mkdir -p /var/www/whites-management/data
sudo chown -R www-data:www-data /var/www/whites-management

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Upload your Whites Management files to /var/www/whites-management/"
echo "2. Start the service: sudo systemctl start whites-management"
echo "3. Enable auto-start: sudo systemctl enable whites-management"
echo "4. Install SSL certificate: sudo certbot --nginx -d $DOMAIN"
echo ""
echo "Your application will be available at: http://$DOMAIN"
echo ""
echo "To check status: sudo systemctl status whites-management"
echo "To view logs: sudo journalctl -u whites-management -f"