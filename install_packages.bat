@echo off
echo ===================================================
echo    Whites Management - Package Installation
echo ===================================================
echo.

echo Installing required Python packages...
echo This may take a few minutes...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 first, then run this script again.
    echo.
    pause
    exit /b 1
)

REM Install packages
echo Installing Streamlit...
pip install "streamlit>=1.28.0"

echo Installing Pandas...
pip install "pandas>=1.3.0"

echo Installing Plotly...
pip install "plotly>=5.0.0"

echo Installing XlsxWriter...
pip install "xlsxwriter>=3.0.0"

echo.
echo ===================================================
echo Installation complete!
echo ===================================================
echo.
echo Run 'check_system.bat' to verify the installation.
echo Then run 'start_app.bat' to start the application.
echo.
pause