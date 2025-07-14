@echo off
echo ===================================================
echo    Whites Management - System Check
echo ===================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 and add it to PATH
    echo.
    goto :end
) else (
    echo ✓ Python is installed:
    python --version
)

echo.
echo Checking required packages...

echo Checking Streamlit...
python -c "import streamlit; print('✓ Streamlit version:', streamlit.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ Streamlit not found
    set missing_packages=1
)

echo Checking Pandas...
python -c "import pandas; print('✓ Pandas version:', pandas.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ Pandas not found
    set missing_packages=1
)

echo Checking Plotly...
python -c "import plotly; print('✓ Plotly version:', plotly.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ Plotly not found
    set missing_packages=1
)

echo Checking XlsxWriter...
python -c "import xlsxwriter; print('✓ XlsxWriter version:', xlsxwriter.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ✗ XlsxWriter not found
    set missing_packages=1
)

echo.
if defined missing_packages (
    echo Some packages are missing. To install them, run:
    echo pip install -r offline_requirements.txt
    echo.
) else (
    echo ✓ All required packages are installed!
    echo.
    echo System is ready to run the Whites Management System.
    echo Double-click 'start_app.bat' to start the application.
)

:end
echo.
pause