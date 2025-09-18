@echo off
echo VexityBot Ultimate Tkinter Fixed Build Script v2
echo ================================================
echo Building VexityBot with comprehensive Tkinter fixes
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
echo Building VexityBot Ultimate with comprehensive Tkinter support...
pyinstaller --onefile ^
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
    --add-data="Standalone_PokemonGo_Bot.py;." ^
    --add-data="PokemonGo_Bot_pgoapi_Integration.py;." ^
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
    --hidden-import=_tkinter ^
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
    --collect-data=tkinter ^
    --collect-submodules=tkinter ^
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
    echo - Enhanced Pokemon Go Bot with pgoapi
    echo - DeathBot with black screen takeover
    echo - VPS Bot Controller for remote control
    echo - GameBots with ShadowStrike OSRS automation
    echo - Steganography tools
    echo - Database management and data analysis
    echo - AI management and bot control
    echo - Tkinter data files properly collected
    echo - All Tkinter submodules included
    echo.
    echo Build completed successfully!
    echo.
    echo Next steps:
    echo 1. Test the executable: dist\VexityBot_Ultimate.exe
    echo 2. The Tkinter data directory issue should be resolved
    echo 3. All Pokemon Go bot features should work
    echo.
    echo Testing the executable...
    echo Running: dist\VexityBot_Ultimate.exe
    echo.
    timeout /t 3 /nobreak >nul
    start "" "dist\VexityBot_Ultimate.exe"
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
    echo - Tkinter data directory not found
    echo.
)

echo.
echo Build process completed!
pause
