@echo off
REM P2P File Sharing Application - Launcher Script

echo ================================================
echo P2P File Sharing Application
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run the application
echo Starting P2P File Sharing Application...
echo.
python ui/main_app.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the application
    pause
    exit /b 1
)
