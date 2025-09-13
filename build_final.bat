@echo off
echo VexityBot Final Build Script
echo ============================

echo This will remove all problematic packages and build a clean executable.
echo Press any key to continue or Ctrl+C to cancel...
pause

echo.
echo Running clean build...
python build_clean.py

echo.
echo Build process completed!
echo Check VexityBot_Final/VexityBot.exe
pause
