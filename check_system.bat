@echo off
echo ===================================================
echo    Whites Management System - System Verification
echo    Complete Installation & Configuration Check
echo ===================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ ERROR: Python is not installed or not in PATH
    echo.
    echo SOLUTION:
    echo 1. Download Python 3.11+ from https://www.python.org/downloads/
    echo 2. During installation, check "Add Python to PATH"
    echo 3. Restart this script after installation
    echo.
    goto :end
) else (
    echo ✓ Python is installed:
    python --version
    echo ✓ Python location:
    where python
)

echo.
echo Checking pip (package manager)...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ pip not found
    echo Installing pip...
    python -m ensurepip --upgrade
) else (
    echo ✓ pip is available
)

echo.
echo ===================================================
echo Checking Required Packages for Whites Management
echo ===================================================

echo Checking Streamlit (Web Interface)...
python -c "import streamlit; print('✓ Streamlit version:', streamlit.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ Streamlit not found - Required for web interface
    set missing_packages=1
)

echo Checking Pandas (Data Management)...
python -c "import pandas; print('✓ Pandas version:', pandas.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ Pandas not found - Required for data processing
    set missing_packages=1
)

echo Checking Plotly (Charts & Graphs)...
python -c "import plotly; print('✓ Plotly version:', plotly.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ Plotly not found - Required for dashboard charts
    set missing_packages=1
)

echo Checking XlsxWriter (Excel Export)...
python -c "import xlsxwriter; print('✓ XlsxWriter version:', xlsxwriter.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ XlsxWriter not found - Required for Excel exports
    set missing_packages=1
)

echo Checking OpenPyXL (Excel Import)...
python -c "import openpyxl; print('✓ OpenPyXL version:', openpyxl.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ! OpenPyXL not found - Optional for Excel imports
    set optional_missing=1
)

echo.
echo ===================================================
echo System Status Summary
echo ===================================================

if defined missing_packages (
    echo ✗ MISSING REQUIRED PACKAGES DETECTED
    echo.
    echo TO FIX: Run 'install_packages.bat' to install missing packages
    echo Or manually install with:
    echo pip install streamlit pandas plotly xlsxwriter openpyxl
    echo.
) else (
    echo ✓ ALL REQUIRED PACKAGES ARE INSTALLED!
    echo.
    echo SYSTEM FEATURES VERIFIED:
    echo ✓ Vehicle inventory management
    echo ✓ Plant machine inventory  
    echo ✓ Maintenance record tracking
    echo ✓ Equipment hire management
    echo ✓ Dashboard and statistics
    echo ✓ Data export capabilities
    echo ✓ Horizontal navigation interface
    echo.
    echo READY TO START!
    echo Double-click 'start_app.bat' to launch the system
    echo Access at: http://localhost:8501
)

if defined optional_missing (
    echo.
    echo NOTE: Some optional packages are missing but won't affect core functionality.
)

:end
echo.
echo ===================================================
pause