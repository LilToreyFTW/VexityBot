@echo off
title VexityBot - Advanced Bot Management System
color 0A

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

echo Starting VexityBot GUI...
dist\VexityBot.exe

if errorlevel 1 (
    echo.
    echo Error starting VexityBot!
    echo Please check that all files are present.
    pause
)
