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
echo.
echo Press any key to continue...
pause >nul

:: ================================
:: KILL ROBLOX PROCESSES
:: ================================
echo Killing Roblox processes...
taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1
taskkill /F /IM RobloxStudioBeta.exe >nul 2>&1
taskkill /F /IM RobloxCrashHandler.exe >nul 2>&1
taskkill /F /IM RobloxInstaller.exe >nul 2>&1
echo Done.

:: ================================
:: DELETE FOLDERS
:: ================================
echo Deleting leftover folders...
if exist "%LOCALAPPDATA%\Roblox" (
    rmdir /S /Q "%LOCALAPPDATA%\Roblox" >nul 2>&1
    echo Deleted %LOCALAPPDATA%\Roblox
)
if exist "%APPDATA%\Roblox" (
    rmdir /S /Q "%APPDATA%\Roblox" >nul 2>&1
    echo Deleted %APPDATA%\Roblox
)
if exist "%ProgramFiles%\Roblox" (
    rmdir /S /Q "%ProgramFiles%\Roblox" >nul 2>&1
    echo Deleted %ProgramFiles%\Roblox
)
if exist "%ProgramFiles(x86)%\Roblox" (
    rmdir /S /Q "%ProgramFiles(x86)%\Roblox" >nul 2>&1
    echo Deleted %ProgramFiles(x86)%\Roblox
)
if exist "C:\ProgramData\Roblox" (
    rmdir /S /Q "C:\ProgramData\Roblox" >nul 2>&1
    echo Deleted C:\ProgramData\Roblox
)
if exist "%USERPROFILE%\AppData\LocalLow\Roblox" (
    rmdir /S /Q "%USERPROFILE%\AppData\LocalLow\Roblox" >nul 2>&1
    echo Deleted %USERPROFILE%\AppData\LocalLow\Roblox
)
echo Folder cleanup complete.

:: ================================
:: REGISTRY CLEANUP
:: ================================
echo Removing registry entries...
reg delete "HKCU\Software\Roblox" /f >nul 2>&1
if %errorlevel% equ 0 echo Deleted HKCU\Software\Roblox
reg delete "HKLM\Software\Roblox" /f >nul 2>&1
if %errorlevel% equ 0 echo Deleted HKLM\Software\Roblox
reg delete "HKLM\Software\WOW6432Node\Roblox" /f >nul 2>&1
if %errorlevel% equ 0 echo Deleted HKLM\Software\WOW6432Node\Roblox
echo Registry cleanup complete.

:: ================================
:: CACHE + TEMP CLEANUP
:: ================================
echo Cleaning temp files...
del /F /Q "%TEMP%\Roblox*.*" >nul 2>&1
if exist "%TEMP%\Roblox" rmdir /S /Q "%TEMP%\Roblox" >nul 2>&1
echo Temp cleanup complete.

:: ================================
:: NETWORK CLEAN (OPTIONAL BUT GOOD)
:: ================================
echo Flushing DNS cache...
ipconfig /flushdns >nul
echo DNS cache flushed.

echo.
echo === CLEANUP COMPLETE ===
echo Restart your PC before reinstalling Roblox.
echo.
echo Press any key to exit...
pause >nul
