# Fleet Management System - Troubleshooting Guide

## Common Issues and Solutions

### 1. AttributeError: module 'streamlit' has no attribute 'switch_page'

**Problem**: You have an older version of Streamlit installed.

**Solution**:
```cmd
pip install --upgrade streamlit
```

If that doesn't work, try:
```cmd
pip uninstall streamlit
pip install streamlit>=1.28.0
```

**Alternative**: The application has been updated to work without this function. Simply use the sidebar navigation instead of the quick action buttons.

### 2. ImportError or ModuleNotFoundError

**Problem**: Required packages are not installed.

**Solution**:
1. Run `install_packages.bat` as Administrator
2. Or manually install:
```cmd
pip install streamlit>=1.28.0 pandas>=1.3.0 plotly>=5.0.0
```

### 3. Permission Denied Errors

**Problem**: Python cannot write to the data folder.

**Solutions**:
- Run the application as Administrator
- Check folder permissions for C:\FleetManagement
- Ensure antivirus is not blocking the application

### 4. Application Won't Start

**Problem**: Various startup issues.

**Check List**:
1. Python is installed: `python --version`
2. Packages are installed: Run `check_system.bat`
3. You're in the correct folder: `cd C:\FleetManagement`
4. Port 8501 is not in use by another application

**Solutions**:
- Close any other Streamlit applications
- Try a different port:
```cmd
streamlit run app.py --server.port 8502
```

### 5. Data Not Saving

**Problem**: CSV files are not being created or updated.

**Check**:
- Data folder exists in your FleetManagement directory
- You have write permissions
- Sufficient disk space available

**Solution**:
```cmd
mkdir data
```

### 6. Browser Not Opening Automatically

**Problem**: Streamlit starts but browser doesn't open.

**Solution**:
- Manually navigate to: http://localhost:8501
- Try different browsers (Chrome, Firefox, Edge)
- Check Windows Firewall settings

### 7. Charts Not Displaying

**Problem**: Plotly charts show as blank or error.

**Solution**:
```cmd
pip install --upgrade plotly
```

### 8. Python Not Found

**Problem**: 'python' is not recognized as a command.

**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or add Python to PATH manually:
   - Search "Environment Variables" in Windows
   - Add Python installation path to PATH variable
   - Restart Command Prompt

### 9. Older Streamlit Compatibility

**Problem**: You're using an older Streamlit version and getting errors.

**Workaround**:
The application has been updated to be compatible with older versions. Navigation buttons will show information messages instead of switching pages directly.

**Navigation**: Use the sidebar menu to navigate between pages:
- 🏠 Main Dashboard
- 🚗 Vehicle Inventory  
- 🔧 Maintenance Records
- 📊 Dashboard
- 🔧 Tool Hire

### 10. Company Firewall Issues

**Problem**: Packages won't install due to corporate firewall.

**Solutions**:
1. Ask IT department to whitelist PyPI (pypi.org)
2. Download packages manually and install offline
3. Use company's internal package repository if available

### 11. Windows Defender/Antivirus Blocking

**Problem**: Antivirus software blocks the application.

**Solutions**:
- Add FleetManagement folder to antivirus exclusions
- Temporarily disable real-time protection during installation
- Run from a different location (Desktop, Documents)

## Quick Fixes

### Reset Everything
If you encounter multiple issues:

1. Delete the entire FleetManagement folder
2. Create a new C:\FleetManagement folder
3. Copy all files again
4. Run `install_packages.bat` as Administrator
5. Run `check_system.bat` to verify
6. Run `start_app.bat`

### Manual Start
If batch files don't work:

```cmd
cd C:\FleetManagement
python -m streamlit run app.py --server.port 8501
```

### Check Installation
Verify your setup:

```cmd
python --version
pip list | findstr streamlit
pip list | findstr pandas
pip list | findstr plotly
```

## Getting Help

1. Run `check_system.bat` and note any error messages
2. Check Windows Event Viewer for system errors
3. Ensure all files are in the correct folder structure
4. Try running from Command Prompt to see detailed error messages

## Minimum System Requirements

- Windows 10 or 11
- Python 3.8 or higher (3.11 recommended)
- 4GB RAM minimum
- 500MB free disk space
- Administrator privileges for installation