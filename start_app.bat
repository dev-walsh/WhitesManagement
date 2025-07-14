@echo off
echo ===================================================
echo    Whites Management System - Starting Application
echo    Complete Fleet & Equipment Management Solution
echo ===================================================
echo.
echo FEATURES:
echo - Vehicle Inventory (Road Vehicles)
echo - Machine Inventory (Plant Equipment) 
echo - Maintenance Records & Scheduling
echo - Tool & Equipment Hire Management
echo - Financial Dashboard & Statistics
echo - Horizontal Navigation Interface
echo.
echo Starting the application...
echo The system will automatically open in your web browser.
echo.
echo ACCESS: http://localhost:8501
echo.
echo TO STOP THE APPLICATION:
echo - Close this command window, or
echo - Press Ctrl+C in this window
echo.
echo NAVIGATION:
echo - Use the horizontal menu bar at the top
echo - No sidebar navigation (clean interface)
echo - Click buttons to switch between sections
echo.
echo ===================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.11+ first.
    echo Run 'install_packages.bat' after installing Python.
    pause
    exit /b 1
)

REM Start the application with optimal offline settings
echo Starting Whites Management System...
echo.
echo NOTE: This system works completely offline after installation
echo All data is stored locally in CSV files
echo.
python -m streamlit run app.py --server.port 8501 --server.address localhost --server.headless true --browser.gatherUsageStats false --global.disableWatchdogWarning true

echo.
echo ===================================================
echo Application has stopped.
echo Thank you for using Whites Management System!
echo ===================================================
pause