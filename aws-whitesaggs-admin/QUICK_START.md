# Quick Start Guide - AWS Deployment for whitesaggs.com/admin

## Prerequisites
- AWS Account with EC2 access
- AWS CLI configured (`aws configure`)
- EC2 Key Pair created
- Domain whitesaggs.com registered

## Option 1: CloudFormation (Recommended)
```bash
# Deploy with CloudFormation
./scripts/deploy_with_cli.sh
```

## Option 2: Terraform
```bash
# Initialize Terraform
cd configs/
terraform init

# Create terraform.tfvars
cat > terraform.tfvars << EOF
key_name = "your-key-pair-name"
instance_type = "t3.small"
domain_name = "whitesaggs.com"
allowed_ssh_cidr = "YOUR_IP/32"
