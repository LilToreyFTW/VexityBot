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
    --console ^
    --name=VexityBot_Ultimate ^
    --distpath=dist ^
    --workpath=build ^
    --specpath=. ^
    --clean ^
    --noconfirm ^
    --add-data="README.md;." ^
    --add-data="DEPLOYMENT_GUIDE.md;." ^
    --add-data="bot_deployment_config.json;." ^
    --add-data="osrs_bot_requirements.txt;." ^
    --add-data="pgoapi;pgoapi" ^
    --add-data="pokemongo_bot;pokemongo_bot" ^
    --add-data="BlackScreenTakeover.py;." ^
    --add-data="DeathBot.py;." ^
    --add-data="Enhanced_PokemonGo_Bot.py;." ^
    --add-data="Enhanced_PokemonGo_Bot_Integration.py;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.constants ^
    --hidden-import=tkinter.dnd ^
    --hidden-import=tkinter.colorchooser ^
    --hidden-import=tkinter.commondialog ^
    --hidden-import=tkinter.simpledialog ^
    --hidden-import=tkinter.font ^
    --hidden-import=tkinter.dialog ^
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
    --hidden-import=queue ^
    --hidden-import=pickle ^
    --hidden-import=asyncio ^
    --hidden-import=typing ^
    --hidden-import=pgoapi ^
    --hidden-import=pgoapi.pgoapi ^
    --hidden-import=pgoapi.exceptions ^
    --hidden-import=pgoapi.utilities ^
    --hidden-import=pgoapi.auth ^
    --hidden-import=pgoapi.auth_ptc ^
    --hidden-import=pgoapi.auth_google ^
    --hidden-import=pgoapi.rpc_api ^
    --collect-all=tkinter ^
    --collect-all=tkinter.ttk ^
    --collect-all=tkinter.messagebox ^
    --collect-all=tkinter.scrolledtext ^
    --collect-all=tkinter.filedialog ^
    --collect-all=pgoapi ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    --exclude-module=sklearn ^
    --exclude-module=tensorflow ^
    --exclude-module=torch ^
    --exclude-module=opencv-python ^
    --exclude-module=pyautogui ^
    --exclude-module=requests ^
    --exclude-module=urllib3 ^
    --exclude-module=cryptography ^
    --exclude-module=dnspython ^
    --exclude-module=scapy ^
    --exclude-module=nmap ^
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
