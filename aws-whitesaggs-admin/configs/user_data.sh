#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Update system
apt-get update
apt-get upgrade -y

# Install dependencies
apt-get install -y curl awscli

# Download and run deployment script
curl -sSL https://raw.githubusercontent.com/your-repo/whites-management/main/aws_whitesaggs_deployment.sh | bash

# Configure S3 backup
cat > /opt/whites-management/backup_to_s3.sh << 'S3_BACKUP_EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="whitesaggs_admin_data_$DATE.tar.gz"
S3_BUCKET="${bucket_name}"

# Create local backup
/opt/whites-management/backup_whitesaggs_admin.sh

# Upload to S3
aws s3 cp /opt/whites-management/backups/$BACKUP_FILE s3://$S3_BUCKET/backups/
S3_BACKUP_EOF

chmod +x /opt/whites-management/backup_to_s3.sh

# Setup daily S3 backup
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/whites-management/backup_to_s3.sh") | crontab -

echo "User data script completed"
