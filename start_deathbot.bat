@echo off
echo ========================================
echo    DeathBot #25 - Ultimate Destruction
echo ========================================
echo.

echo [DEATHBOT] Initializing DeathBot #25...
echo [DEATHBOT] ⚡ Ricochet Boom AC/12v Power
echo [DEATHBOT] 🔥 Auto-initiate Python Script
echo [DEATHBOT] ⏰ Countdown timer: 12 seconds
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [ERROR] Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo [DEATHBOT] Starting DeathBot #25...
echo [DEATHBOT] 💀 Ultimate Destruction Bot
echo [DEATHBOT] ⚠️  WARNING: EXTREMELY DANGEROUS  ⚠️
echo.

REM Start DeathBot
python DeathBot.py

pause
