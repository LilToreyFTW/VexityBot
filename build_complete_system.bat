@echo off
echo VexityBot Complete System Builder
echo =================================
echo Building VexityBot Ultimate + VPS Server + Client EXE
echo.

echo Step 1: Building VexityBot Ultimate...
call build_auto.bat

echo.
echo Step 2: Building VPS Bot Server...
if not exist "VPS_Bot_Server.py" (
    echo ERROR: VPS_Bot_Server.py not found!
    echo Please ensure all VPS files are present.
    pause
    exit /b 1
)

echo Building VPS Bot Server executable...
python -m PyInstaller ^
    --onefile ^
    --name=VPS_Bot_Server ^
    --add-data="ShadowStrike_OSRS_Bot.py;." ^
    --add-data="osrs_bot_requirements.txt;." ^
    --hidden-import=socket ^
    --hidden-import=json ^
    --hidden-import=threading ^
    --hidden-import=time ^
    --hidden-import=logging ^
    --hidden-import=datetime ^
    --hidden-import=queue ^
    --hidden-import=pickle ^
    --hidden-import=pathlib ^
    VPS_Bot_Server.py

echo.
echo Step 3: Building Client Bot Controller...
if not exist "Client_Bot_Controller.py" (
    echo ERROR: Client_Bot_Controller.py not found!
    echo Please ensure all client files are present.
    pause
    exit /b 1
)

echo Building Client Bot Controller executable...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name=Client_Bot_Controller ^
    --add-data="README.md;." ^
    --add-data="DEPLOYMENT_GUIDE.md;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=socket ^
    --hidden-import=json ^
    --hidden-import=threading ^
    --hidden-import=time ^
    --hidden-import=logging ^
    --hidden-import=datetime ^
    Client_Bot_Controller.py

echo.
echo Step 4: Creating deployment package...
if not exist "deployment" mkdir deployment

echo Copying main executable...
if exist "dist\VexityBot_Ultimate.exe" (
    copy "dist\VexityBot_Ultimate.exe" "deployment\"
    echo ✅ VexityBot_Ultimate.exe copied
) else (
    echo ❌ VexityBot_Ultimate.exe not found!
)

echo Copying VPS server...
if exist "dist\VPS_Bot_Server.exe" (
    copy "dist\VPS_Bot_Server.exe" "deployment\"
    echo ✅ VPS_Bot_Server.exe copied
) else (
    echo ❌ VPS_Bot_Server.exe not found!
)

echo Copying client controller...
if exist "dist\Client_Bot_Controller.exe" (
    copy "dist\Client_Bot_Controller.exe" "deployment\"
    echo ✅ Client_Bot_Controller.exe copied
) else (
    echo ❌ Client_Bot_Controller.exe not found!
)

echo Copying configuration files...
if exist "bot_deployment_config.json" copy "bot_deployment_config.json" "deployment\"
if exist "osrs_bot_requirements.txt" copy "osrs_bot_requirements.txt" "deployment\"
if exist "DEPLOYMENT_GUIDE.md" copy "DEPLOYMENT_GUIDE.md" "deployment\"
if exist "README.md" copy "README.md" "deployment\"

echo Creating VPS setup script...
echo @echo off > "deployment\setup_vps.bat"
echo echo Setting up VPS Bot Server... >> "deployment\setup_vps.bat"
echo echo. >> "deployment\setup_vps.bat"
echo echo Installing Python dependencies... >> "deployment\setup_vps.bat"
echo pip install -r osrs_bot_requirements.txt >> "deployment\setup_vps.bat"
echo echo. >> "deployment\setup_vps.bat"
echo echo Starting VPS Bot Server... >> "deployment\setup_vps.bat"
echo VPS_Bot_Server.exe --host 0.0.0.0 --port 9999 >> "deployment\setup_vps.bat"
echo pause >> "deployment\setup_vps.bat"

echo Creating client setup script...
echo @echo off > "deployment\setup_client.bat"
echo echo VexityBot Client Setup >> "deployment\setup_client.bat"
echo echo ====================== >> "deployment\setup_client.bat"
echo echo. >> "deployment\setup_client.bat"
echo echo 1. Edit config.txt with your VPS IP address >> "deployment\setup_client.bat"
echo echo 2. Run Client_Bot_Controller.exe >> "deployment\setup_client.bat"
echo echo 3. Enter VPS details and connect >> "deployment\setup_client.bat"
echo echo. >> "deployment\setup_client.bat"
echo pause >> "deployment\setup_client.bat"

echo.
echo Step 5: Creating configuration files...
echo # VexityBot Client Configuration > "deployment\config.txt"
echo VPS_IP=YOUR_VPS_IP_HERE >> "deployment\config.txt"
echo VPS_PORT=9999 >> "deployment\config.txt"
echo AUTO_CONNECT=false >> "deployment\config.txt"

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Deployment package created in: deployment\
echo.
echo Files included:
dir deployment\ /b
echo.
echo Next steps:
echo 1. Upload VPS_Bot_Server.exe to your VPS
echo 2. Run setup_vps.bat on VPS to start server
echo 3. Distribute Client_Bot_Controller.exe to users
echo 4. Users can connect and control bots remotely
echo.
echo For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
pause
