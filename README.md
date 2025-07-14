# Whites Management System

Complete fleet, equipment, and maintenance management solution for Windows.

## Quick Start

1. **Install Python 3.11+** from [python.org](https://www.python.org/downloads/)
2. **Run installation**: Double-click `install_offline.bat`
3. **Start the system**: Double-click `start_app.bat`
4. **Access**: Open http://localhost:8501 in your browser

## Features

- **Vehicle Inventory**: Complete road vehicle management with VIN tracking
- **Plant Machine Inventory**: Excavators, bulldozers, cranes with operating hours
- **Maintenance Tracking**: Scheduling, history, and cost management
- **Equipment Hire**: Tool rental management with customer tracking
- **Financial Reporting**: Revenue, costs, and comprehensive statistics
- **Data Export**: Excel and CSV export capabilities
- **Offline Operation**: Works completely without internet after setup

## System Requirements

- Windows 10/11
- Python 3.11 or later
- 100MB free disk space

## File Structure

```
Whites_Management/
├── app.py                    # Main application
├── pages/                    # Page modules
├── utils/                    # Data management utilities
├── data/                     # CSV data storage
├── .streamlit/               # Configuration
├── *.bat                     # Windows installation scripts
└── *.md                      # Documentation
```

## Support Files

- `install_offline.bat` - Complete offline setup
- `install_packages.bat` - Standard package installation
- `check_system.bat` - System verification
- `backup_data.bat` - Data backup utility
- `start_app.bat` - Standard startup
- `start_app_simple.bat` - Simple startup

For detailed setup instructions, see `WINDOWS_SETUP.md`.