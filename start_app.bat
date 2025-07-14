@echo off
echo ===================================================
echo    Fleet Management System - Offline Version
echo ===================================================
echo.
echo Starting the application...
echo The system will open in your web browser.
echo.
echo To stop the application:
echo - Close this window, or
echo - Press Ctrl+C in this window
echo.
echo ===================================================
echo.

cd /d "%~dp0"
python -m streamlit run app.py --server.port 8501 --server.address localhost --server.headless true

echo.
echo Application has stopped.
pause