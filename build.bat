@echo off
echo VexityBot Build Script
echo ======================

echo Installing dependencies...
pip install -r requirements.txt

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
python build_exe.py

echo Build complete!
echo Check dist/VexityBot.exe
pause
