@echo off
echo VexityBot Ultimate Auto Build Script
echo ====================================
echo Building VexityBot with VPS Bot Controller and GameBots
echo.

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "VexityBot.spec" del "VexityBot.spec"
if exist "*.spec" del "*.spec"

echo.
echo Installing required dependencies...
pip install pyinstaller pillow psutil

echo.
echo Building VexityBot Ultimate executable...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name=VexityBot_Ultimate ^
    --icon=icon.ico ^
    --add-data="README.md;." ^
    --add-data="DEPLOYMENT_GUIDE.md;." ^
    --add-data="bot_deployment_config.json;." ^
    --add-data="osrs_bot_requirements.txt;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=socket ^
    --hidden-import=json ^
    --hidden-import=threading ^
    --hidden-import=time ^
    --hidden-import=logging ^
    --hidden-import=datetime ^
    --hidden-import=random ^
    --hidden-import=subprocess ^
    --hidden-import=os ^
    --hidden-import=sys ^
    --hidden-import=pathlib ^
    --exclude-module=dnspython ^
    --exclude-module=scapy ^
    --exclude-module=nmap ^
    --exclude-module=cryptography ^
    --exclude-module=requests ^
    --exclude-module=tensorflow ^
    --exclude-module=opencv-python ^
    --exclude-module=pyautogui ^
    main_gui.py

echo.
echo Checking if build was successful...
if exist "dist\VexityBot_Ultimate.exe" (
    echo.
    echo ========================================
    echo SUCCESS: VexityBot Ultimate created!
    echo ========================================
    echo Location: dist\VexityBot_Ultimate.exe
    echo.
    echo File size:
    dir "dist\VexityBot_Ultimate.exe" | findstr "VexityBot_Ultimate.exe"
    echo.
    echo Features included:
    echo - Main VexityBot GUI with all tabs
    echo - VPS Bot Controller for remote OSRS bot control
    echo - GameBots with ShadowStrike OSRS automation
    echo - Steganography tools
    echo - Bomb creation and EXE building
    echo - Database management and data analysis
    echo - AI management and bot control
    echo - Screens and victim EXE creation
    echo.
    echo Build completed successfully!
    echo.
    echo Next steps:
    echo 1. Test the executable: dist\VexityBot_Ultimate.exe
    echo 2. Deploy VPS server files to your VPS
    echo 3. Use VPS Bot Controller tab to connect and control bots
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo VexityBot_Ultimate.exe not found.
    echo Check the error messages above.
    echo.
    echo Common issues:
    echo - Missing dependencies
    echo - Python path issues
    echo - File permission problems
    echo.
)

echo.
echo Build process completed!
pause
