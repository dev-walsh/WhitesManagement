@echo off
title Whites Management System - Quick Start

echo ===================================================
echo    Whites Management System - Quick Start
echo ===================================================
echo.
echo FIRST TIME SETUP CHECKLIST:
echo [ ] 1. Install Python 3.11+ from python.org
echo [ ] 2. Run 'install_packages.bat' (installs requirements)
echo [ ] 3. Run 'check_system.bat' (verifies installation)
echo [ ] 4. Run this file to start the system
echo.
echo CURRENT FEATURES:
echo - Modern horizontal navigation (no sidebar)
echo - Vehicle inventory with complete tracking
echo - Plant machine management with rental rates
echo - Maintenance scheduling and history
echo - Equipment hire management
echo - Dashboard with real-time statistics
echo - CSV and Excel data export capabilities
echo.
echo ACCESS URL: http://localhost:8501
echo.
echo Starting application...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Simple start with default settings
python -m streamlit run app.py --browser.gatherUsageStats false

echo.
echo Application closed.
pause