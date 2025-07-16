terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "EC2 Key Pair name"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

variable "domain_name" {
  description = "Domain name"
  type        = string
  default     = "whitesaggs.com"
}

variable "allowed_ssh_cidr" {
  description = "CIDR block for SSH access"
  type        = string
  default     = "0.0.0.0/0"
}

# Data sources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Resources
resource "aws_security_group" "whites_management" {
  name_prefix = "whites-management-"
  description = "Security group for Whites Management"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
    description = "SSH"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Whites Management Security Group"
  }
}

resource "aws_iam_role" "whites_management" {
  name = "whites-management-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_instance_profile" "whites_management" {
  name = "whites-management-profile"
  role = aws_iam_role.whites_management.name
}

resource "aws_s3_bucket" "backup" {
  bucket = "whites-management-backups-${random_string.bucket_suffix.result}"
}

resource "aws_s3_bucket_versioning" "backup" {
  bucket = aws_s3_bucket.backup.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backup" {
  bucket = aws_s3_bucket.backup.id

  rule {
    id     = "delete_old_backups"
    status = "Enabled"

    expiration {
      days = 90
    }
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_instance" "whites_management" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.whites_management.id]
  subnet_id              = data.aws_subnets.default.ids[0]
  iam_instance_profile   = aws_iam_instance_profile.whites_management.name

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    bucket_name = aws_s3_bucket.backup.bucket
  }))

  tags = {
    Name = "Whites Management Admin Panel"
    Environment = "Production"
  }
}

resource "aws_eip" "whites_management" {
  domain   = "vpc"
  instance = aws_instance.whites_management.id

  tags = {
    Name = "Whites Management EIP"
  }
}

# Outputs
output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.whites_management.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_eip.whites_management.public_ip
}

output "application_url" {
  description = "Application URL"
  value       = "https://${var.domain_name}/admin"
}

output "ssh_command" {
  description = "SSH command"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_eip.whites_management.public_ip}"
}

output "backup_bucket" {
  description = "S3 backup bucket name"
  value       = aws_s3_bucket.backup.bucket
}
