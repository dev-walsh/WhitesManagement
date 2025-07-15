#!/bin/bash

# Script to create separate deployment packages
echo "Creating separate deployment packages for Whites Management..."

# Clean up any existing packages
rm -f whites-management-*.tar.gz
rm -rf deployment-temp/

# Create temporary directories
mkdir -p deployment-temp/windows-offline
mkdir -p deployment-temp/ec2-cloud

echo "Preparing Windows Offline Package..."

# Windows Offline Package
cp -r pages/ deployment-temp/windows-offline/
cp -r utils/ deployment-temp/windows-offline/
cp -r .streamlit/ deployment-temp/windows-offline/
cp app.py deployment-temp/windows-offline/
cp pyproject.toml deployment-temp/windows-offline/

# Windows-specific files
cp *.bat deployment-temp/windows-offline/ 2>/dev/null || true
cp *WINDOWS*.md deployment-temp/windows-offline/ 2>/dev/null || true
cp DEPLOYMENT_GUIDE.md deployment-temp/windows-offline/ 2>/dev/null || true
cp TROUBLESHOOTING.md deployment-temp/windows-offline/ 2>/dev/null || true
cp OFFLINE_SETUP.md deployment-temp/windows-offline/ 2>/dev/null || true
cp offline_requirements.txt deployment-temp/windows-offline/ 2>/dev/null || true

# Create Windows requirements file
cat > deployment-temp/windows-offline/requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
EOF

# Create Windows README
cat > deployment-temp/windows-offline/README.md << EOF
# Whites Management - Windows Offline Version

## Quick Start for Windows

1. **Install Python 3.11**
   - Download from python.org
   - Make sure to check "Add Python to PATH"

2. **Run Installation**
   \`\`\`cmd
   install_packages.bat
   \`\`\`

3. **Start Application**
   \`\`\`cmd
   start_app.bat
   \`\`\`

4. **Access Application**
   - Open browser to: http://localhost:5000

## Features
- Complete offline operation
- Local CSV data storage
- Vehicle and machine inventory management
- Tool hire and rental tracking
- Maintenance records
- Dashboard and statistics

## Files Included
- Application source code
- Windows batch files for easy setup
- Offline documentation
- All dependencies included

## Requirements
- Windows 10/11
- Python 3.11 or higher
- 2GB RAM minimum
- 1GB disk space

## Support
See README_WINDOWS.md and TROUBLESHOOTING.md for detailed instructions.
EOF

echo "Preparing EC2 Cloud Package..."

# EC2 Cloud Package
cp -r pages/ deployment-temp/ec2-cloud/
cp -r utils/ deployment-temp/ec2-cloud/
cp -r .streamlit/ deployment-temp/ec2-cloud/
cp app.py deployment-temp/ec2-cloud/
cp pyproject.toml deployment-temp/ec2-cloud/

# EC2-specific files
cp AWS_EC2_DEPLOYMENT.md deployment-temp/ec2-cloud/ 2>/dev/null || true
cp ec2_setup_script.sh deployment-temp/ec2-cloud/ 2>/dev/null || true
cp HOSTINGER_DEPLOYMENT.md deployment-temp/ec2-cloud/ 2>/dev/null || true
cp hostinger_setup.sh deployment-temp/ec2-cloud/ 2>/dev/null || true

# Create EC2 requirements file
cat > deployment-temp/ec2-cloud/requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
EOF

# Create EC2-optimized Streamlit config
mkdir -p deployment-temp/ec2-cloud/.streamlit
cat > deployment-temp/ec2-cloud/.streamlit/config.toml << EOF
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

# Create EC2 README
cat > deployment-temp/ec2-cloud/README.md << EOF
# Whites Management - AWS EC2 Cloud Version

## Quick Start for AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.small or larger recommended
   - Security group: ports 22, 80, 443, 5000

2. **Upload and Setup**
   \`\`\`bash
   # Upload package to EC2
   scp -i your-key.pem -r . ubuntu@your-ec2-ip:~/whites-management/
   
   # Connect and run setup
   ssh -i your-key.pem ubuntu@your-ec2-ip
   cd whites-management
   chmod +x ec2_setup_script.sh
   ./ec2_setup_script.sh
   \`\`\`

3. **Access Application**
   - http://your-ec2-ip
   - Or your custom domain after DNS setup

## Features
- Production-ready cloud deployment
- Nginx reverse proxy
- SSL certificate support
- Automated backups
- Security hardening
- System monitoring

## Cloud Providers Supported
- AWS EC2 (primary)
- Hostinger VPS
- Any Ubuntu VPS provider

## Cost Estimates
- t3.micro: ~£8.50/month (Free tier eligible)
- t3.small: ~£17/month (Recommended)
- t3.medium: ~£34/month (High traffic)

## Support
See AWS_EC2_DEPLOYMENT.md for detailed instructions.
EOF

# Create helper scripts for EC2
cat > deployment-temp/ec2-cloud/upload_to_ec2.sh << 'EOF'
#!/bin/bash
# Helper script to upload to EC2
# Usage: ./upload_to_ec2.sh your-key.pem your-ec2-ip

if [ $# -ne 2 ]; then
    echo "Usage: $0 <key-file.pem> <ec2-ip-address>"
    echo "Example: $0 my-key.pem 1.2.3.4"
    exit 1
fi

KEY_FILE="$1"
EC2_IP="$2"

echo "Uploading Whites Management to EC2..."
scp -i "$KEY_FILE" -r . ubuntu@"$EC2_IP":~/whites-management/

echo "Connecting to EC2 for setup..."
ssh -i "$KEY_FILE" ubuntu@"$EC2_IP" "cd whites-management && chmod +x ec2_setup_script.sh && ./ec2_setup_script.sh"
EOF

chmod +x deployment-temp/ec2-cloud/upload_to_ec2.sh

echo "Creating archive packages..."

# Create Windows package
cd deployment-temp/windows-offline
tar --exclude=".DS_Store" --exclude="*.pyc" --exclude="__pycache__" -czf ../../whites-management-windows-offline.tar.gz *
cd ../..

# Create EC2 package  
cd deployment-temp/ec2-cloud
tar --exclude=".DS_Store" --exclude="*.pyc" --exclude="__pycache__" -czf ../../whites-management-ec2-cloud.tar.gz *
cd ../..

# Clean up
rm -rf deployment-temp/

echo ""
echo "=== Deployment Packages Created ==="
echo ""
echo "Windows Offline Package:"
echo "  File: whites-management-windows-offline.tar.gz"
echo "  Size: $(du -h whites-management-windows-offline.tar.gz | cut -f1)"
echo "  Target: Windows 10/11 local installation"
echo ""
echo "EC2 Cloud Package:"
echo "  File: whites-management-ec2-cloud.tar.gz" 
echo "  Size: $(du -h whites-management-ec2-cloud.tar.gz | cut -f1)"
echo "  Target: AWS EC2 Ubuntu / Cloud VPS"
echo ""
echo "Both packages are ready for deployment!"