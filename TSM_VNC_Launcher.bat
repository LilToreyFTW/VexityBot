@echo off
chcp 65001 >nul
title TSM-SeniorOasisPanel VNC Integration

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              TSM-SeniorOasisPanel VNC Integration            ║
echo ║                    noVNC + TigerVNC + Web VNC                ║
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
echo 📋 VNC Integration Options:
echo.
echo [1] 🚀 Start Complete VNC Integration (All Services)
echo [2] 🐅 TigerVNC Only
echo [3] 🌐 noVNC Dashboard Only  
echo [4] 🖥️ Web VNC Only
echo [5] 🎯 TSM Master Launcher
echo [6] 🧪 Run System Tests
echo [7] 📖 View Complete Guide
echo [8] ❌ Exit
echo.

set /p choice="🔢 Choose option (1-8): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting Complete VNC Integration...
    echo This will start TigerVNC, noVNC Dashboard, and Web VNC
    echo.
    python TSM_Complete_Integration.py start
) else if "%choice%"=="2" (
    echo.
    echo 🐅 Starting TigerVNC...
    python TSM_Complete_Integration.py tigervnc
) else if "%choice%"=="3" (
    echo.
    echo 🌐 Starting noVNC Dashboard...
    python TSM_Complete_Integration.py novnc
) else if "%choice%"=="4" (
    echo.
    echo 🖥️ Starting Web VNC...
    python TSM_Complete_Integration.py webvnc
) else if "%choice%"=="5" (
    echo.
    echo 🎯 Starting TSM Master Launcher...
    python TSM_Master_Launcher.py
) else if "%choice%"=="6" (
    echo.
    echo 🧪 Running System Tests...
    python TSM_SystemTest.py
    pause
) else if "%choice%"=="7" (
    echo.
    echo 📖 Opening Complete Guide...
    type TSM_Complete_Guide.md
    pause
) else if "%choice%"=="8" (
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
echo TSM-SeniorOasisPanel VNC Integration Complete
echo ═══════════════════════════════════════════════════════════════
echo.
pause
