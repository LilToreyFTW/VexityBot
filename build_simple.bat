@echo off
echo VexityBot Simple Build Script
echo =============================
echo.

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

echo.
echo Building VexityBot with minimal dependencies...
python -m PyInstaller --onefile --console --name=VexityBot_Simple main_gui.py

echo.
echo Checking if build was successful...
if exist "dist\VexityBot_Simple.exe" (
    echo.
    echo SUCCESS: VexityBot_Simple.exe created!
    echo Location: dist\VexityBot_Simple.exe
    echo.
    echo This version has minimal dependencies to avoid DLL issues.
    echo.
) else (
    echo ERROR: Build failed!
)

pause