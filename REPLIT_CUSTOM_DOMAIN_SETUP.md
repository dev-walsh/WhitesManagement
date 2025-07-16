# Replit Custom Domain Setup for whitesaggs.com/admin

## Overview
This guide shows how to configure your Whites Management system on Replit with custom domain whitesaggs.com/admin.

## Step 1: Deploy on Replit
1. Your application is now deployed on Replit
2. You'll receive a Replit URL like: `https://your-app-name.your-username.repl.co`
3. Test the application at this URL first

## Step 2: Configure Custom Domain in Replit
1. Go to your Replit project
2. Click the "Deploy" button
3. In the deployment settings:
   - Enable "Custom Domain"
   - Enter your domain: `whitesaggs.com`
   - Configure subdirectory routing for `/admin`

## Step 3: DNS Configuration
Configure your domain registrar's DNS settings:

### Option A: CNAME Record (Recommended)
```
Type: CNAME
Name: whitesaggs.com
Value: your-app-name.your-username.repl.co
TTL: 300
```

### Option B: A Record (If CNAME not supported for root domain)
```
Type: A
Name: @
Value: [Replit's IP address]
TTL: 300
```

## Step 4: Subdirectory Routing Setup
Since you want `/admin` as the path, you have two options:

### Option A: Nginx Proxy (Recommended)
If you control the main whitesaggs.com site, configure nginx:

```nginx
location /admin {
    proxy_pass https://your-app-name.your-username.repl.co;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Script-Name /admin;
}
```

### Option B: Subdomain Approach
Use a subdomain instead:
- Domain: `admin.whitesaggs.com`
- Configure CNAME: `admin.whitesaggs.com` → `your-app-name.your-username.repl.co`

## Step 5: SSL Configuration
Replit automatically provides SSL certificates for custom domains.

## Step 6: Application Configuration
The application has been configured with:
- `baseUrlPath = "/admin"` in Streamlit config
- Proper routing for subdirectory access

## Step 7: Test Your Setup
1. Wait for DNS propagation (up to 48 hours)
2. Access your admin panel at: `https://whitesaggs.com/admin`
3. Verify all functionality works correctly

## Troubleshooting

### DNS Not Resolving
```bash
# Check DNS propagation
nslookup whitesaggs.com
dig whitesaggs.com
```

### SSL Certificate Issues
- Replit handles SSL automatically
- Wait for DNS propagation before SSL is issued
- Check Replit deployment logs for SSL status

### Subdirectory Not Working
- Verify nginx configuration on main server
- Check that baseUrlPath is correctly set
- Ensure proxy headers are properly configured

## Alternative: Full Domain Setup
If you want the entire whitesaggs.com to point to your Replit app:

1. Configure DNS to point to Replit
2. Remove `/admin` subdirectory requirement
3. Access directly at `https://whitesaggs.com`

## Cost Considerations
- Replit custom domains require a paid plan
- SSL certificates are included with custom domains
- No additional server costs compared to VPS hosting

## Support
- Replit provides built-in SSL and CDN
- Automatic scaling and uptime monitoring
- No server maintenance required

Your Whites Management system will be professionally hosted on Replit with your custom domain whitesaggs.com/admin.