# Fleet Management System - Windows Offline Setup

This guide will help you set up and run the Fleet Management System on your Windows machine completely offline.

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

### Step 2: Download the Fleet Management System

1. **Create a folder** for the application:
   ```
   C:\FleetManagement\
   ```

2. **Copy all files** from this project to the folder:
   - app.py
   - pages\ folder (with all .py files inside)
   - utils\ folder (with all .py files inside)
   - .streamlit\ folder (with config.toml)
   - requirements.txt (see below)
   - start_app.bat (see below)

### Step 3: Install Required Packages

1. **Create requirements.txt** in your FleetManagement folder with this content:
   ```
   streamlit==1.28.1
   pandas==2.1.3
   plotly==5.17.0
   ```

2. **Install packages**:
   - Open Command Prompt as Administrator
   - Navigate to your folder: `cd C:\FleetManagement`
   - Install packages: `pip install -r requirements.txt`

### Step 4: Create Startup Script

Create a file called `start_app.bat` in your FleetManagement folder:

```batch
@echo off
echo Starting Fleet Management System...
echo.
echo The application will open in your web browser.
echo To stop the application, close this window or press Ctrl+C
echo.
cd /d "%~dp0"
python -m streamlit run app.py --server.port 8501 --server.address localhost
pause
```

## Running the Application

### Method 1: Using the Batch File
1. Double-click `start_app.bat`
2. The application will start and open in your web browser
3. Access URL: http://localhost:8501

### Method 2: Using Command Line
1. Open Command Prompt
2. Navigate to: `cd C:\FleetManagement`
3. Run: `streamlit run app.py`
4. Open browser to: http://localhost:8501

## Data Storage

- All your data is stored in CSV files in the `data\` folder
- Files created automatically:
  - `vehicles.csv` - Vehicle inventory
  - `maintenance.csv` - Maintenance records
  - `equipment.csv` - Equipment inventory
  - `rentals.csv` - Rental records

## Backup Your Data

**Important**: Regularly backup your `data\` folder to prevent data loss.

### Simple Backup Method:
1. Copy the entire `data\` folder
2. Paste it to a backup location (USB drive, network folder, etc.)
3. Rename with date: `data_backup_2025-01-15`

### Automated Backup (Optional):
Create `backup_data.bat`:
```batch
@echo off
set backup_folder=C:\FleetManagement_Backups
set date_stamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%
mkdir "%backup_folder%\%date_stamp%" 2>nul
xcopy "C:\FleetManagement\data" "%backup_folder%\%date_stamp%\" /E /Y
echo Backup completed to %backup_folder%\%date_stamp%
pause
```

## Troubleshooting

### Application Won't Start
1. Check Python installation: `python --version`
2. Check Streamlit installation: `pip show streamlit`
3. Ensure you're in the correct folder
4. Check for error messages in Command Prompt

### Browser Doesn't Open
1. Manually go to: http://localhost:8501
2. Try different browser
3. Check if port 8501 is blocked by firewall

### Permission Errors
1. Run Command Prompt as Administrator
2. Check folder permissions
3. Ensure antivirus isn't blocking files

### Data Not Saving
1. Check if `data\` folder exists
2. Verify write permissions to the folder
3. Check disk space

## Features Available Offline

✅ **Complete Vehicle Management**
- Add, edit, delete vehicles
- Track vehicle status (On Hire/Off Hire)
- Mileage tracking
- Custom vehicle types
- Defects and notes

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
- Fleet overview
- Financial summaries
- Equipment utilization
- Interactive charts

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
C:\FleetManagement\
├── app.py
├── start_app.bat
├── requirements.txt
├── WINDOWS_SETUP.md
├── pages\
│   ├── 1_Vehicle_Inventory.py
│   ├── 2_Maintenance_Records.py
│   ├── 3_Dashboard.py
│   └── 4_Tool_Hire.py
├── utils\
│   ├── data_manager.py
│   └── validators.py
├── .streamlit\
│   └── config.toml
└── data\
    ├── vehicles.csv
    ├── maintenance.csv
    ├── equipment.csv
    └── rentals.csv
```