@echo off
echo Starting VPS Bot Server...
echo ==========================
echo.
echo This will start the VPS Bot Server on localhost:9999
echo Press Ctrl+C to stop the server
echo.

python VPS_Bot_Server.py --host 127.0.0.1 --port 9999

pause
