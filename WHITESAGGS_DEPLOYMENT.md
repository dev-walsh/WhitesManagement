# Whites Management Deployment Guide for whitesaggs.com

## Overview
This guide provides step-by-step instructions for deploying the Whites Management system on your domain whitesaggs.com.

## Prerequisites
- VPS or dedicated server with Ubuntu 22.04 LTS
- Root access to the server
- Domain whitesaggs.com pointing to your server IP
- Minimum 1GB RAM, 2GB recommended
- 20GB disk space minimum

## Quick Deployment (Automated)

### Option 1: One-Command Setup
```bash
# On your Ubuntu server as root:
curl -sSL https://raw.githubusercontent.com/your-repo/whites-management/main/whitesaggs_deployment.sh | bash
```

### Option 2: Manual Setup
1. Upload the deployment script to your server
2. Make it executable: `chmod +x whitesaggs_deployment.sh`
3. Run as root: `./whitesaggs_deployment.sh`

## Step-by-Step Manual Process

### 1. Server Preparation
```bash
# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y python3.11 python3.11-venv python3-pip nginx git curl certbot python3-certbot-nginx ufw htop
```

### 2. Create Application Directory
```bash
# Create directory
mkdir -p /opt/whites-management
cd /opt/whites-management

# Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly xlsxwriter
```

### 3. Upload Application Files
```bash
# Upload your Whites Management files to /opt/whites-management/
# Ensure all files (app.py, pages/, utils/, .streamlit/) are present

# Set permissions
chown -R www-data:www-data /opt/whites-management
chmod -R 755 /opt/whites-management
```

### 4. Configure Systemd Service
```bash
# Create service file
tee /etc/systemd/system/whites-management.service > /dev/null <<EOF
[Unit]
Description=Whites Management Application for whitesaggs.com
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/whites-management
Environment=PATH=/opt/whites-management/venv/bin
ExecStart=/opt/whites-management/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable whites-management
systemctl start whites-management
```

### 5. Configure Nginx
```bash
# Create nginx configuration
tee /etc/nginx/sites-available/whites-management > /dev/null <<EOF
server {
    listen 80;
    server_name whitesaggs.com www.whitesaggs.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
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
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

### 6. Configure Firewall
```bash
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable
```

### 7. DNS Configuration
Configure your domain registrar's DNS settings:

```
Type: A
Name: @ (for whitesaggs.com)
Value: YOUR_SERVER_IP
TTL: 3600

Type: A
Name: www
Value: YOUR_SERVER_IP
TTL: 3600
```

### 8. SSL Certificate Setup
```bash
# After DNS propagation (wait 24-48 hours)
certbot --nginx -d whitesaggs.com -d www.whitesaggs.com --non-interactive --agree-tos --email admin@whitesaggs.com
```

## Automated Scripts (Created by Deployment Script)

### Upload Files
```bash
# Upload application files
/root/upload_whitesaggs_files.sh /path/to/your/whites-management-files
```

### Setup SSL
```bash
# Setup SSL certificate
/root/setup_ssl_whitesaggs.sh
```

### Check Status
```bash
# Check system status
/root/check_whitesaggs_status.sh
```

### Backup Data
```bash
# Manual backup
/opt/whites-management/backup_whitesaggs.sh
```

## Hosting Provider Recommendations

### Budget Option: Vultr
- **Cost**: $3.50-6/month
- **RAM**: 1GB-2GB
- **Setup**: Use whitesaggs_deployment.sh script
- **Features**: Good performance, multiple locations

### Recommended: DigitalOcean
- **Cost**: $5-12/month
- **RAM**: 1GB-2GB
- **Setup**: Use whitesaggs_deployment.sh script
- **Features**: Excellent documentation, reliable

### Professional: Linode
- **Cost**: $5-20/month
- **RAM**: 1GB-4GB
- **Setup**: Use whitesaggs_deployment.sh script
- **Features**: High performance, good support

### Enterprise: AWS EC2
- **Cost**: $8-50/month
- **RAM**: 1GB-8GB
- **Setup**: Use whitesaggs_deployment.sh script
- **Features**: Scalable, enterprise-grade

## Monitoring and Maintenance

### Health Checks
```bash
# Check application
curl http://whitesaggs.com/health

# Check SSL
openssl s_client -connect whitesaggs.com:443 -servername whitesaggs.com

# Check service status
systemctl status whites-management
```

### Log Monitoring
```bash
# Application logs
journalctl -u whites-management -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Resource Monitoring
```bash
# System resources
htop

# Disk space
df -h

# Memory usage
free -h
```

### Updates
```bash
# Update system
apt update && apt upgrade -y

# Update Python packages
cd /opt/whites-management
source venv/bin/activate
pip install --upgrade streamlit pandas plotly xlsxwriter

# Restart service
systemctl restart whites-management
```

## Backup Strategy

### Automatic Backups
- **Daily**: 2:00 AM server time
- **Location**: `/opt/whites-management/backups/`
- **Retention**: 30 days
- **Format**: `whitesaggs_data_YYYYMMDD_HHMMSS.tar.gz`

### Manual Backup
```bash
# Create backup
/opt/whites-management/backup_whitesaggs.sh

# Restore from backup
cd /opt/whites-management
tar -xzf backups/whitesaggs_data_20240715_020000.tar.gz
systemctl restart whites-management
```

## Security Features

### SSL/TLS
- **Certificate**: Let's Encrypt (free)
- **Protocols**: TLSv1.2, TLSv1.3
- **Auto-renewal**: Automated via cron

### Security Headers
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (HTTPS only)

### Firewall
- **SSH**: Port 22 (your IP only recommended)
- **HTTP**: Port 80 (redirects to HTTPS)
- **HTTPS**: Port 443
- **Application**: Port 5000 (internal only)

## Troubleshooting

### Common Issues

1. **Service won't start**
   ```bash
   journalctl -u whites-management --no-pager
   systemctl restart whites-management
   ```

2. **502 Bad Gateway**
   ```bash
   # Check if app is running
   curl http://localhost:5000/health
   systemctl status whites-management
   ```

3. **SSL certificate issues**
   ```bash
   # Check certificate
   certbot certificates
   # Renew if needed
   certbot renew
   ```

4. **Domain not resolving**
   ```bash
   # Check DNS
   dig whitesaggs.com
   nslookup whitesaggs.com
   ```

### Performance Optimization

1. **Increase server resources** if needed
2. **Use CDN** for static files (Cloudflare)
3. **Enable gzip compression** in Nginx
4. **Monitor resource usage** regularly

## Cost Estimates

### Monthly Costs
- **Server**: $3.50-20/month (depending on provider/size)
- **Domain**: $1-2/month (annual payment)
- **SSL**: Free (Let's Encrypt)
- **Backup**: Included in server storage

### Total Monthly Cost: $4.50-22/month

## Support and Maintenance

### Regular Tasks
- **Weekly**: Check logs and resource usage
- **Monthly**: Update system packages
- **Quarterly**: Review security settings and backups

### Emergency Contacts
- **Server Provider**: Contact your hosting provider
- **Domain Registrar**: Contact your domain registrar
- **SSL Issues**: Let's Encrypt community forum

This deployment guide ensures your Whites Management system runs professionally on whitesaggs.com with proper security, monitoring, and backup systems in place.