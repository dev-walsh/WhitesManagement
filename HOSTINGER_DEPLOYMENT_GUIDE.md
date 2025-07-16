# Hostinger Deployment Guide: WordPress + Streamlit Integration

## Problem Statement
Hostinger shared hosting does NOT support Python/Streamlit. This guide shows how to integrate your Streamlit app with WordPress on Hostinger.

## Solution: Hybrid Deployment

### Step 1: Deploy Streamlit App (Free)
1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Community Cloud**
   - Go to https://share.streamlit.io/
   - Connect your GitHub account
   - Select your repository
   - Click "Deploy"
   - Get your app URL: `https://yourapp.streamlit.app`

### Step 2: Set Up WordPress on Hostinger

1. **Install WordPress** via Hostinger's 1-click installer
2. **Create Custom Pages** for your app integration
3. **Add iframes** to embed your Streamlit app

### Step 3: WordPress Integration Code

#### Method 1: Simple iframe Embedding
```html
<!-- Add to WordPress page/post -->
<iframe src="https://yourapp.streamlit.app" 
        width="100%" 
        height="800px"
        frameborder="0">
</iframe>
```

#### Method 2: Custom WordPress Page Template
Create `page-dashboard.php` in your theme:
```php
<?php
/*
Template Name: Dashboard
*/
get_header(); ?>

<div id="primary" class="content-area">
    <main id="main" class="site-main">
        <div class="dashboard-container">
            <h1>Whites Management Dashboard</h1>
            <iframe src="https://yourapp.streamlit.app" 
                    width="100%" 
                    height="800px"
                    frameborder="0">
            </iframe>
        </div>
    </main>
</div>

<?php get_footer(); ?>
```

#### Method 3: WordPress Shortcode
Add to your theme's `functions.php`:
```php
function dashboard_shortcode() {
    return '<iframe src="https://yourapp.streamlit.app" width="100%" height="800px" frameborder="0"></iframe>';
}
add_shortcode('dashboard', 'dashboard_shortcode');
```

Use in any page: `[dashboard]`

### Step 4: Styling Integration

Add CSS to WordPress theme:
```css
.dashboard-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 20px;
}

.dashboard-container iframe {
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
    .dashboard-container iframe {
        height: 600px;
    }
}
```

### Step 5: Navigation Menu

Add dashboard link to WordPress menu:
1. Go to WordPress Admin → Appearance → Menus
2. Add Custom Link:
   - URL: `/dashboard/`
   - Link Text: "Dashboard"

## Alternative: Convert to PHP/WordPress

If you prefer a fully integrated solution, convert your app to PHP:

### Required WordPress Plugins
- **Advanced Custom Fields** - For data forms
- **WP Data Tables** - For data display
- **User Role Editor** - For admin access

### Database Structure
```sql
-- Create custom tables in WordPress database
CREATE TABLE wp_vehicles (
    id int(11) NOT NULL AUTO_INCREMENT,
    whites_id varchar(20),
    make varchar(100),
    model varchar(100),
    year int(4),
    license_plate varchar(20),
    status varchar(20),
    PRIMARY KEY (id)
);
```

### PHP Forms (WordPress Custom Post Types)
```php
// Custom post type for vehicles
function register_vehicle_post_type() {
    register_post_type('vehicle', array(
        'labels' => array(
            'name' => 'Vehicles',
            'singular_name' => 'Vehicle'
        ),
        'public' => true,
        'supports' => array('title', 'custom-fields'),
        'show_in_admin_bar' => true,
    ));
}
add_action('init', 'register_vehicle_post_type');
```

## Recommendation

**Use Option 1 (Hybrid Approach)** because:
- ✅ Keeps your existing Streamlit code
- ✅ Free hosting for the app
- ✅ Easy to maintain
- ✅ Professional appearance
- ✅ Mobile responsive

The PHP conversion would require completely rewriting your application.

## Final Steps

1. Deploy Streamlit app on Community Cloud
2. Set up WordPress on Hostinger
3. Create dashboard page with iframe
4. Style integration
5. Add to navigation menu

Your users won't notice the difference - they'll see a seamless experience!