
@echo off
echo VexityBot Installer
echo ===================

echo Creating VexityBot directory...
mkdir "C:\VexityBot" 2>nul

echo Copying files...
copy "dist\VexityBot.exe" "C:\VexityBot\"
copy "main_gui.py" "C:\VexityBot\"
copy "VexityBotCore.py" "C:\VexityBot\"
copy "VexityBotNetworking.py" "C:\VexityBot\"
copy "VexityBotJavaFX.java" "C:\VexityBot\"
copy "VexityBotCpp.h" "C:\VexityBot\"
copy "VexityBotCpp.cpp" "C:\VexityBot\"
copy "VexityBotCSharp.cs" "C:\VexityBot\"
copy "requirements.txt" "C:\VexityBot\"

echo Creating desktop shortcut...
echo [InternetShortcut] > "%USERPROFILE%\Desktop\VexityBot.url"
echo URL=file:///C:/VexityBot/VexityBot.exe >> "%USERPROFILE%\Desktop\VexityBot.url"
echo IconFile=C:\VexityBot\VexityBot.exe >> "%USERPROFILE%\Desktop\VexityBot.url"
echo IconIndex=0 >> "%USERPROFILE%\Desktop\VexityBot.url"

echo Installation complete!
echo VexityBot has been installed to C:\VexityBot
echo Desktop shortcut created.
pause
