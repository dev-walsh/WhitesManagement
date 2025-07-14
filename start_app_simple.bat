@echo off
echo Whites Management System Starting...
echo.
echo If this is your first time, make sure you have:
echo 1. Installed Python 3.11
echo 2. Run install_packages.bat
echo 3. Run check_system.bat
echo.
echo The application will open at: http://localhost:8501
echo.

cd /d "%~dp0"
python -m streamlit run app.py

pause