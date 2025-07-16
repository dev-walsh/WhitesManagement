#!/bin/bash

# Domain Setup Helper Script for Whites Management
# This script helps configure your custom domain deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Function to check if domain is valid
validate_domain() {
    local domain=$1
    if [[ $domain =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to check DNS resolution
check_dns() {
    local domain=$1
    local expected_ip=$2
    
    print_info "Checking DNS resolution for $domain..."
    
    # Check if domain resolves
    if resolved_ip=$(dig +short "$domain" A | head -n1); then
        if [[ -n "$resolved_ip" ]]; then
            if [[ "$resolved_ip" == "$expected_ip" ]]; then
                print_success "DNS correctly points to $expected_ip"
                return 0
            else
                print_warning "DNS points to $resolved_ip but expected $expected_ip"
                return 1
            fi
        else
            print_warning "Domain does not resolve to any IP address"
            return 1
        fi
    else
        print_error "Cannot resolve domain $domain"
        return 1
    fi
}

# Function to generate Nginx configuration
generate_nginx_config() {
    local domain=$1
    local app_port=${2:-5000}
    
    cat > "nginx_${domain}.conf" << EOF
server {
    listen 80;
    server_name $domain www.$domain;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # File upload size limit
    client_max_body_size 50M;
    
    # Main proxy configuration
    location / {
        proxy_pass http://127.0.0.1:$app_port;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF
    
    print_success "Generated Nginx configuration: nginx_${domain}.conf"
}

# Function to generate SSL setup script
generate_ssl_script() {
    local domain=$1
    local email=${2:-"admin@$domain"}
    
    cat > "setup_ssl_${domain}.sh" << EOF
#!/bin/bash
# SSL Setup Script for $domain

set -e

echo "Setting up SSL certificate for $domain..."

# Install certbot if not present
if ! command -v certbot &> /dev/null; then
    echo "Installing certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
fi

# Stop nginx temporarily
sudo systemctl stop nginx

# Get certificate
sudo certbot certonly --standalone \\
    --non-interactive \\
    --agree-tos \\
    --email "$email" \\
    -d "$domain" \\
    -d "www.$domain"

# Update nginx configuration for SSL
sudo tee /etc/nginx/sites-available/whites-management > /dev/null <<'NGINX_EOF'
server {
    listen 80;
    server_name $domain www.$domain;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $domain www.$domain;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$domain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$domain/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
}
NGINX_EOF

# Start nginx
sudo systemctl start nginx
sudo systemctl reload nginx

# Setup auto-renewal
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "SSL certificate installed successfully!"
echo "Your site is now available at: https://$domain"
EOF
    
    chmod +x "setup_ssl_${domain}.sh"
    print_success "Generated SSL setup script: setup_ssl_${domain}.sh"
}

# Function to generate deployment instructions
generate_deployment_guide() {
    local domain=$1
    local hosting_type=$2
    
    cat > "DEPLOY_${domain}.md" << EOF
# Deployment Guide for $domain

## Hosting Type: $hosting_type

### Step 1: Server Setup
1. Launch Ubuntu 22.04 server
2. Update system: \`sudo apt update && sudo apt upgrade -y\`
3. Install dependencies: \`sudo apt install -y python3.11 python3.11-venv python3-pip nginx git curl\`

### Step 2: DNS Configuration
Point your domain DNS to your server IP:
\`\`\`
Type: A
Name: @ (for root domain) or subdomain name
Value: YOUR_SERVER_IP
TTL: 3600
\`\`\`

### Step 3: Application Setup
\`\`\`bash
# Create application directory
sudo mkdir -p /opt/whites-management
cd /opt/whites-management

# Upload your application files here
# Extract: tar -xzf whites-management-*.tar.gz

# Create virtual environment
sudo python3.11 -m venv venv
sudo ./venv/bin/pip install streamlit pandas plotly xlsxwriter

# Create systemd service
sudo tee /etc/systemd/system/whites-management.service > /dev/null <<'SERVICE_EOF'
[Unit]
Description=Whites Management Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/whites-management
Environment=PATH=/opt/whites-management/venv/bin
ExecStart=/opt/whites-management/venv/bin/streamlit run app.py --server.port 5000 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Set permissions
sudo chown -R www-data:www-data /opt/whites-management
sudo chmod -R 755 /opt/whites-management

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable whites-management
sudo systemctl start whites-management
\`\`\`

### Step 4: Nginx Configuration
\`\`\`bash
# Use the generated nginx configuration
sudo cp nginx_${domain}.conf /etc/nginx/sites-available/whites-management
sudo ln -s /etc/nginx/sites-available/whites-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
\`\`\`

### Step 5: SSL Certificate
\`\`\`bash
# Run the SSL setup script
./setup_ssl_${domain}.sh
\`\`\`

### Step 6: Firewall Configuration
\`\`\`bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
\`\`\`

## Verification
- HTTP: http://$domain
- HTTPS: https://$domain (after SSL setup)

## Maintenance
- Check status: \`sudo systemctl status whites-management\`
- View logs: \`sudo journalctl -u whites-management -f\`
- Restart: \`sudo systemctl restart whites-management\`

## Backup
\`\`\`bash
# Daily backup
tar -czf /backup/whites-data-\$(date +%Y%m%d).tar.gz /opt/whites-management/data/
\`\`\`
EOF
    
    print_success "Generated deployment guide: DEPLOY_${domain}.md"
}

# Main script
main() {
    print_header "Whites Management - Domain Setup Helper"
    
    # Get domain from user
    echo "Enter your domain name (e.g., yourdomain.com or fleet.yourdomain.com):"
    read -r domain
    
    # Validate domain
    if ! validate_domain "$domain"; then
        print_error "Invalid domain format"
        exit 1
    fi
    
    print_success "Domain validated: $domain"
    
    # Get hosting type
    echo ""
    echo "Select your hosting type:"
    echo "1) VPS (DigitalOcean, Linode, AWS EC2, etc.)"
    echo "2) Shared Hosting with SSH"
    echo "3) Cloud Platform (Heroku, Railway, etc.)"
    echo "4) Don't know / Need recommendation"
    echo ""
    read -p "Enter choice (1-4): " hosting_choice
    
    case $hosting_choice in
        1) hosting_type="VPS" ;;
        2) hosting_type="Shared Hosting" ;;
        3) hosting_type="Cloud Platform" ;;
        4) hosting_type="Recommendation Needed" ;;
        *) print_error "Invalid choice"; exit 1 ;;
    esac
    
    # Get server IP if VPS
    if [[ "$hosting_type" == "VPS" ]]; then
        echo ""
        echo "Enter your server IP address (optional, for DNS checking):"
        read -r server_ip
        
        if [[ -n "$server_ip" ]]; then
            check_dns "$domain" "$server_ip"
        fi
    fi
    
    # Get email for SSL
    echo ""
    echo "Enter email for SSL certificate (default: admin@$domain):"
    read -r ssl_email
    ssl_email=${ssl_email:-"admin@$domain"}
    
    print_header "Generating Configuration Files"
    
    # Generate files
    generate_nginx_config "$domain"
    generate_ssl_script "$domain" "$ssl_email"
    generate_deployment_guide "$domain" "$hosting_type"
    
    print_header "Files Generated"
    
    echo "The following files have been created:"
    echo "  📝 nginx_${domain}.conf - Nginx configuration"
    echo "  🔐 setup_ssl_${domain}.sh - SSL setup script"
    echo "  📋 DEPLOY_${domain}.md - Complete deployment guide"
    echo ""
    
    if [[ "$hosting_type" == "VPS" ]]; then
        print_info "Next steps for VPS deployment:"
        echo "1. Upload your Whites Management files to your server"
        echo "2. Follow the instructions in DEPLOY_${domain}.md"
        echo "3. Configure your domain DNS to point to your server IP"
        echo "4. Run the SSL setup script after DNS propagation"
    elif [[ "$hosting_type" == "Cloud Platform" ]]; then
        print_info "For cloud platforms like Heroku:"
        echo "1. Check the platform's documentation for custom domains"
        echo "2. Most platforms provide CNAME records for custom domains"
        echo "3. SSL is usually handled automatically by the platform"
    else
        print_info "Follow the deployment guide for your specific hosting setup"
    fi
    
    print_success "Setup helper complete!"
}

# Run main function
main "$@"