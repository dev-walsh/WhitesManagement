@echo off
echo ===================================================
echo    Whites Management System - Data Backup Utility
echo    Backup All Fleet & Equipment Data
echo ===================================================
echo.

REM Set backup location
set backup_folder=C:\WhitesManagement_Backups

REM Create date stamp (YYYYMMDD format)
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "date_stamp=%dt:~0,8%"
set "time_stamp=%dt:~8,6%"

REM Create backup directory
set "backup_path=%backup_folder%\backup_%date_stamp%_%time_stamp%"
mkdir "%backup_path%" 2>nul

echo ===================================================
echo Backing up Whites Management data files...
echo ===================================================

REM Check if data folder exists
if not exist "data\" (
    echo ! No data folder found - creating sample structure
    mkdir "data" 2>nul
    echo Sample data structure created
    echo Note: Add your vehicles, equipment, and maintenance data to start using the system
) else (
    echo ✓ Data folder found
)

REM Copy data files
echo.
echo ✓ Copying data files...
if exist "data\" (
    xcopy "data\*" "%backup_path%\" /E /Y /Q
    echo   └── Vehicle data (vehicles.csv)
    echo   └── Machine data (machines.csv) 
    echo   └── Maintenance records (maintenance.csv)
    echo   └── Equipment inventory (equipment.csv)
    echo   └── Rental records (rentals.csv)
)

REM Backup application files
echo.
echo ✓ Backing up system configuration...
if exist "*.py" xcopy "*.py" "%backup_path%\app_files\" /E /I /Y /Q >nul
if exist "pages\*.py" xcopy "pages\*.py" "%backup_path%\app_files\pages\" /E /I /Y /Q >nul
if exist "utils\*.py" xcopy "utils\*.py" "%backup_path%\app_files\utils\" /E /I /Y /Q >nul

REM Copy batch files and documentation
if exist "*.bat" xcopy "*.bat" "%backup_path%\setup_files\" /E /I /Y /Q >nul
if exist "*.md" xcopy "*.md" "%backup_path%\setup_files\" /E /I /Y /Q >nul
if exist "*.txt" xcopy "*.txt" "%backup_path%\setup_files\" /E /I /Y /Q >nul

REM Create backup info file
echo.
echo ✓ Creating backup information file...
echo Whites Management System Backup > "%backup_path%\backup_info.txt"
echo Backup Date: %date% %time% >> "%backup_path%\backup_info.txt"
echo System Version: Horizontal Navigation Update >> "%backup_path%\backup_info.txt"
echo. >> "%backup_path%\backup_info.txt"
echo Backed up components: >> "%backup_path%\backup_info.txt"
echo - Vehicle inventory data >> "%backup_path%\backup_info.txt"
echo - Plant machine inventory >> "%backup_path%\backup_info.txt"
echo - Maintenance records >> "%backup_path%\backup_info.txt"
echo - Equipment and rental data >> "%backup_path%\backup_info.txt"
echo - System configuration files >> "%backup_path%\backup_info.txt"
echo - Windows setup scripts >> "%backup_path%\backup_info.txt"

REM Check if backup was successful
if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo SUCCESS: Complete system backup completed!
    echo ===================================================
    echo.
    echo Backup location: %backup_path%
    echo.
    echo BACKED UP FILES:
    if exist "%backup_path%\vehicles.csv" echo ✓ Vehicle data
    if exist "%backup_path%\machines.csv" echo ✓ Machine data
    if exist "%backup_path%\maintenance.csv" echo ✓ Maintenance records
    if exist "%backup_path%\equipment.csv" echo ✓ Equipment inventory
    if exist "%backup_path%\rentals.csv" echo ✓ Rental records
    echo ✓ Application files
    echo ✓ Setup scripts
    echo.
    echo To restore: Copy contents back to your Whites Management directory
) else (
    echo.
    echo ! Some files may not have been backed up
    echo Check the backup folder: %backup_path%
)

echo.
echo Backup complete! Keep this backup safe.
pause