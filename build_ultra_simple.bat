@echo off
echo VexityBot Ultra Simple Build
echo ============================

echo Building ultra simple executable...
python -m PyInstaller --onefile --windowed --name=VexityBot main_ultra_simple.py

echo.
if exist "dist\VexityBot.exe" (
    echo SUCCESS! VexityBot.exe created!
    echo Location: dist\VexityBot.exe
) else (
    echo FAILED! Check for errors above.
)

pause
