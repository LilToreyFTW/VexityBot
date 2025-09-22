@echo off
chcp 65001 >nul
title TSM-SeniorOasisPanel Master System

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    TSM-SeniorOasisPanel                     ║
echo ║                   Master Control System                     ║
echo ║                        Version 2.0.0                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo ✅ Python found. Installing dependencies...
pip install pillow pywin32

echo.
echo 📋 Available Commands:
echo.
echo 1. 🖥️  Start Server: python TSM_SeniorOasisPanel_server.py
echo 2. 👤 Start Client: python TSM_SeniorOasisPanel_client.py
echo 3. 🖼️  Create Stealth Image: python TSM_StealthMode.py create ^<image^> [host] [port]
echo 4. 📦 Create Package: python TSM_StealthMode.py package ^<image^> [host] [port]
echo 5. 🔧 Enhanced VNC: python TSM_EnhancedVNC.py [server/client]
echo 6. 🧪 Run Tests: python TSM_SystemTest.py
echo 7. 🎬 Master Launcher: python TSM_Master_Launcher.py
echo 8. 📖 View Guide: type TSM_Complete_Guide.md
echo.

echo 🎯 Quick Start Options:
echo.
echo [1] Start Master Launcher (Recommended)
echo [2] Start Server Only
echo [3] Start Client Only
echo [4] Create Stealth Image
echo [5] Run System Tests
echo [6] View Complete Guide
echo [7] Exit
echo.

set /p choice="🔢 Choose option (1-7): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting Master Launcher...
    python TSM_Master_Launcher.py
) else if "%choice%"=="2" (
    echo.
    echo 🖥️ Starting TSM Server...
    python TSM_SeniorOasisPanel_server.py
) else if "%choice%"=="3" (
    echo.
    echo 👤 Starting TSM Client...
    python TSM_SeniorOasisPanel_client.py
) else if "%choice%"=="4" (
    echo.
    echo 🖼️ Creating Stealth Image...
    set /p image_path="📁 Enter image path: "
    if exist "%image_path%" (
        python TSM_StealthMode.py create "%image_path%"
    ) else (
        echo ❌ Image file not found
        pause
    )
) else if "%choice%"=="5" (
    echo.
    echo 🧪 Running System Tests...
    python TSM_SystemTest.py
    pause
) else if "%choice%"=="6" (
    echo.
    echo 📖 Opening Complete Guide...
    type TSM_Complete_Guide.md
    pause
) else if "%choice%"=="7" (
    echo.
    echo 👋 Thank you for using TSM-SeniorOasisPanel
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice
    pause
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo TSM-SeniorOasisPanel Quick Start Complete
echo ═══════════════════════════════════════════════════════════════
echo.
pause
