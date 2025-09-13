@echo off
echo VexityBot Quick Build
echo ====================

echo Removing problematic packages...
pip uninstall enum34 -y
pip uninstall scapy -y
pip uninstall nmap -y

echo Installing PyInstaller...
pip install pyinstaller

echo Building minimal executable...
python build_minimal.py

echo Build complete!
echo Check VexityBot_Minimal/VexityBot.exe
pause
