@echo off
echo VexityBot Simple Tkinter Fix Build
echo ==================================
echo Quick build with Tkinter data collection
echo.

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building with Tkinter data collection...
pyinstaller --onefile ^
    --console ^
    --name=VexityBot_Ultimate ^
    --collect-data=tkinter ^
    --collect-submodules=tkinter ^
    --hidden-import=tkinter ^
    --hidden-import=_tkinter ^
    --add-data="pgoapi;pgoapi" ^
    --add-data="pokemongo_bot;pokemongo_bot" ^
    --add-data="BlackScreenTakeover.py;." ^
    --add-data="DeathBot.py;." ^
    --add-data="Enhanced_PokemonGo_Bot.py;." ^
    --add-data="Enhanced_PokemonGo_Bot_Integration.py;." ^
    main_gui.py

echo.
if exist "dist\VexityBot_Ultimate.exe" (
    echo SUCCESS: Build completed!
    echo Location: dist\VexityBot_Ultimate.exe
    echo.
    echo Testing the executable...
    start "" "dist\VexityBot_Ultimate.exe"
) else (
    echo ERROR: Build failed!
)

pause
