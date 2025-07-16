# Custom Domain Deployment Guide for Whites Management

## Overview
This guide explains how to deploy Whites Management on your own domain using various hosting providers that support Python applications.

## Hosting Provider Options

### 1. VPS Providers (Recommended)
Most flexible option with full control.

#### Popular VPS Providers:
- **DigitalOcean**: $5-20/month, excellent documentation
- **Linode**: $5-20/month, developer-friendly
- **Vultr**: $3.50-20/month, good performance
- **AWS EC2**: $8-50/month, enterprise-grade
- **Hetzner**: €3-20/month, EU-based
- **Google Cloud**: $5-30/month, reliable

#### Setup Process:
1. Launch Ubuntu 22.04 VPS
2. Point your domain A record to VPS IP
3. Use our automated setup script
4. Configure SSL with Let's Encrypt

### 2. Platform-as-a-Service (PaaS)
Easier management, less control.

#### PaaS Options:
- **Heroku**: $7-25/month, easy deployment
- **Railway**: $5-20/month, modern platform
- **Render**: $7-25/month, automatic deployments
- **PythonAnywhere**: $5-20/month, Python-focused

### 3. Shared Hosting with Python Support
Budget option if Python is supported.

#### Providers:
- **A2 Hosting**: Python support available
- **InMotion**: Business plans include Python
- **SiteGround**: Advanced plans support Python
- **Hostinger**: VPS plans recommended

## Quick Setup for VPS (Any Provider)

### Step 1: Launch VPS
```bash
# Minimum requirements:
- OS: Ubuntu 22.04 LTS
- RAM: 1GB (2GB recommended)
- Storage: 20GB
- CPU: 1 core (2 cores recommended)
```

### Step 2: Point Domain to VPS
In your domain registrar's DNS settings:
```
Type: A
Name: @ (or your subdomain)
Value: Your VPS IP address
TTL: 3600
```

For subdomain (e.g., fleet.yourdomain.com):
```
Type: A
Name: fleet
Value: Your VPS IP address
TTL: 3600
```

### Step 3: Connect and Setup
```bash
# Connect to your VPS
ssh root@your-vps-ip

# Download and run setup script
curl -o setup.sh https://raw.githubusercontent.com/your-repo/whites-management/main/vps_setup.sh
chmod +x setup.sh
./setup.sh
```

### Step 4: Upload Application
```bash
# Upload your application files
scp -r whites-management-files/ root@your-vps-ip:/opt/whites-management/
```

### Step 5: Configure Domain
```bash
# Update Nginx configuration with your domain
sudo nano /etc/nginx/sites-available/whites-management
# Change server_name to your domain
# Restart Nginx
sudo systemctl reload nginx
```

### Step 6: Setup SSL
```bash
# Install SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Universal VPS Setup Script

Create this script for any VPS provider:

```bash
#!/bin/bash
# Universal VPS setup script for Whites Management

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3.11 python3.11-venv python3-pip nginx git curl certbot python3-certbot-nginx

# Create application directory
mkdir -p /opt/whites-management
cd /opt/whites-management

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly xlsxwriter

# Create systemd service
tee /etc/systemd/system/whites-management.service > /dev/null <<EOF
[Unit]
Description=Whites Management Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/whites-management
Environment=PATH=/opt/whites-management/venv/bin
ExecStart=/opt/whites-management/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Get domain name
echo "Enter your domain name (e.g., yourdomain.com):"
read DOMAIN

# Create Nginx configuration
tee /etc/nginx/sites-available/whites-management > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# Enable services
systemctl enable whites-management nginx
systemctl start whites-management

echo "Setup complete! Upload your application files to /opt/whites-management/"
echo "Then run: sudo systemctl restart whites-management"
echo "Setup SSL with: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
```

## Platform-Specific Guides

### DigitalOcean Droplet
1. Create Ubuntu 22.04 droplet ($5/month minimum)
2. Add your SSH key during creation
3. Point domain A record to droplet IP
4. SSH in and run setup script
5. Upload application files
6. Configure SSL

### Heroku Deployment
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Create `requirements.txt`:
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
```

4. Deploy:
```bash
git init
heroku create your-app-name
git add .
git commit -m "Initial deployment"
git push heroku main
heroku domains:add yourdomain.com
```

5. Configure DNS CNAME to point to Heroku

### Railway Deployment
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. Add custom domain in Railway dashboard
5. Configure DNS as instructed

## DNS Configuration

### For Root Domain (yourdomain.com)
```
Type: A
Name: @
Value: Your server IP
TTL: 3600
```

### For Subdomain (fleet.yourdomain.com)
```
Type: A  
Name: fleet
Value: Your server IP
TTL: 3600
```

### For CDN/Load Balancer
```
Type: CNAME
Name: @
Value: your-provider.com
TTL: 3600
```

## SSL Certificate Setup

### Using Let's Encrypt (Free)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Using Cloudflare (Free)
1. Add your domain to Cloudflare
2. Update nameservers at registrar
3. Enable SSL/TLS in Cloudflare dashboard
4. Set SSL mode to "Full"

## Cost Comparison

### VPS Hosting
- **Budget**: $3-5/month (1GB RAM)
- **Recommended**: $10-20/month (2GB RAM)
- **High Performance**: $20-50/month (4GB+ RAM)

### PaaS Hosting
- **Heroku**: $7-25/month
- **Railway**: $5-20/month
- **Render**: $7-25/month

### Domain Costs
- **Domain registration**: $10-15/year
- **SSL Certificate**: Free (Let's Encrypt)
- **CDN**: $0-20/month (optional)

## Security Recommendations

### Basic Security
```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

### Advanced Security
- Use fail2ban for intrusion prevention
- Regular security updates
- Monitor logs for suspicious activity
- Use strong passwords and SSH keys
- Regular backups

## Monitoring and Maintenance

### Health Checks
```bash
# Check application status
sudo systemctl status whites-management

# View logs
sudo journalctl -u whites-management -f

# Check resource usage
htop
df -h
```

### Backup Strategy
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /backup/whites-data-$DATE.tar.gz /opt/whites-management/data/
find /backup -name "whites-data-*.tar.gz" -mtime +30 -delete
```

## Troubleshooting

### Common Issues
1. **Domain not resolving**: Check DNS propagation (24-48 hours)
2. **SSL not working**: Verify domain points to correct IP
3. **Application not starting**: Check logs with `journalctl`
4. **502 Bad Gateway**: Application not running on port 5000

### Getting Help
- Check provider documentation
- Use community forums
- Contact hosting provider support
- Review application logs

This guide provides multiple paths to deploy on your own domain. Choose the option that best fits your technical comfort level and budget.