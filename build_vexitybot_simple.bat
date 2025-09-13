@echo off
echo Building VexityBot with Pokemon Integration...
echo ===========================================

echo Checking Python...
python --version
if errorlevel 1 (
    echo Python not found!
    pause
    exit /b 1
)

echo.
echo Installing PyInstaller if needed...
pip install pyinstaller

echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "VexityBot.spec" del "VexityBot.spec"

echo.
echo Building VexityBot.exe...
pyinstaller --onefile --windowed --name=VexityBot --add-data="data;data" --add-data="config;config" --add-data="imagecoded;imagecoded" --hidden-import=PokemonDataManager --hidden-import=Thunderbolt_PokemonGO_Bot --hidden-import=VexityBotSteganography --hidden-import=VexityBotSteganographyGUI main_gui_only.py

echo.
if exist "dist\VexityBot.exe" (
    echo SUCCESS! VexityBot.exe created!
    echo Location: %CD%\dist\VexityBot.exe
    echo.
    echo Testing launch...
    start "" "dist\VexityBot.exe"
) else (
    echo BUILD FAILED!
    echo Check error messages above.
)

echo.
pause
