@echo off
echo ===================================================
echo    Whites Management System - Offline Installation
echo    Complete Offline Setup for Windows
echo ===================================================
echo.
echo This script will prepare your system for complete offline operation.
echo It will install all required packages and configure the system
echo to work without any internet connection after initial setup.
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo REQUIRED: Python 3.11 or later
    echo Download from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During Python installation:
    echo 1. Check "Add Python to PATH"
    echo 2. Check "Install pip"
    echo 3. Choose "Customize installation"
    echo 4. Check "Add Python to environment variables"
    echo.
    pause
    exit /b 1
)

echo Found Python:
python --version
echo Location:
where python
echo.

REM Upgrade pip for offline compatibility
echo Upgrading pip for offline operation...
python -m pip install --upgrade pip

echo.
echo Installing packages for offline operation...
echo This includes all dependencies needed for complete offline functionality.
echo.

REM Install from requirements file
if exist "offline_requirements.txt" (
    echo Installing from offline_requirements.txt...
    pip install -r offline_requirements.txt --no-warn-script-location
) else (
    echo Installing packages individually...
    pip install "streamlit>=1.28.0" --no-warn-script-location
    pip install "pandas>=2.0.0" --no-warn-script-location
    pip install "plotly>=5.15.0" --no-warn-script-location
    pip install "xlsxwriter>=3.1.0" --no-warn-script-location
    pip install "openpyxl>=3.1.0" --no-warn-script-location
    pip install "urllib3>=2.0.0" --no-warn-script-location
    pip install "certifi>=2023.0.0" --no-warn-script-location
    pip install "requests>=2.31.0" --no-warn-script-location
    pip install "numpy>=1.24.0" --no-warn-script-location
    pip install "python-dateutil>=2.8.0" --no-warn-script-location
    pip install "pytz>=2023.0" --no-warn-script-location
)

REM Create data directory structure
echo.
echo Setting up data directory structure...
if not exist "data" mkdir "data"
if not exist ".streamlit" mkdir ".streamlit"

REM Create Streamlit config for offline operation
echo.
echo Creating offline configuration...
echo [server] > .streamlit\config.toml
echo headless = true >> .streamlit\config.toml
echo address = "localhost" >> .streamlit\config.toml
echo port = 8501 >> .streamlit\config.toml
echo. >> .streamlit\config.toml
echo [browser] >> .streamlit\config.toml
echo gatherUsageStats = false >> .streamlit\config.toml
echo. >> .streamlit\config.toml
echo [theme] >> .streamlit\config.toml
echo base = "light" >> .streamlit\config.toml
echo primaryColor = "#1f77b4" >> .streamlit\config.toml

echo.
echo ===================================================
echo OFFLINE INSTALLATION COMPLETE!
echo ===================================================
echo.
echo ✓ Python packages installed for offline operation
echo ✓ Data directory structure created
echo ✓ Streamlit configured for offline mode
echo ✓ System ready for complete offline use
echo.
echo NEXT STEPS:
echo 1. Run 'check_system.bat' to verify everything works
echo 2. Run 'start_app.bat' to start the system
echo 3. Access at: http://localhost:8501
echo.
echo OFFLINE FEATURES READY:
echo ✓ Vehicle inventory management
echo ✓ Plant machine tracking
echo ✓ Maintenance record keeping
echo ✓ Equipment hire management
echo ✓ Financial reporting and statistics
echo ✓ Data export to Excel and CSV
echo ✓ Horizontal navigation interface
echo.
echo NOTE: After this setup, no internet connection is required.
echo All data is stored locally in CSV files in the 'data' folder.
echo.
pause