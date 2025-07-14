@echo off
echo ===================================================
echo    Fleet Management System - Data Backup
echo ===================================================
echo.

REM Set backup location
set backup_folder=C:\FleetManagement_Backups

REM Create date stamp (YYYYMMDD format)
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "date_stamp=%dt:~0,8%"
set "time_stamp=%dt:~8,6%"

REM Create backup directory
set "backup_path=%backup_folder%\backup_%date_stamp%_%time_stamp%"
mkdir "%backup_path%" 2>nul

REM Check if data folder exists
if not exist "data\" (
    echo ERROR: No data folder found!
    echo Make sure you're running this from the FleetManagement directory.
    pause
    exit /b 1
)

REM Copy data files
echo Backing up data files...
xcopy "data\*" "%backup_path%\" /E /Y /Q

REM Check if backup was successful
if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo SUCCESS: Data backup completed!
    echo ===================================================
    echo.
    echo Backup location: %backup_path%
    echo.
    echo Files backed up:
    dir "%backup_path%" /B
) else (
    echo.
    echo ERROR: Backup failed!
    echo Please check permissions and try again.
)

echo.
pause