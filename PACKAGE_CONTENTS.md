# Whites Management System - Package Contents

## Package Overview
Complete offline business management system for Windows.
**Total Size**: ~50KB (excluding data files)
**Python Files**: 8 files
**Windows Scripts**: 5 batch files  
**Documentation**: 6 files

## Core Application Files

### Main Application
- `app.py` - Main Streamlit application with horizontal navigation

### Page Modules (`pages/`)
- `1_Vehicle_Inventory.py` - Road vehicle management
- `2_Maintenance_Records.py` - Maintenance tracking
- `3_Dashboard.py` - Analytics and reporting
- `4_Tool_Hire.py` - Equipment rental management
- `5_Statistics.py` - Financial statistics
- `6_Machine_Inventory.py` - Plant machine management

### Utility Modules (`utils/`)
- `data_manager.py` - CSV data operations
- `validators.py` - Input validation functions

## Windows Installation Scripts

### Primary Scripts
- `install_offline.bat` - **RECOMMENDED** Complete offline setup
- `install_packages.bat` - Standard package installation
- `start_app.bat` - **MAIN STARTUP** Full-featured startup
- `start_app_simple.bat` - Simple startup option

### Maintenance Scripts
- `check_system.bat` - System verification
- `backup_data.bat` - Data backup utility

## Configuration Files

### Requirements
- `offline_requirements.txt` - Python package dependencies

### System Configuration
- `.streamlit/config.toml` - Streamlit configuration for offline operation

## Data Storage (`data/`)
- `vehicles.csv` - Road vehicle inventory
- `machines.csv` - Plant machine inventory  
- `maintenance.csv` - Maintenance records
- `equipment.csv` - Equipment inventory
- `rentals.csv` - Rental transactions

## Documentation Files

### Setup Guides
- `README.md` - Quick start guide
- `WINDOWS_SETUP.md` - Detailed Windows installation
- `OFFLINE_SETUP.md` - Offline operation guide
- `DOWNLOAD_PACKAGE.md` - Package information

### Support Documentation  
- `TROUBLESHOOTING.md` - Problem resolution
- `replit.md` - Technical architecture documentation

## Installation Instructions

1. **Download and extract** this package to your desired location
2. **Install Python 3.11+** from python.org (if not already installed)
3. **Run setup**: Double-click `install_offline.bat`
4. **Start system**: Double-click `start_app.bat`
5. **Access**: Open http://localhost:8501 in your browser

## Key Features Ready for Use

✓ Complete vehicle and machine inventory management
✓ Maintenance scheduling and tracking
✓ Equipment hire with customer management
✓ Financial reporting and statistics
✓ Data export to Excel and CSV
✓ Horizontal navigation interface
✓ Complete offline operation
✓ Windows optimized

## File Permissions
All `.bat` files should have execute permissions on Windows.
Python files require Python 3.11+ interpreter.

## Support
For issues, refer to `TROUBLESHOOTING.md` or `WINDOWS_SETUP.md`