# Complete Deployment Guide: Streamlit + WordPress on Hostinger

## Overview
Since Hostinger shared hosting doesn't support Python/Streamlit, we'll use a hybrid approach:
1. Deploy your Streamlit app on **Streamlit Community Cloud** (FREE)
2. Set up WordPress on **Hostinger** 
3. Integrate them seamlessly using WordPress pages

## Part 1: Deploy Streamlit App (FREE)

### Step 1: Prepare Your Code for GitHub
```bash
# Create a new repository on GitHub (go to github.com)
# Clone this repository locally or push your existing code

# Required files for deployment:
- app.py (main application)
- login.py (authentication)
- utils/data_manager.py
- utils/validators.py
- requirements.txt (dependencies)
- .streamlit/config.toml (configuration)
```

### Step 2: Create requirements.txt
Create a file called `requirements.txt` with these dependencies:
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
xlsxwriter>=3.1.0
```

### Step 3: Create .streamlit/config.toml
Create folder `.streamlit` and file `config.toml` inside it:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
base = "dark"
```

### Step 4: Push to GitHub
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial deployment - Whites Management System"

# Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/whites-management.git

# Push to GitHub
git push -u origin main
```

### Step 5: Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io/
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your repositories
4. Click "New app"
5. Select your repository
6. Set main file path: `app.py`
7. Click "Deploy!"

**Your app will be available at:** `https://yourusername-whites-management-app-xxxxx.streamlit.app`

## Part 2: Set Up WordPress on Hostinger

### Step 1: Access Hostinger Control Panel
1. Log into your Hostinger account
2. Go to "Hosting" → Select your hosting plan
3. Click "Manage" next to your domain

### Step 2: Install WordPress
1. In the control panel, find "Auto Installer" or "WordPress"
2. Click "Install WordPress"
3. Choose your domain (e.g., whitesaggs.com)
4. Set up admin credentials:
   - Username: `whitesadmin`
   - Password: `WhitesFleet2025!`
   - Email: your email address
5. Click "Install"

### Step 3: Access WordPress Admin
1. Go to `https://whitesaggs.com/wp-admin`
2. Login with your WordPress credentials
3. You'll see the WordPress dashboard

## Part 3: Integrate Streamlit with WordPress

### Step 1: Create Admin Page
1. In WordPress dashboard, go to "Pages" → "Add New"
2. Title: "Dashboard" or "Admin Panel"
3. Set URL slug: `admin` (so it becomes whitesaggs.com/admin)

### Step 2: Add Streamlit Integration Code
In the page content, switch to "HTML" or "Code" mode and add:

```html
<div class="streamlit-container">
    <style>
        .streamlit-container {
            width: 100%;
            min-height: 100vh;
            background: #1a1a2e;
            margin: 0;
            padding: 0;
        }
        
        .streamlit-frame {
            width: 100%;
            height: 100vh;
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .loading-message {
            text-align: center;
            padding: 50px;
            color: #64b5f6;
            font-size: 18px;
            background: #1a1a2e;
        }
        
        @media (max-width: 768px) {
            .streamlit-frame {
                height: 90vh;
            }
        }
    </style>
    
    <div class="loading-message">
        Loading Whites Management System...
    </div>
    
    <iframe 
        src="https://yourusername-whites-management-app-xxxxx.streamlit.app" 
        class="streamlit-frame"
        onload="document.querySelector('.loading-message').style.display='none';">
    </iframe>
</div>
```

**Important:** Replace `yourusername-whites-management-app-xxxxx.streamlit.app` with your actual Streamlit app URL.

### Step 3: Configure Page Settings
1. Set page template to "Full Width" (if available)
2. Remove sidebar and comments
3. Set page visibility to "Private" or "Password Protected" for security
4. Save the page

### Step 4: Add to Navigation Menu
1. Go to "Appearance" → "Menus"
2. Create a new menu called "Main Menu"
3. Add your admin page to the menu
4. Set menu location to "Primary Menu"
5. Save menu

