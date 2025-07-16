#!/bin/bash

# Create domain deployment package
echo "Creating custom domain deployment package..."

# Create directory structure
mkdir -p domain-deployment
mkdir -p domain-deployment/scripts
mkdir -p domain-deployment/configs

# Copy core application files
cp -r pages/ domain-deployment/
cp -r utils/ domain-deployment/
cp -r .streamlit/ domain-deployment/
cp app.py domain-deployment/
cp pyproject.toml domain-deployment/

# Copy domain-specific files
cp CUSTOM_DOMAIN_DEPLOYMENT.md domain-deployment/
cp domain_setup_helper.sh domain-deployment/scripts/

# Create requirements file
cat > domain-deployment/requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
EOF

# Create universal VPS setup script
cat > domain-deployment/scripts/universal_vps_setup.sh << 'EOF'
#!/bin/bash
# Universal VPS Setup Script for Any Provider

set -e

echo "=== Universal VPS Setup for Whites Management ==="

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip nginx git curl certbot python3-certbot-nginx ufw

# Create application directory
sudo mkdir -p /opt/whites-management
cd /opt/whites-management

# Create virtual environment
sudo python3.11 -m venv venv
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install streamlit pandas plotly xlsxwriter

# Get domain
echo "Enter your domain name (e.g., yourdomain.com):"
read DOMAIN

# Create systemd service
sudo tee /etc/systemd/system/whites-management.service > /dev/null <<SERVICE_EOF
[Unit]
Description=Whites Management Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/whites-management
Environment=PATH=/opt/whites-management/venv/bin
ExecStart=/opt/whites-management/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Create nginx configuration
sudo tee /etc/nginx/sites-available/whites-management > /dev/null <<NGINX_EOF
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
NGINX_EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Set permissions
sudo chown -R www-data:www-data /opt/whites-management
sudo chmod -R 755 /opt/whites-management

# Enable services
sudo systemctl daemon-reload
sudo systemctl enable whites-management nginx

echo ""
echo "=== Setup Complete ==="
echo "1. Upload your application files to /opt/whites-management/"
echo "2. Start the service: sudo systemctl start whites-management"
echo "3. Setup SSL: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "Your application will be available at: http://$DOMAIN"
echo "After SSL setup: https://$DOMAIN"
EOF

chmod +x domain-deployment/scripts/universal_vps_setup.sh

# Create Heroku deployment files
cat > domain-deployment/Procfile << EOF
web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0
EOF

cat > domain-deployment/runtime.txt << EOF
python-3.11.0
EOF

# Create Railway deployment config
cat > domain-deployment/railway.json << EOF
{
    "build": {
        "builder": "NIXPACKS"
    },
    "deploy": {
        "startCommand": "streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0",
        "restartPolicyType": "ON_FAILURE",
        "restartPolicyMaxRetries": 10
    }
}
EOF

# Create provider-specific guides
cat > domain-deployment/PROVIDERS.md << EOF
# Hosting Provider Specific Guides

## VPS Providers (Recommended)

### DigitalOcean
- Cost: \$5-20/month
- Create Ubuntu 22.04 droplet
- Use universal_vps_setup.sh script
- Point domain A record to droplet IP

### Linode
- Cost: \$5-20/month  
- Create Ubuntu 22.04 Linode
- Use universal_vps_setup.sh script
- Configure domain DNS in Linode manager

### AWS EC2
- Cost: \$8-50/month
- Launch Ubuntu 22.04 instance
- Configure security groups (22, 80, 443)
- Use universal_vps_setup.sh script

### Vultr
- Cost: \$3.50-20/month
- Deploy Ubuntu 22.04 server
- Use universal_vps_setup.sh script
- Configure DNS in Vultr dashboard

## Platform as a Service

### Heroku
- Cost: \$7-25/month
- Uses included Procfile and runtime.txt
- Deploy via Git: git push heroku main
- Add custom domain in Heroku dashboard

### Railway
- Cost: \$5-20/month
- Uses included railway.json
- Connect GitHub repository
- Add custom domain in Railway dashboard

### Render
- Cost: \$7-25/month
- Build: pip install -r requirements.txt
- Start: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0
- Add custom domain in Render dashboard

## DNS Configuration

For all providers, configure DNS:
```
Type: A (for VPS)
Name: @ (root domain) or subdomain
Value: Your server IP
TTL: 3600

Type: CNAME (for PaaS)
Name: @ or subdomain
Value: provider-hostname.com
TTL: 3600
```

## SSL Certificates

### VPS: Let's Encrypt (Free)
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### PaaS: Automatic
Most platforms handle SSL automatically for custom domains.
EOF

# Create README for domain package
cat > domain-deployment/README.md << EOF
# Whites Management - Custom Domain Deployment

## Overview
This package contains everything needed to deploy Whites Management on your own domain using various hosting providers.

## Quick Start Options

### Option 1: VPS (Any Provider)
1. Launch Ubuntu 22.04 VPS
2. Upload this package to server
3. Run: \`./scripts/universal_vps_setup.sh\`
4. Upload application files
5. Configure SSL

### Option 2: Platform as a Service
1. Connect to your PaaS provider (Heroku, Railway, etc.)
2. Use included config files (Procfile, railway.json, etc.)
3. Deploy via Git or dashboard
4. Add custom domain in provider dashboard

### Option 3: Interactive Setup
1. Run: \`./scripts/domain_setup_helper.sh\`
2. Follow guided setup for your specific needs

## What's Included

### Core Application
- Complete Whites Management system
- Vehicle inventory management
- Machine/plant equipment tracking
- Tool hire and rental system
- Maintenance records
- Dashboard and statistics

### Deployment Tools
- Universal VPS setup script
- Platform-specific config files
- Domain setup helper
- SSL certificate automation
- Nginx configuration templates

### Documentation
- Provider-specific guides
- DNS configuration instructions
- SSL setup procedures
- Troubleshooting guides

## Supported Hosting Providers

### VPS Providers
- DigitalOcean (\$5-20/month)
- Linode (\$5-20/month)
- AWS EC2 (\$8-50/month)
- Vultr (\$3.50-20/month)
- Hetzner (€3-20/month)

### PaaS Providers
- Heroku (\$7-25/month)
- Railway (\$5-20/month)
- Render (\$7-25/month)

## Requirements
- Ubuntu 22.04 (for VPS)
- Python 3.11 support
- 1GB RAM minimum (2GB recommended)
- Custom domain name

## Support
See CUSTOM_DOMAIN_DEPLOYMENT.md for detailed instructions.
EOF

# Create archive
tar -czf whites-management-custom-domain.tar.gz domain-deployment/

# Cleanup
rm -rf domain-deployment/

echo "Custom domain deployment package created: whites-management-custom-domain.tar.gz"
echo "Package size: $(du -h whites-management-custom-domain.tar.gz | cut -f1)"