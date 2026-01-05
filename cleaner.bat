@echo off
title Roblox Full Cleanup Tool
color 0A
setlocal enabledelayedexpansion

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

echo.
echo Configure steps ([+]=run, [-]=skip):
call :ask "Kill Roblox processes" CLEAN_KILL
call :ask "Delete Roblox folders" CLEAN_FOLDERS
call :ask "Registry cleanup" CLEAN_REG
call :ask "Temp/cache cleanup" CLEAN_TEMP
call :ask "Flush DNS cache" CLEAN_DNS
call :ask "Delete Roblox credentials" CLEAN_CREDS
echo.

:: ================================
:: KILL ROBLOX PROCESSES
:: ================================
if "%CLEAN_KILL%"=="Y" (
    echo Killing Roblox processes... [+]
    taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1
    taskkill /F /IM RobloxStudioBeta.exe >nul 2>&1
    taskkill /F /IM RobloxCrashHandler.exe >nul 2>&1
    taskkill /F /IM RobloxInstaller.exe >nul 2>&1
    echo Done.
) else (
    echo Skipped killing Roblox processes [-]
)

:: ================================
:: DELETE FOLDERS
:: ================================
if "%CLEAN_FOLDERS%"=="Y" (
    echo Deleting leftover folders... [+]
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
) else (
    echo Skipped folder cleanup [-]
)

:: ================================
:: REGISTRY CLEANUP
:: ================================
if "%CLEAN_REG%"=="Y" (
    echo Removing registry entries... [+]
    reg delete "HKCU\Software\Roblox" /f >nul 2>&1
    if %errorlevel% equ 0 echo Deleted HKCU\Software\Roblox
    reg delete "HKLM\Software\Roblox" /f >nul 2>&1
    if %errorlevel% equ 0 echo Deleted HKLM\Software\Roblox
    reg delete "HKLM\Software\WOW6432Node\Roblox" /f >nul 2>&1
    if %errorlevel% equ 0 echo Deleted HKLM\Software\WOW6432Node\Roblox
    echo Registry cleanup complete.
) else (
    echo Skipped registry cleanup [-]
)

:: ================================
:: CACHE + TEMP CLEANUP
:: ================================
if "%CLEAN_TEMP%"=="Y" (
    echo Cleaning temp files... [+]
    del /F /Q "%TEMP%\Roblox*.*" >nul 2>&1
    if exist "%TEMP%\Roblox" rmdir /S /Q "%TEMP%\Roblox" >nul 2>&1
    echo Temp cleanup complete.
) else (
    echo Skipped temp cleanup [-]
)

:: ================================
:: NETWORK CLEAN (OPTIONAL BUT GOOD)
:: ================================
if "%CLEAN_DNS%"=="Y" (
    echo Flushing DNS cache... [+]
    ipconfig /flushdns >nul
    echo DNS cache flushed.
) else (
    echo Skipped DNS flush [-]
)

:: ================================
:: DELETE ROBLOX CREDENTIALS
:: ================================
if "%CLEAN_CREDS%"=="Y" (
    echo Deleting Roblox-related Windows credentials... [+]
    for /f "tokens=*" %%i in ('cmdkey /list ^| findstr /i "roblox"') do (
        set "target=%%i"
        set "target=!target:Target: =!"
        cmdkey /delete:"!target!" >nul 2>&1
    )
    echo Credentials cleanup complete.
) else (
    echo Skipped credential cleanup [-]
)

echo.
echo === CLEANUP COMPLETE ===
echo Restart your PC before reinstalling Roblox.
echo.
echo Press any key to exit...
pause >nul

goto :eof

:ask
setlocal
set "msg=%~1"
set "var=%~2"
choice /C YN /N /M "%msg% [+]=Y [-]=N (Y/N)? "
if errorlevel 2 (set "ans=N") else (set "ans=Y")
endlocal & set "%var%=%ans%"
exit /b
