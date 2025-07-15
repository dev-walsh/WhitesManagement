#!/bin/bash

# Script to create EC2 deployment package
echo "Creating EC2 deployment package for Whites Management..."

# Create deployment directory
mkdir -p ec2-deployment

# Copy application files
cp -r pages/ ec2-deployment/
cp -r utils/ ec2-deployment/
cp -r .streamlit/ ec2-deployment/
cp app.py ec2-deployment/
cp pyproject.toml ec2-deployment/

# Copy deployment documentation
cp AWS_EC2_DEPLOYMENT.md ec2-deployment/
cp ec2_setup_script.sh ec2-deployment/

# Create EC2-specific requirements file
cat > ec2-deployment/requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
EOF

# Create EC2-specific config
mkdir -p ec2-deployment/.streamlit
cat > ec2-deployment/.streamlit/config.toml << EOF
[server]
headless = true
address = "0.0.0.0"
port = 5000
enableCORS = false
enableXsrfProtection = false
fileWatcherType = "poll"

[browser]
gatherUsageStats = false

[runner]
magicEnabled = false

[global]
developmentMode = false

[theme]
base = "light"
EOF

# Create README for EC2 deployment
cat > ec2-deployment/README_EC2.md << EOF
# Whites Management - EC2 Deployment Package

## Quick Start

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.small or larger recommended
   - Security group with ports 22, 80, 443, 5000

2. **Connect and Run Setup**
   \`\`\`bash
   # Upload this package to your EC2 instance
   scp -i your-key.pem -r ec2-deployment ubuntu@your-ec2-ip:~/
   
   # Connect to EC2
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Run automated setup
   cd ec2-deployment
   chmod +x ec2_setup_script.sh
   ./ec2_setup_script.sh
   
   # Upload application files
   ./upload_whites_files.sh .
   \`\`\`

3. **Configure Domain (Optional)**
   - Point your domain A record to EC2 IP
   - Run: \`./setup_ssl.sh\`

## Files Included
- Application source code (app.py, pages/, utils/)
- EC2 setup script (automated installation)
- Deployment documentation
- Requirements and configuration files

## Support
See AWS_EC2_DEPLOYMENT.md for detailed instructions.
EOF

# Create archive
tar -czf whites-management-ec2.tar.gz ec2-deployment/

# Cleanup
rm -rf ec2-deployment/

echo "EC2 deployment package created: whites-management-ec2.tar.gz"
echo "Package size: $(du -h whites-management-ec2.tar.gz | cut -f1)"