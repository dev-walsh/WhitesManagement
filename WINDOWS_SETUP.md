# Whites Management System - Windows Offline Setup

This guide will help you set up and run the Whites Management System on your Windows machine completely offline. This comprehensive solution handles vehicle inventory, plant machines, maintenance tracking, and equipment hire management.

## System Requirements

- Windows 10 or Windows 11
- At least 4GB RAM
- 500MB free disk space
- Administrator privileges (for Python installation)

## Installation Steps

### Step 1: Download and Install Python

1. **Download Python 3.11** from the official website:
   - Go to https://www.python.org/downloads/windows/
   - Download "Python 3.11.x" (latest 3.11 version)
   - Choose "Windows installer (64-bit)" for most systems

2. **Install Python**:
   - Run the downloaded installer
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Choose "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt (cmd)
   - Type: `python --version`
   - You should see: `Python 3.11.x`

### Step 2: Download the Whites Management System

1. **Create a folder** for the application:
   ```
   C:\WhitesManagement\
   ```

2. **Copy all files** from this project to the folder:
   - app.py
   - pages\ folder (with all .py files inside):
     - 1_Vehicle_Inventory.py
     - 2_Maintenance_Records.py
     - 3_Dashboard.py
     - 4_Tool_Hire.py
     - 5_Statistics.py
     - 6_Machine_Inventory.py
   - utils\ folder (with all .py files inside)
   - .streamlit\ folder (with config.toml)
   - offline_requirements.txt
   - start_app.bat
   - start_app_simple.bat
   - install_packages.bat
   - check_system.bat
   - backup_data.bat
   - All documentation files (.md)

### Step 3: Install Required Packages

**Easy Method**:
1. **Run the installer**: Double-click `install_packages.bat`
2. **Verify installation**: Double-click `check_system.bat`

**Manual Method** (if needed):
1. Open Command Prompt as Administrator
2. Navigate to your folder: `cd C:\WhitesManagement`
3. Install packages: `pip install -r offline_requirements.txt`

### Step 4: Startup Scripts (Already Included)

The following startup scripts are already included in your download:

- `start_app.bat` - Full featured startup with system information
- `start_app_simple.bat` - Simple startup for quick access
- `check_system.bat` - Verify installation before running
- `backup_data.bat` - Backup all your business data

## Running the Application

### Method 1: Using the Batch File
1. Double-click `start_app.bat`
2. The application will start and open in your web browser
3. Access URL: http://localhost:8501

### Method 2: Using Command Line
1. Open Command Prompt
2. Navigate to: `cd C:\WhitesManagement`
3. Run: `streamlit run app.py`
4. Open browser to: http://localhost:8501

### Method 3: System Verification First
1. Double-click `check_system.bat` to verify installation
2. If all checks pass, use Method 1 or 2 above

## Data Storage

- All your data is stored in CSV files in the `data\` folder
- Files created automatically:
  - `vehicles.csv` - Road vehicle inventory  
  - `machines.csv` - Plant machine inventory
  - `maintenance.csv` - Maintenance records
  - `equipment.csv` - Equipment inventory
  - `rentals.csv` - Rental records

## Backup Your Data

**Important**: Regularly backup your `data\` folder to prevent data loss.

### Simple Backup Method:
1. Copy the entire `data\` folder
2. Paste it to a backup location (USB drive, network folder, etc.)
3. Rename with date: `data_backup_2025-01-15`

### Automated Backup (Included):
The system includes `backup_data.bat` which automatically:
- Creates timestamped backups in `C:\WhitesManagement_Backups\`
- Backs up all data files (vehicles, machines, maintenance, equipment, rentals)
- Backs up system configuration files
- Creates backup information file with details
- Simply double-click to run

## Troubleshooting

### Quick Solutions for Common Errors

**"AttributeError: module 'streamlit' has no attribute 'switch_page'"**
- Upgrade Streamlit: `pip install --upgrade streamlit`
- Or use sidebar navigation (this error has been fixed in the app)

**Application Won't Start**
1. Run `check_system.bat` to verify installation
2. Check Python installation: `python --version`
3. Try `start_app_simple.bat` instead

**Navigation Issues**
- Use the horizontal navigation bar at the top of the page
- No sidebar navigation (clean interface design)
- Click navigation buttons to switch between sections

**Interface Notes**
- Modern horizontal navigation replaces traditional sidebar
- Clean, professional appearance for business use
- All features accessible via top navigation menu

**See TROUBLESHOOTING.md for complete error solutions**

## Features Available Offline

✅ **Complete Vehicle Management**
- Road vehicle inventory with VIN/chassis tracking
- Vehicle status (On Hire/Off Hire/Under Maintenance)
- Mileage tracking and service history
- Custom vehicle types with Whites ID system
- Defects and notes management

✅ **Plant Machine Management**
- Heavy equipment inventory (excavators, bulldozers, cranes, etc.)
- Operating hours tracking instead of mileage
- Daily/weekly rental rates for machine hire
- Machine status and availability tracking
- Custom machine types and specifications

✅ **Maintenance Tracking**
- Log maintenance records
- Cost tracking in British pounds (£)
- Service provider information
- Due date tracking

✅ **Equipment & Tool Hire**
- Equipment inventory management
- Rental processing
- Customer management
- Revenue tracking
- Overdue rental alerts

✅ **Dashboard & Analytics**
- Comprehensive fleet overview with key metrics
- Financial summaries and cost analysis
- Equipment utilization and rental revenue
- Interactive charts and real-time statistics
- Modern horizontal navigation interface

✅ **Data Management**
- Import/Export CSV files
- Data backup capabilities
- Complete offline operation

## Security Notes

- No internet connection required after setup
- All data stays on your local machine
- No external services or cloud storage
- Complies with company offline policies

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify all installation steps
3. Ensure Python and packages are correctly installed
4. Check Windows Event Viewer for system errors

## File Structure

Your final folder should look like:
```
C:\WhitesManagement\
├── app.py
├── start_app.bat
├── start_app_simple.bat
├── install_packages.bat
├── check_system.bat
├── backup_data.bat
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
├── .streamlit\
│   └── config.toml
└── data\
    ├── vehicles.csv
    ├── machines.csv
    ├── maintenance.csv
    ├── equipment.csv
    └── rentals.csv
```