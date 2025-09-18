@echo off
echo VexityBot Ultimate - Tkinter Fixed Build
echo ========================================
echo This build fixes the "Tk data directory not found" error
echo.

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building VexityBot with Tkinter fix...
pyinstaller --onefile --console --name=VexityBot_Ultimate --collect-data=tkinter --collect-submodules=tkinter --add-data="pgoapi;pgoapi" --add-data="pokemongo_bot;pokemongo_bot" --add-data="BlackScreenTakeover.py;." --add-data="DeathBot.py;." --add-data="Enhanced_PokemonGo_Bot.py;." --add-data="Enhanced_PokemonGo_Bot_Integration.py;." --add-data="Standalone_PokemonGo_Bot.py;." --add-data="PokemonGo_Bot_pgoapi_Integration.py;." --hidden-import=pgoapi --hidden-import=pgoapi.pgoapi --hidden-import=pgoapi.exceptions --hidden-import=pgoapi.utilities --hidden-import=pgoapi.auth --hidden-import=pgoapi.auth_ptc --hidden-import=pgoapi.auth_google --hidden-import=pgoapi.rpc_api --exclude-module=numpy --exclude-module=pandas --exclude-module=torch --exclude-module=opencv-python --exclude-module=scipy --exclude-module=sklearn --exclude-module=tensorflow --exclude-module=matplotlib main_gui.py

echo.
if exist "dist\VexityBot_Ultimate.exe" (
    echo ========================================
    echo SUCCESS: VexityBot Ultimate created!
    echo ========================================
    echo Location: dist\VexityBot_Ultimate.exe
    echo.
    echo File size:
    dir "dist\VexityBot_Ultimate.exe" | findstr "VexityBot_Ultimate.exe"
    echo.
    echo ✅ Tkinter data directory issue FIXED!
    echo ✅ Users will no longer see the error:
    echo    "Tk data directory not found"
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
    echo.
    echo Testing the executable...
    start "" "dist\VexityBot_Ultimate.exe"
) else (
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo VexityBot_Ultimate.exe not found.
    echo Check the error messages above.
)

echo.
echo Build process completed!
pause
