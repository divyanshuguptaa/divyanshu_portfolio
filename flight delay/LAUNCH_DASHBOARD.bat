@echo off
cd /d "%~dp0"
cls
color 0B

echo.
echo ================================================================================
echo.
echo                   FLIGHT DELAY DASHBOARD 2024
echo.
echo ================================================================================
echo.
echo  Starting dashboard on http://localhost:8001
echo.
echo  Please wait 5-10 seconds for initialization...
echo.
echo ================================================================================
echo.
echo  Once you see "Dash is running on http://127.0.0.1:8001"
echo.
echo  Open your browser and go to:
echo.
echo      http://localhost:8001
echo.
echo ================================================================================
echo.
echo  Press Ctrl+C to stop the dashboard when done.
echo.
echo ================================================================================
echo.

python flight_delay_dashboard.py

echo.
echo ================================================================================
echo  Dashboard stopped.
echo ================================================================================
pause

