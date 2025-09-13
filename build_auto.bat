@echo off
echo VexityBot Auto Build Script
echo ===========================

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "VexityBot.spec" del "VexityBot.spec"

echo.
echo Building VexityBot executable...
cd VexityBot
python -m PyInstaller --onefile --windowed --name=VexityBot --exclude-module=dnspython --exclude-module=scapy --exclude-module=nmap --exclude-module=cryptography --exclude-module=requests main_gui_only.py

echo.
echo Checking if build was successful...
if exist "dist\VexityBot.exe" (
    echo SUCCESS: VexityBot.exe created successfully!
    echo Location: VexityBot\dist\VexityBot.exe
    echo Size: 
    dir "dist\VexityBot.exe" | findstr "VexityBot.exe"
    echo.
    echo Build completed successfully!
) else (
    echo ERROR: Build failed! VexityBot.exe not found.
    echo Check the error messages above.
)

echo.
echo Build process completed!
