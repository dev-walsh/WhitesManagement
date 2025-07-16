#!/bin/bash

# AWS CLI deployment script for whitesaggs.com/admin

set -e

# Configuration
REGION="us-east-1"
INSTANCE_TYPE="t3.small"
KEY_NAME=""
DOMAIN_NAME="whitesaggs.com"
STACK_NAME="whites-management-admin"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    print_error "AWS CLI not configured. Run 'aws configure' first."
    exit 1
fi

# Get key name if not provided
if [ -z "$KEY_NAME" ]; then
    echo "Available key pairs:"
    aws ec2 describe-key-pairs --region $REGION --output table
    echo ""
    read -p "Enter your EC2 key pair name: " KEY_NAME
fi

# Get VPC and subnet
VPC_ID=$(aws ec2 describe-vpcs --region $REGION --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text)
SUBNET_ID=$(aws ec2 describe-subnets --region $REGION --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[0].SubnetId' --output text)

print_status "Using VPC: $VPC_ID"
print_status "Using Subnet: $SUBNET_ID"

# Deploy CloudFormation stack
print_status "Deploying CloudFormation stack..."
aws cloudformation create-stack \
    --stack-name $STACK_NAME \
    --template-body file://configs/cloudformation.yaml \
    --parameters \
        ParameterKey=KeyName,ParameterValue=$KEY_NAME \
        ParameterKey=InstanceType,ParameterValue=$INSTANCE_TYPE \
        ParameterKey=VpcId,ParameterValue=$VPC_ID \
        ParameterKey=SubnetId,ParameterValue=$SUBNET_ID \
        ParameterKey=DomainName,ParameterValue=$DOMAIN_NAME \
    --capabilities CAPABILITY_IAM \
    --region $REGION

print_status "Stack creation initiated. Waiting for completion..."
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $REGION

# Get stack outputs
PUBLIC_IP=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION --query 'Stacks[0].Outputs[?OutputKey==`PublicIP`].OutputValue' --output text)
INSTANCE_ID=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION --query 'Stacks[0].Outputs[?OutputKey==`InstanceId`].OutputValue' --output text)

print_status "Deployment completed successfully!"
echo ""
echo "Stack Name: $STACK_NAME"
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "SSH Command: ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
echo ""
echo "Next steps:"
echo "1. Point $DOMAIN_NAME DNS to $PUBLIC_IP"
echo "2. Wait for DNS propagation (24-48 hours)"
echo "3. SSH to server and run: /root/setup_ssl_whitesaggs_admin.sh"
echo "4. Access admin panel at: https://$DOMAIN_NAME/admin"
