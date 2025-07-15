# AWS EC2 Ubuntu Deployment Guide for Whites Management

## Overview
This guide provides step-by-step instructions for deploying the Whites Management system on an Amazon EC2 Ubuntu server.

## Prerequisites
- AWS Account with EC2 access
- Basic knowledge of SSH and Linux commands
- Domain name (optional but recommended)

## Step 1: Launch EC2 Instance

### 1.1 EC2 Instance Configuration
```
Instance Type: t3.micro (Free tier eligible) or t3.small for better performance
Operating System: Ubuntu Server 22.04 LTS (64-bit x86)
Storage: 20 GB GP3 (minimum)
Security Group: Custom (see below)
```

### 1.2 Security Group Rules
Create a security group with these inbound rules:
```
SSH (22)     - Source: Your IP
HTTP (80)    - Source: 0.0.0.0/0 (Anywhere)
HTTPS (443)  - Source: 0.0.0.0/0 (Anywhere)
Custom (5000) - Source: 0.0.0.0/0 (For Streamlit during setup)
```

### 1.3 Key Pair
- Create or use existing EC2 Key Pair
- Download .pem file and keep it secure
- Set permissions: `chmod 400 your-key.pem`

## Step 2: Connect to EC2 Instance

### 2.1 SSH Connection
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 2.2 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

## Step 3: Install Dependencies

### 3.1 Install Python and Required Packages
```bash
# Install Python 3.11 and pip
sudo apt install python3.11 python3.11-venv python3-pip nginx git curl unzip -y

# Install additional system dependencies
sudo apt install build-essential python3.11-dev -y
```

### 3.2 Create Application User
```bash
sudo useradd -m -s /bin/bash whites
sudo usermod -aG sudo whites
```

## Step 4: Setup Application Directory

### 4.1 Create Directory Structure
```bash
sudo mkdir -p /opt/whites-management
sudo chown whites:whites /opt/whites-management
cd /opt/whites-management
```

### 4.2 Upload Application Files
Option A - Direct Upload via SCP:
```bash
# From your local machine
scp -i your-key.pem -r /path/to/whites-management/* ubuntu@your-ec2-ip:/tmp/
ssh -i your-key.pem ubuntu@your-ec2-ip
sudo mv /tmp/* /opt/whites-management/
sudo chown -R whites:whites /opt/whites-management
```

Option B - Git Clone (if you have a repository):
```bash
sudo -u whites git clone https://github.com/your-repo/whites-management.git /opt/whites-management
```

## Step 5: Python Environment Setup

### 5.1 Create Virtual Environment
```bash
cd /opt/whites-management
sudo -u whites python3.11 -m venv venv
sudo -u whites ./venv/bin/pip install --upgrade pip
```

### 5.2 Install Python Dependencies
```bash
sudo -u whites ./venv/bin/pip install streamlit pandas plotly xlsxwriter
```

## Step 6: Configure Systemd Service

### 6.1 Create Service File
```bash
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
```

### 6.2 Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable whites-management
sudo systemctl start whites-management
sudo systemctl status whites-management
```

## Step 7: Configure Nginx Reverse Proxy

### 7.1 Create Nginx Configuration
```bash
sudo tee /etc/nginx/sites-available/whites-management > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Replace with your domain or EC2 public IP
    
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
```

### 7.2 Enable Site and Test
```bash
sudo ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Step 8: Configure SSL Certificate (Optional but Recommended)

### 8.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2 Obtain SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Step 9: Configure Automatic Backups

### 9.1 Create Backup Script
```bash
sudo tee /opt/whites-management/backup.sh > /dev/null <<'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/whites-management/backups"
mkdir -p $BACKUP_DIR

# Backup data directory
tar -czf $BACKUP_DIR/whites_data_$DATE.tar.gz /opt/whites-management/data/

# Keep only last 30 days of backups
find $BACKUP_DIR -name "whites_data_*.tar.gz" -mtime +30 -delete

echo "Backup completed: whites_data_$DATE.tar.gz"
EOF

sudo chmod +x /opt/whites-management/backup.sh
sudo chown whites:whites /opt/whites-management/backup.sh
```

### 9.2 Setup Cron Job for Daily Backups
```bash
sudo -u whites crontab -e
# Add this line:
0 2 * * * /opt/whites-management/backup.sh >> /opt/whites-management/backup.log 2>&1
```

## Step 10: Security Hardening

### 10.1 Configure UFW Firewall
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

### 10.2 Disable Root Login and Password Authentication
```bash
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

## Step 11: Monitoring and Logs

### 11.1 Check Application Status
```bash
# Check service status
sudo systemctl status whites-management

# View application logs
sudo journalctl -u whites-management -f

# Check nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 11.2 Monitor Resources
```bash
# Install htop for resource monitoring
sudo apt install htop -y

# Check disk usage
df -h

# Check memory usage
free -h
```

## Cost Estimates

### EC2 Instance Costs (Monthly - USD)
- **t3.micro** (1 vCPU, 1GB RAM): ~$8.50/month (Free tier: 750 hours/month)
- **t3.small** (2 vCPU, 2GB RAM): ~$17/month
- **t3.medium** (2 vCPU, 4GB RAM): ~$34/month

### Additional Costs
- **EBS Storage** (20GB): ~$2/month
- **Data Transfer**: First 1GB free, then $0.09/GB
- **Elastic IP**: Free if associated with running instance

## Troubleshooting

### Common Issues

1. **Service Won't Start**
```bash
sudo journalctl -u whites-management --no-pager
sudo systemctl restart whites-management
```

2. **Permission Issues**
```bash
sudo chown -R whites:whites /opt/whites-management
sudo chmod -R 755 /opt/whites-management
```

3. **Port Access Issues**
```bash
sudo netstat -tlnp | grep :5000
sudo ufw status
```

4. **Nginx Configuration Issues**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Maintenance

### Regular Tasks
- **Weekly**: Check disk space and logs
- **Monthly**: Update system packages
- **Quarterly**: Review backups and security settings

### Update Application
```bash
sudo systemctl stop whites-management
cd /opt/whites-management
# Upload new files or pull from git
sudo systemctl start whites-management
```

## Domain Configuration

### Point Domain to EC2
1. Get your EC2 Elastic IP (recommended) or Public IP
2. In your domain registrar's DNS settings:
   - A Record: @ points to your EC2 IP
   - A Record: www points to your EC2 IP
3. Update Nginx configuration with your domain name
4. Obtain SSL certificate with Certbot

## Performance Optimization

### For High Traffic
- Use Application Load Balancer
- Consider RDS for database instead of CSV files
- Implement CloudFront CDN
- Use Auto Scaling Groups

### Memory Optimization
```bash
# Add swap file if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

This deployment guide provides a production-ready setup for the Whites Management system on AWS EC2 Ubuntu.