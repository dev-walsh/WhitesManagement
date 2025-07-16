#!/bin/bash

# Create whitesaggs.com deployment package
echo "Creating whitesaggs.com deployment package..."

# Create deployment directory
mkdir -p whitesaggs-deployment
mkdir -p whitesaggs-deployment/scripts
mkdir -p whitesaggs-deployment/configs

# Copy core application files
cp -r pages/ whitesaggs-deployment/
cp -r utils/ whitesaggs-deployment/
cp -r .streamlit/ whitesaggs-deployment/
cp app.py whitesaggs-deployment/

# Copy whitesaggs-specific files
cp whitesaggs_deployment.sh whitesaggs-deployment/scripts/
cp WHITESAGGS_DEPLOYMENT.md whitesaggs-deployment/

# Create requirements file
cat > whitesaggs-deployment/requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
EOF

# Create DNS configuration guide
cat > whitesaggs-deployment/DNS_SETUP.md << EOF
# DNS Setup for whitesaggs.com

## Required DNS Records

Configure these records in your domain registrar's DNS settings:

### A Records (IPv4)
\`\`\`
Type: A
Name: @ (root domain)
Value: YOUR_SERVER_IP
TTL: 3600

Type: A
Name: www
Value: YOUR_SERVER_IP
TTL: 3600
\`\`\`

### Optional: AAAA Records (IPv6)
If your server has IPv6:
\`\`\`
Type: AAAA
Name: @
Value: YOUR_SERVER_IPv6
TTL: 3600

Type: AAAA
Name: www
Value: YOUR_SERVER_IPv6
TTL: 3600
\`\`\`

## DNS Propagation
- **Time**: 24-48 hours for full propagation
- **Check**: Use \`dig whitesaggs.com\` or online DNS checker
- **Verify**: Both whitesaggs.com and www.whitesaggs.com should resolve

## Common DNS Providers

### Cloudflare (Recommended)
1. Add whitesaggs.com to Cloudflare
2. Update nameservers at registrar
3. Add A records as above
4. Enable "Proxy status" for additional security

### Namecheap
1. Login to Namecheap account
2. Go to Domain List → Manage
3. Advanced DNS → Add records as above

### GoDaddy
1. Login to GoDaddy account
2. My Products → DNS → Manage Zones
3. Add records as above

### Google Domains
1. Login to Google Domains
2. My domains → DNS
3. Add records as above

## Testing DNS Setup
\`\`\`bash
# Test DNS resolution
dig whitesaggs.com
dig www.whitesaggs.com

# Test from different locations
nslookup whitesaggs.com 8.8.8.8
nslookup whitesaggs.com 1.1.1.1
\`\`\`

## SSL Certificate Requirements
- DNS must be properly configured first
- Both whitesaggs.com and www.whitesaggs.com must resolve
- Wait for full DNS propagation before running SSL setup
EOF

# Create server requirements guide
cat > whitesaggs-deployment/SERVER_REQUIREMENTS.md << EOF
# Server Requirements for whitesaggs.com

## Minimum Requirements
- **OS**: Ubuntu 22.04 LTS
- **RAM**: 1GB (2GB recommended)
- **Storage**: 20GB SSD
- **CPU**: 1 core (2 cores recommended)
- **Network**: 100Mbps connection

## Recommended Specifications
- **RAM**: 2GB-4GB for better performance
- **Storage**: 40GB SSD with backup space
- **CPU**: 2+ cores for concurrent users
- **Network**: 1Gbps connection

## Hosting Provider Recommendations

### Budget Option: Vultr
- **Cost**: \$3.50-6/month
- **Specs**: 1GB-2GB RAM, 1-2 CPU cores
- **Locations**: Multiple worldwide
- **Features**: Good performance/price ratio

### Recommended: DigitalOcean
- **Cost**: \$5-12/month
- **Specs**: 1GB-2GB RAM, 1-2 CPU cores
- **Locations**: Global presence
- **Features**: Excellent documentation, reliable

### Professional: Linode
- **Cost**: \$5-20/month
- **Specs**: 1GB-4GB RAM, 1-4 CPU cores
- **Locations**: High-performance networks
- **Features**: Developer-friendly, good support

### Enterprise: AWS EC2
- **Cost**: \$8-50/month
- **Specs**: Scalable configurations
- **Locations**: Global infrastructure
- **Features**: Enterprise-grade, highly scalable

## Security Requirements
- **SSH Key**: Required for secure access
- **Firewall**: UFW configured automatically
- **SSL**: Let's Encrypt certificate
- **Updates**: Automatic security updates

## Backup Requirements
- **Local**: Daily automated backups
- **Retention**: 30 days of backup history
- **Location**: /opt/whites-management/backups/
- **Format**: Compressed tar.gz files

## Monitoring Requirements
- **Health Checks**: Automated application monitoring
- **Logs**: Centralized logging with journalctl
- **Resources**: CPU, memory, disk monitoring
- **SSL**: Certificate expiration monitoring
EOF

# Create quick start guide
cat > whitesaggs-deployment/QUICK_START.md << EOF
# Quick Start Guide for whitesaggs.com

## Step 1: Get a Server
Choose a hosting provider and launch Ubuntu 22.04 LTS server:
- **Vultr**: \$3.50/month minimum
- **DigitalOcean**: \$5/month minimum
- **Linode**: \$5/month minimum

## Step 2: Configure DNS
Point whitesaggs.com to your server IP:
1. Login to your domain registrar
2. Go to DNS settings
3. Add A record: @ → YOUR_SERVER_IP
4. Add A record: www → YOUR_SERVER_IP
5. Wait 24-48 hours for propagation

## Step 3: Deploy Application
Connect to your server and run:
\`\`\`bash
# Upload and extract this package
tar -xzf whitesaggs-deployment.tar.gz
cd whitesaggs-deployment

# Run automated setup
sudo ./scripts/whitesaggs_deployment.sh
\`\`\`

## Step 4: Upload Files
\`\`\`bash
# Upload your application files
sudo /root/upload_whitesaggs_files.sh /path/to/extracted/whitesaggs-deployment
\`\`\`

## Step 5: Setup SSL
After DNS propagation:
\`\`\`bash
sudo /root/setup_ssl_whitesaggs.sh
\`\`\`

## Step 6: Access Your Application
- **HTTP**: http://whitesaggs.com
- **HTTPS**: https://whitesaggs.com (after SSL)

## Troubleshooting
- **Status**: \`sudo /root/check_whitesaggs_status.sh\`
- **Logs**: \`sudo journalctl -u whites-management -f\`
- **Restart**: \`sudo systemctl restart whites-management\`

## Support
See WHITESAGGS_DEPLOYMENT.md for detailed instructions.
EOF

# Create README for the package
cat > whitesaggs-deployment/README.md << EOF
# Whites Management for whitesaggs.com

This package contains everything needed to deploy the Whites Management system on your domain whitesaggs.com.

## What's Included
- Complete Whites Management application
- Automated deployment script for Ubuntu servers
- DNS configuration guide
- SSL certificate setup
- Monitoring and backup scripts
- Troubleshooting documentation

## Files Structure
- **app.py, pages/, utils/**: Core application files
- **scripts/**: Deployment and management scripts
- **DNS_SETUP.md**: DNS configuration guide
- **SERVER_REQUIREMENTS.md**: Server specifications
- **QUICK_START.md**: Fast deployment guide
- **WHITESAGGS_DEPLOYMENT.md**: Complete documentation

## Quick Deployment
1. Get Ubuntu 22.04 server
2. Configure DNS for whitesaggs.com
3. Run: \`sudo ./scripts/whitesaggs_deployment.sh\`
4. Upload files and setup SSL

## Support
Your Whites Management system will be professionally deployed on whitesaggs.com with:
- Nginx reverse proxy
- SSL certificate
- Automated backups
- System monitoring
- Security hardening

For detailed instructions, see WHITESAGGS_DEPLOYMENT.md
EOF

# Create archive
tar -czf whitesaggs-deployment.tar.gz whitesaggs-deployment/

# Clean up
rm -rf whitesaggs-deployment/

echo "whitesaggs.com deployment package created: whitesaggs-deployment.tar.gz"
echo "Package size: $(du -h whitesaggs-deployment.tar.gz | cut -f1)"