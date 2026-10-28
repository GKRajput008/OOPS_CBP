@echo off
title Robotics Components ERP - C++ Console Launcher
echo ========================================================
echo   Robotics Laboratory Inventory System (C++ OOPS CBP)
echo ========================================================
echo.

if exist main.exe (
    echo Launching main.exe...
    main.exe
    goto end
)

echo [i] Compiling main.cpp with g++...
C:\msys64\ucrt64\bin\g++.exe -std=c++17 -Wall main.cpp -o main.exe
if %ERRORLEVEL% equ 0 (
    echo [OK] Compiled successfully. Starting...
    main.exe
) else (
    echo [!] Compilation failed. Please ensure g++ is installed.
    pause
)

:end
