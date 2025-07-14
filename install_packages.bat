@echo off
echo ===================================================
echo    Whites Management System - Package Installation
echo    Complete Offline Fleet & Equipment Management
echo ===================================================
echo.
echo This will install all required packages for:
echo - Vehicle Inventory Management (Road Vehicles)
echo - Plant Machine Inventory (Excavators, Bulldozers, etc.)
echo - Maintenance Record Tracking
echo - Tool & Equipment Hire Management
echo - Comprehensive Dashboard & Statistics
echo - Data Import/Export (CSV & Excel)
echo.

echo Installing required Python packages...
echo This may take a few minutes...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or later first, then run this script again.
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing core packages...

echo Installing Streamlit (Web Interface)...
pip install "streamlit>=1.28.0" --no-warn-script-location

echo Installing Pandas (Data Management)...
pip install "pandas>=2.0.0" --no-warn-script-location

echo Installing Plotly (Charts & Visualizations)...
pip install "plotly>=5.15.0" --no-warn-script-location

echo Installing XlsxWriter (Excel Export)...
pip install "xlsxwriter>=3.1.0" --no-warn-script-location

echo Installing additional utilities...
pip install "openpyxl>=3.1.0" --no-warn-script-location

echo.
echo ===================================================
echo Installation Complete!
echo ===================================================
echo.
echo The Whites Management System is now ready to use.
echo.
echo NEXT STEPS:
echo 1. Run 'check_system.bat' to verify installation
echo 2. Run 'start_app.bat' to start the application
echo 3. Access the system at http://localhost:8501
echo.
echo FEATURES INCLUDED:
echo - Horizontal navigation (no sidebar)
echo - Vehicle inventory with VIN tracking
echo - Plant machine inventory with operating hours
echo - Maintenance scheduling and tracking
echo - Equipment rental management
echo - Financial reporting and statistics
echo - Data export to CSV and Excel formats
echo.
pause