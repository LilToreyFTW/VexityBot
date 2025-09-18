@echo off
echo Quick Tkinter Fix
echo =================

echo Cleaning old builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building with minimal dependencies and Tkinter fix...
pyinstaller --onefile --console --name=VexityBot_Ultimate --collect-data=tkinter --collect-submodules=tkinter --exclude-module=numpy --exclude-module=pandas --exclude-module=torch --exclude-module=opencv-python --exclude-module=scipy --exclude-module=sklearn --exclude-module=tensorflow main_gui.py

echo.
if exist "dist\VexityBot_Ultimate.exe" (
    echo SUCCESS! Tkinter issue should be fixed.
    echo Location: dist\VexityBot_Ultimate.exe
    echo.
    echo Testing the executable...
    start "" "dist\VexityBot_Ultimate.exe"
) else (
    echo Build failed!
)

pause
