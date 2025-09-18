@echo off
echo Fixing Tkinter Build Issue
echo ==========================

echo Cleaning old builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building with Tkinter data collection...
pyinstaller --onefile --console --name=VexityBot_Ultimate --collect-data=tkinter --collect-submodules=tkinter main_gui.py

echo.
if exist "dist\VexityBot_Ultimate.exe" (
    echo SUCCESS! Tkinter issue should be fixed.
    echo Location: dist\VexityBot_Ultimate.exe
) else (
    echo Build failed!
)

pause
