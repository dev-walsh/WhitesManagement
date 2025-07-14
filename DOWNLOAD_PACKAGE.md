# Fleet Management System - Complete Offline Package

## What You Need to Download

To run this Fleet Management System completely offline on your Windows machine, you need to download these files to a folder on your computer (e.g., `C:\FleetManagement\`):

## Core Application Files

### Main Application
- `app.py` - Main dashboard and entry point

### Pages (create a `pages\` folder)
- `pages\1_Vehicle_Inventory.py` - Vehicle management
- `pages\2_Maintenance_Records.py` - Maintenance tracking  
- `pages\3_Dashboard.py` - Analytics and reporting
- `pages\4_Tool_Hire.py` - Equipment rental management

### Utilities (create a `utils\` folder)
- `utils\data_manager.py` - Database operations
- `utils\validators.py` - Data validation

### Configuration (create a `.streamlit\` folder)
- `.streamlit\config.toml` - Streamlit settings

## Setup Files
- `WINDOWS_SETUP.md` - Complete installation guide
- `offline_requirements.txt` - Python package list
- `start_app.bat` - Start the application
- `backup_data.bat` - Backup your data
- `check_system.bat` - Verify installation

## Folder Structure

Create this exact folder structure on your Windows machine:

```
C:\FleetManagement\
├── app.py
├── start_app.bat
├── backup_data.bat
├── check_system.bat
├── offline_requirements.txt
├── WINDOWS_SETUP.md
├── pages\
│   ├── 1_Vehicle_Inventory.py
│   ├── 2_Maintenance_Records.py
│   ├── 3_Dashboard.py
│   └── 4_Tool_Hire.py
├── utils\
│   ├── data_manager.py
│   └── validators.py
└── .streamlit\
    └── config.toml
```

## Installation Steps Summary

1. **Install Python 3.11** from python.org
2. **Download all files** to `C:\FleetManagement\`
3. **Install packages**: Open Command Prompt as Administrator, navigate to the folder, run:
   ```
   pip install -r offline_requirements.txt
   ```
4. **Run system check**: Double-click `check_system.bat`
5. **Start application**: Double-click `start_app.bat`

## Key Features

✅ **Completely Offline** - No internet required after setup
✅ **British Currency** - All costs shown in £
✅ **Vehicle Management** - Track fleet with Whites ID system
✅ **Equipment Hire** - Complete rental management
✅ **Maintenance Tracking** - Full service history
✅ **Dashboard Analytics** - Business insights and reports
✅ **Data Export/Import** - CSV file support
✅ **Automatic Backups** - Protect your data

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