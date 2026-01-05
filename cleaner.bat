@echo off
title Roblox Full Cleanup Tool
color 0A

:: ================================
:: ADMIN CHECK
:: ================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Run this file as ADMINISTRATOR.
    pause
    exit /b
)

echo === Roblox Uninstall Helper ===
echo This will remove Roblox files, folders, cache, and registry entries.
echo Make sure Roblox is already uninstalled.
pause

:: ================================
:: KILL ROBLOX PROCESSES
:: ================================
echo Killing Roblox processes...
taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1
taskkill /F /IM RobloxStudioBeta.exe >nul 2>&1
taskkill /F /IM RobloxCrashHandler.exe >nul 2>&1

:: ================================
:: DELETE FOLDERS
:: ================================
echo Deleting leftover folders...
rmdir /S /Q "%LOCALAPPDATA%\Roblox" >nul 2>&1
rmdir /S /Q "%APPDATA%\Roblox" >nul 2>&1
rmdir /S /Q "%ProgramFiles%\Roblox" >nul 2>&1
rmdir /S /Q "%ProgramFiles(x86)%\Roblox" >nul 2>&1
rmdir /S /Q "C:\ProgramData\Roblox" >nul 2>&1

:: ================================
:: REGISTRY CLEANUP
:: ================================
echo Removing registry entries...
reg delete "HKCU\Software\Roblox" /f >nul 2>&1
reg delete "HKLM\Software\Roblox" /f >nul 2>&1
reg delete "HKLM\Software\WOW6432Node\Roblox" /f >nul 2>&1

:: ================================
:: CACHE + TEMP CLEANUP
:: ================================
echo Cleaning temp files...
del /F /Q "%TEMP%\Roblox*.*" >nul 2>&1
rmdir /S /Q "%TEMP%\Roblox" >nul 2>&1

:: ================================
:: NETWORK CLEAN (OPTIONAL BUT GOOD)
:: ================================
echo Flushing DNS cache...
ipconfig /flushdns >nul

echo.
echo === CLEANUP COMPLETE ===
echo Restart your PC before reinstalling Roblox.
pause
