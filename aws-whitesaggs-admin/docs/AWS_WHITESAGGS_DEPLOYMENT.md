# AWS Deployment Guide for whitesaggs.com/admin

## Overview
This guide provides step-by-step instructions for deploying the Whites Management system on AWS EC2 at whitesaggs.com/admin.

## Architecture
- **Domain**: whitesaggs.com/admin
- **Server**: AWS EC2 Ubuntu 22.04 LTS
- **Reverse Proxy**: Nginx
- **SSL**: Let's Encrypt
- **Database**: Local CSV files
- **Backups**: Local with S3 option

## AWS Prerequisites

### 1. AWS Account Setup
- Active AWS account
- EC2 access permissions
- Route 53 (optional, for DNS)
- S3 bucket (optional, for backups)

### 2. EC2 Instance Requirements
- **Instance Type**: t2.micro (free tier) or t3.small (recommended)
- **AMI**: Ubuntu 22.04 LTS
- **Storage**: 20GB EBS volume minimum
- **Security Group**: Configured for web traffic

## Quick Deployment

### Step 1: Launch EC2 Instance
1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose Ubuntu 22.04 LTS AMI
4. Select t2.micro (free tier) or t3.small (recommended)
5. Configure storage: 20GB minimum
6. Create or select key pair
7. Configure security group (see below)

### Step 2: Configure Security Group
Create inbound rules:
```
Rule 1: SSH (22) - Source: Your IP only
Rule 2: HTTP (80) - Source: 0.0.0.0/0
Rule 3: HTTPS (443) - Source: 0.0.0.0/0
```

### Step 3: Connect and Deploy
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Switch to root
sudo su -

# Download and run deployment script
curl -sSL https://raw.githubusercontent.com/your-repo/whites-management/main/aws_whitesaggs_deployment.sh | bash
```

### Step 4: Upload Application Files
```bash
# Upload your application files
/root/upload_whitesaggs_admin_files.sh /path/to/your/whites-management-files
```

### Step 5: Configure DNS
Choose one option:

#### Option A: Route 53 (Recommended)
```bash
# Get helper commands
/root/aws_route53_setup.sh
```

#### Option B: External Registrar
Point A records to your EC2 instance IP:
```
whitesaggs.com → Your EC2 IP
www.whitesaggs.com → Your EC2 IP
```

### Step 6: Setup SSL
```bash
# After DNS propagation (24-48 hours)
/root/setup_ssl_whitesaggs_admin.sh
```

## Detailed Setup Instructions

### EC2 Instance Configuration

#### Instance Types and Costs
```
t2.micro:  $0/month (free tier) - 1 vCPU, 1GB RAM
t3.small:  $15/month - 2 vCPU, 2GB RAM (recommended)
t3.medium: $30/month - 2 vCPU, 4GB RAM (high traffic)
```

#### Security Group Configuration
```bash
# Create security group
aws ec2 create-security-group \
    --group-name whites-management-sg \
    --description "Security group for Whites Management"

# Add SSH rule (replace YOUR_IP)
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 22 \
    --cidr YOUR_IP/32

# Add HTTP rule
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# Add HTTPS rule
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0
```

### DNS Configuration

#### Route 53 Setup
1. Create hosted zone for whitesaggs.com
2. Note the nameservers
3. Update domain registrar with Route 53 nameservers
4. Create A records pointing to EC2 instance IP

#### Manual DNS Configuration
At your domain registrar:
```
Type: A
Name: @ (or whitesaggs.com)
Value: YOUR_EC2_IP
TTL: 300

Type: A
Name: www
Value: YOUR_EC2_IP
TTL: 300
```

### SSL Certificate Setup

#### Automatic Setup (Recommended)
```bash
/root/setup_ssl_whitesaggs_admin.sh
```

#### Manual Setup
```bash
# Stop nginx
sudo systemctl stop nginx

# Get certificate
sudo certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email admin@whitesaggs.com \
    -d whitesaggs.com \
    -d www.whitesaggs.com

# Update nginx config (included in script)
# Start nginx
sudo systemctl start nginx
```

## Application Configuration

### Streamlit Configuration
The deployment automatically configures Streamlit for subdirectory routing:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
baseUrlPath = "/admin"
```

### Nginx Configuration
Nginx routes requests to the admin panel:
```nginx
location /admin {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header X-Script-Name /admin;
    # Additional headers...
}
```

## Monitoring and Maintenance

### Health Checks
```bash
# Check overall status
/root/check_whitesaggs_admin_status.sh

# Check individual components
sudo systemctl status whites-management
sudo systemctl status nginx
curl http://localhost:5000/health
```

### Log Monitoring
```bash
# Application logs
sudo journalctl -u whites-management -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Resource Monitoring
```bash
# CPU and memory
htop

# Disk usage
df -h