## Part 4: Advanced WordPress Configuration

### Step 1: Install Required Plugins
1. Go to "Plugins" → "Add New"
2. Search and install these plugins:
   - **Disable Comments** (security)
   - **Wordfence Security** (security)
   - **WP Super Cache** (performance)
   - **Custom CSS and JS** (styling)

### Step 2: Security Configuration
1. In Wordfence, enable:
   - Firewall protection
   - Malware scanning
   - Login security
2. Change WordPress login URL from `/wp-admin` to something custom
3. Limit login attempts

### Step 3: Custom CSS for Better Integration
Go to "Appearance" → "Customize" → "Custom CSS":

```css
/* Hide WordPress admin bar for non-admins */
#wpadminbar {
    display: none !important;
}

/* Full-width page styling */
.admin-page {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}

/* Remove default WordPress page margins */
.admin-page .entry-content {
    margin: 0;
    padding: 0;
}

/* Responsive design */
@media (max-width: 768px) {
    .streamlit-frame {
        height: 90vh;
    }
}
```

## Part 5: Domain and SSL Setup

### Step 1: Configure Domain
1. In Hostinger panel, go to "Domains"
2. Point your domain to Hostinger nameservers
3. Set up subdomain routing if needed

### Step 2: SSL Certificate
1. In Hostinger panel, go to "SSL"
2. Enable "Force HTTPS" for your domain
3. Install Let's Encrypt SSL certificate (free)

## Part 6: Testing and Troubleshooting

### Step 1: Test Complete Flow
1. Visit `https://whitesaggs.com/admin`
2. Verify the Streamlit app loads properly
3. Test login with credentials:
   - Username: `whitesadmin`
   - Password: `WhitesFleet2025!`
4. Test all CRUD operations
5. Verify mobile responsiveness

### Step 2: Common Issues and Solutions

**Issue: Streamlit app doesn't load**
- Check if Streamlit Community Cloud app is running
- Verify iframe URL is correct
- Check browser console for errors

**Issue: Login doesn't work**
- Ensure Streamlit app is using correct credentials
- Check if session timeout is working

**Issue: Mobile display problems**
- Adjust iframe height in CSS
- Test on different devices

## Part 7: Maintenance and Updates

### Step 1: Regular Updates
1. **Streamlit App**: Push changes to GitHub, auto-deploys
2. **WordPress**: Keep WordPress and plugins updated
3. **Security**: Monitor Wordfence security reports

### Step 2: Backup Strategy
1. **Streamlit Data**: CSV files are stored in app, consider backup
2. **WordPress**: Use Hostinger's backup feature
3. **Domain**: Keep domain registration current

### Step 3: Performance Monitoring
1. Monitor Streamlit app performance
2. Check WordPress loading speed
3. Monitor SSL certificate expiration

## Final Result

After completing all steps, you'll have:
- ✅ **WordPress site** at `https://whitesaggs.com`
- ✅ **Management system** at `https://whitesaggs.com/admin`
- ✅ **Secure login** with production credentials
- ✅ **Mobile-responsive** design
- ✅ **SSL encryption** for security
- ✅ **Professional appearance** with seamless integration

Your users will access the system through your WordPress site, and it will appear as a single, integrated application.

## Support Resources

- **Streamlit Community Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **WordPress Support**: https://wordpress.org/support/
- **Hostinger Help**: https://support.hostinger.com/
- **Your App URL**: Update this with your actual Streamlit app URL

## Cost Summary
- **Streamlit Community Cloud**: FREE
- **Hostinger Hosting**: Your existing hosting plan
- **Domain**: Your existing domain
- **SSL Certificate**: FREE with Hostinger
- **Total Additional Cost**: $0

This solution gives you a professional, secure, and cost-effective deployment of your Whites Management System!