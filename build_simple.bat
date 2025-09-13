@echo off
echo VexityBot Simple Build Script
echo =============================

echo Removing enum34 package...
pip uninstall enum34 -y

echo Installing basic dependencies...
pip install requests pyinstaller

echo Building executable...
python build_fixed.py

echo Build complete!
echo Check dist/VexityBot.exe
pause
