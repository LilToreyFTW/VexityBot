@echo off
echo VexityBot Complete Build Script
echo ===============================

echo.
echo  ██╗   ██╗███████╗██╗  ██╗██╗████████╗██╗   ██╗██████╗  ██████╗ ████████╗
echo  ██║   ██║██╔════╝╚██╗██╔╝██║╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
echo  ██║   ██║█████╗   ╚███╔╝ ██║   ██║    ╚████╔╝ ██████╔╝██║   ██║   ██║   
echo  ╚██╗ ██╔╝██╔══╝   ██╔██╗ ██║   ██║     ╚██╔╝  ██╔══██╗██║   ██║   ██║   
echo   ╚████╔╝ ███████╗██╔╝ ██╗██║   ██║      ██║   ██████╔╝╚██████╔╝   ██║   
echo    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   
echo.
echo                    Advanced Bot Management System v2.0.0
echo.

echo [1/6] Setting up environment...
python setup.py

echo.
echo [2/6] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [3/6] Creating build directories...
if not exist "dist" mkdir dist
if not exist "build" mkdir build

echo.
echo [4/6] Building executable...
python build_exe.py

echo.
echo [5/6] Creating installer package...
if not exist "VexityBot_Package" mkdir VexityBot_Package
copy "dist\VexityBot.exe" "VexityBot_Package\"
copy "main_gui.py" "VexityBot_Package\"
copy "VexityBotCore.py" "VexityBot_Package\"
copy "VexityBotNetworking.py" "VexityBot_Package\"
copy "VexityBotJavaFX.java" "VexityBot_Package\"
copy "VexityBotCpp.h" "VexityBot_Package\"
copy "VexityBotCpp.cpp" "VexityBot_Package\"
copy "VexityBotCSharp.cs" "VexityBot_Package\"
copy "requirements.txt" "VexityBot_Package\"
copy "README.md" "VexityBot_Package\"
copy "install.bat" "VexityBot_Package\"
copy "launcher.bat" "VexityBot_Package\"
copy "VexityBot.url" "VexityBot_Package\"
xcopy "config" "VexityBot_Package\config\" /E /I
xcopy "logs" "VexityBot_Package\logs\" /E /I

echo.
echo [6/6] Creating final package...
cd VexityBot_Package
powershell Compress-Archive -Path * -DestinationPath ..\VexityBot_v2.0.0.zip
cd ..

echo.
echo ================================
echo Build completed successfully!
echo ================================
echo.
echo Files created:
echo - dist\VexityBot.exe (standalone executable)
echo - VexityBot_Package\ (complete package)
echo - VexityBot_v2.0.0.zip (distribution package)
echo.
echo To install VexityBot:
echo 1. Extract VexityBot_v2.0.0.zip
echo 2. Run install.bat as administrator
echo.
echo To run VexityBot:
echo 1. Double-click VexityBot.exe
echo 2. Or run launcher.bat
echo.
pause
