# Hostinger Deployment Guide for Whites Management

## Overview
This guide explains how to deploy the Whites Management system on Hostinger using your existing domain.

## Prerequisites
- Active Hostinger hosting account with Python support
- Your domain connected to Hostinger
- SSH access to your hosting account (Business plan or higher)

## Deployment Options

### Option 1: Hostinger VPS (Recommended)
Best for business use with full control and performance.

#### Steps:
1. **Upgrade to VPS Hosting**
   - Go to Hostinger control panel
   - Upgrade to VPS plan (starts around £3.99/month)
   - Choose Ubuntu 20.04 or 22.04 LTS

2. **Connect via SSH**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Python and Dependencies**
   ```bash
   apt update && apt upgrade -y
   apt install python3 python3-pip python3-venv nginx -y
   ```

4. **Setup Application Directory**
   ```bash
   mkdir -p /var/www/whites-management
   cd /var/www/whites-management
   ```

5. **Upload Your Application**
   - Use SCP or upload via Hostinger File Manager
   - Copy all files from your project to `/var/www/whites-management/`

6. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install streamlit pandas plotly xlsxwriter
   ```

7. **Configure Nginx**
   Create `/etc/nginx/sites-available/whites-management`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

8. **Enable Site**
   ```bash
   ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
   nginx -t
   systemctl reload nginx
   ```

9. **Create Systemd Service**
   Create `/etc/systemd/system/whites-management.service`:
   ```ini
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
   ```

10. **Start and Enable Service**
    ```bash
    systemctl daemon-reload
    systemctl start whites-management
    systemctl enable whites-management
    ```

11. **Setup SSL Certificate (Optional but Recommended)**
    ```bash
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

### Option 2: Hostinger Shared Hosting
More limited but cheaper option (if Python is supported).

#### Steps:
1. **Check Python Support**
   - Login to Hostinger control panel
   - Check if Python applications are supported
   - Look for "Python App" in the hosting features

2. **Upload Files**
   - Use File Manager to upload all project files
   - Place in public_html or appropriate directory

3. **Configure Application**
   - May need to modify port settings
   - Check Hostinger documentation for Python app deployment

## Application Configuration for Hostinger

### 1. Update Streamlit Config
Create `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "127.0.0.1"
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### 2. Security Considerations
- Ensure data directory has proper permissions
- Consider adding basic authentication
- Regular backups of CSV data files

### 3. Domain Setup
1. In Hostinger control panel, point your domain to the server
2. Update DNS settings if needed
3. Configure any subdomains (e.g., fleet.yourdomain.com)

## Cost Estimates

### VPS Hosting (Recommended)
- **VPS 1**: £3.99/month (1 GB RAM, 20 GB SSD)
- **VPS 2**: £7.99/month (2 GB RAM, 40 GB SSD)
- **VPS 3**: £15.99/month (4 GB RAM, 80 GB SSD)

### Shared Hosting
- **Business**: £2.99/month (if Python supported)
- **Premium**: £1.99/month (basic features)

## Backup Strategy
```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /backups/whites-management-$DATE.tar.gz /var/www/whites-management/data/
```

## Monitoring and Maintenance
- Monitor application logs: `journalctl -u whites-management -f`
- Check system resources: `htop`
- Regular data backups
- Update dependencies periodically

## Troubleshooting

### Common Issues:
1. **Port conflicts**: Ensure port 8501 is available
2. **Permission issues**: Check file permissions for data directory
3. **Memory issues**: Monitor RAM usage, upgrade if needed
4. **SSL certificate**: Renew automatically with certbot

### Support Resources:
- Hostinger Knowledge Base
- SSH access for debugging
- Application logs in systemd journal

## Next Steps
1. Choose your hosting plan (VPS recommended)
2. Setup domain DNS if not already done
3. Follow deployment steps
4. Test application functionality
5. Setup monitoring and backups

Would you like me to help you with any specific part of this deployment process?