# Network usage
sudo netstat -tulpn
```

## Backup Strategy

### Local Backups (Included)
- **Frequency**: Daily at 2:00 AM
- **Location**: `/opt/whites-management/backups/`
- **Retention**: 30 days
- **Format**: Compressed tar.gz

### S3 Backups (Optional)
```bash
# Install AWS CLI (already included in deployment)
# Configure AWS credentials
aws configure

# Create backup script with S3 upload
cat >> /opt/whites-management/backup_to_s3.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="whitesaggs_admin_data_$DATE.tar.gz"
S3_BUCKET="your-backup-bucket"

# Create local backup
/opt/whites-management/backup_whitesaggs_admin.sh

# Upload to S3
aws s3 cp /opt/whites-management/backups/$BACKUP_FILE s3://$S3_BUCKET/backups/

# Clean up old S3 backups (keep 90 days)
aws s3api list-objects-v2 --bucket $S3_BUCKET --prefix backups/ \
    --query 'Contents[?LastModified<`2024-01-01`].Key' \
    --output text | xargs -I {} aws s3 rm s3://$S3_BUCKET/{}
EOF

chmod +x /opt/whites-management/backup_to_s3.sh
```

## Security Hardening

### SSH Security
```bash
# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Disable password authentication
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Restart SSH
sudo systemctl restart ssh
```

### Firewall Configuration
```bash
# UFW is configured automatically, but you can also use AWS Security Groups
sudo ufw status
```

### Application Security
- SSL/TLS encryption
- Security headers in Nginx
- Regular security updates
- Restricted file permissions

## Cost Optimization

### EC2 Instance Costs
```
t2.micro:  Free tier (12 months) then $8.50/month
t3.small:  $15.18/month
t3.medium: $30.37/month
```

### Additional AWS Costs
```
EBS Storage: $0.10/GB/month (20GB = $2/month)
Data Transfer: $0.09/GB (first 1TB free)
Route 53: $0.50/hosted zone/month
```

### Cost Reduction Tips
1. Use t2.micro for testing (free tier)
2. Enable detailed monitoring only if needed
3. Use S3 for backups (cheaper than EBS snapshots)
4. Set up billing alerts

## Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check logs
sudo journalctl -u whites-management --no-pager

# Restart service
sudo systemctl restart whites-management
```

#### 2. 502 Bad Gateway
```bash
# Check if app is running
curl http://localhost:5000/health

# Check port binding
sudo netstat -tulpn | grep :5000
```

#### 3. SSL Certificate Issues
```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew --dry-run
```

#### 4. DNS Not Resolving
```bash
# Check from server
dig whitesaggs.com
nslookup whitesaggs.com

# Check from external
nslookup whitesaggs.com 8.8.8.8
```

### Performance Issues

#### High CPU Usage
```bash
# Check processes
top -p $(pgrep -f streamlit)

# Consider upgrading instance type
# t2.micro → t3.small
```

#### High Memory Usage
```bash
# Check memory
free -h

# Restart application
sudo systemctl restart whites-management
```

#### Slow Loading
```bash
# Check nginx logs
sudo tail -f /var/log/nginx/access.log

# Enable nginx caching if needed
```

## Scaling Options

### Vertical Scaling
- Upgrade EC2 instance type
- Add more storage
- Increase network bandwidth

### Horizontal Scaling
- Application Load Balancer
- Auto Scaling Group
- Multiple availability zones

### Database Scaling
- Migrate to RDS (PostgreSQL/MySQL)
- Add Redis for caching
- Implement database connection pooling

## Deployment Automation

### AWS CloudFormation Template
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Whites Management Admin Panel Infrastructure'

Parameters:
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: EC2 Key Pair for SSH access

Resources:
  WhitesManagementInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c02fb55956c7d316  # Ubuntu 22.04
      InstanceType: t3.small
      KeyName: !Ref KeyName
      SecurityGroups:
        - !Ref WhitesManagementSG
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          curl -sSL https://raw.githubusercontent.com/your-repo/whites-management/main/aws_whitesaggs_deployment.sh | bash

  WhitesManagementSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for Whites Management
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
```

### Terraform Configuration
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "whites_management" {
  ami           = "ami-0c02fb55956c7d316"  # Ubuntu 22.04
  instance_type = "t3.small"
  key_name      = var.key_name
  
  vpc_security_group_ids = [aws_security_group.whites_management.id]
  
  user_data = <<-EOF
    #!/bin/bash
    curl -sSL https://raw.githubusercontent.com/your-repo/whites-management/main/aws_whitesaggs_deployment.sh | bash
  EOF
  
  tags = {
    Name = "Whites Management Admin"
  }
}

resource "aws_security_group" "whites_management" {
  name_prefix = "whites-management-"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Summary

This deployment provides:
- Professional AWS EC2 hosting
- Subdirectory routing (whitesaggs.com/admin)
- SSL certificate automation
- Daily backups
- Monitoring and logging
- Security hardening
- Cost optimization

Your Whites Management system will be accessible at https://whitesaggs.com/admin with enterprise-grade hosting on AWS infrastructure.