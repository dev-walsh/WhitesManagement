# Whites Management System - Complete Offline Package

## What You Need to Download

To run the Whites Management System completely offline on your Windows machine, you need to download these files to a folder on your computer (e.g., `C:\WhitesManagement\`):

## Core Application Files

### Main Application
- `app.py` - Main dashboard and entry point

### Pages (create a `pages\` folder)
- `pages\1_Vehicle_Inventory.py` - Road vehicle management
- `pages\2_Maintenance_Records.py` - Maintenance tracking  
- `pages\3_Dashboard.py` - Analytics and reporting
- `pages\4_Tool_Hire.py` - Equipment rental management
- `pages\5_Statistics.py` - Advanced statistics and reporting
- `pages\6_Machine_Inventory.py` - Plant machine management

### Utilities (create a `utils\` folder)
- `utils\data_manager.py` - Database operations
- `utils\validators.py` - Data validation

### Configuration (create a `.streamlit\` folder)
- `.streamlit\config.toml` - Streamlit settings

## Setup Files
- `WINDOWS_SETUP.md` - Complete installation guide
- `OFFLINE_SETUP.md` - Offline operation guide
- `offline_requirements.txt` - Python package list
- `install_packages.bat` - Install all required packages
- `start_app.bat` - Start the application (full version)
- `start_app_simple.bat` - Start the application (simple version)
- `backup_data.bat` - Backup your data
- `check_system.bat` - Verify installation

## Folder Structure

Create this exact folder structure on your Windows machine:

```
C:\WhitesManagement\
├── app.py
├── install_packages.bat
├── start_app.bat
├── start_app_simple.bat
├── backup_data.bat
├── check_system.bat
├── offline_requirements.txt
├── WINDOWS_SETUP.md
├── OFFLINE_SETUP.md
├── DOWNLOAD_PACKAGE.md
├── pages\
│   ├── 1_Vehicle_Inventory.py
│   ├── 2_Maintenance_Records.py
│   ├── 3_Dashboard.py
│   ├── 4_Tool_Hire.py
│   ├── 5_Statistics.py
│   └── 6_Machine_Inventory.py
├── utils\
│   ├── data_manager.py
│   └── validators.py
└── .streamlit\
    └── config.toml
```

## Installation Steps Summary

1. **Install Python 3.11** from python.org (check "Add Python to PATH")
2. **Download all files** to `C:\WhitesManagement\`
3. **Install packages**: Double-click `install_packages.bat` (or use manual method)
4. **Run system check**: Double-click `check_system.bat`
5. **Start application**: Double-click `start_app.bat`

## Key Features

✅ **Completely Offline** - No internet required after setup
✅ **British Currency** - All costs shown in £ 
✅ **Road Vehicle Management** - Track fleet with Whites ID system
✅ **Plant Machine Management** - Heavy equipment with operating hours
✅ **Equipment Hire** - Complete rental management with revenue tracking
✅ **Maintenance Tracking** - Full service history and scheduling
✅ **Modern Interface** - Horizontal navigation, no sidebar
✅ **Dashboard Analytics** - Real-time business insights and reports
✅ **Data Export/Import** - CSV and Excel file support
✅ **Comprehensive Backups** - Protect all your data

## Data Storage

- All data stored in CSV files in `data\` folder
- Automatically created on first run
- Easy to backup and restore
- No database server required

## Support

- Follow the detailed `WINDOWS_SETUP.md` guide
- Use `check_system.bat` to verify installation
- Regular backups with `backup_data.bat`
- All operations work offline