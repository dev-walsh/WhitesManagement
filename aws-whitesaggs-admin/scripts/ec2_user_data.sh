#!/bin/bash
# AWS EC2 User Data Script for automated deployment

# Log all output
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Update system
apt-get update
apt-get upgrade -y

# Install git
apt-get install -y git

# Clone or download the deployment package
cd /tmp
# You would replace this with your actual repository or download URL
# git clone https://github.com/your-repo/whites-management.git
# cd whites-management

# Run deployment script
chmod +x scripts/aws_whitesaggs_deployment.sh
./scripts/aws_whitesaggs_deployment.sh

echo "EC2 user data script completed"
