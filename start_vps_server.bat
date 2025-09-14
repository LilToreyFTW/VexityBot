@echo off
echo ========================================
echo    VexityBot VPS Server Startup
echo ========================================
echo.

echo [INFO] Starting VexityBot VPS Server GUI...
echo [INFO] Server IP: 191.96.152.162
echo [INFO] Server Port: 9999
echo [INFO] Web Port: 8080
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [ERROR] Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo [INFO] Checking dependencies...
python -c "import tkinter, flask, psutil" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Some dependencies are missing
    echo [INFO] Installing required packages...
    pip install -r vps_requirements.txt
)

REM Start the VPS server
echo [INFO] Launching VexityBot VPS Server GUI...
python vps_server_gui.py

pause