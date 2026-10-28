@echo off
title Robotics Components ERP - Desktop GUI Launcher
echo ===================================================
echo   Launching Robotics Laboratory Desktop GUI (PyQt6)
echo ===================================================
echo.

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Using Python Launcher (py)...
    py main.py
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Using python...
    python main.py
    goto end
)

echo [!] Python was not found in PATH.
pause

:end
