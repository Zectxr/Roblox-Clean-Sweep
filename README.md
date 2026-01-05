# Roblox Clean Sweep

Fast, toggleable Roblox removal for Windows and macOS. Use this when you need a truly clean slate (switching accounts, fixing corrupt installs, or prepping a fresh reinstall).

## Why Clean Sweep?
- Thorough: removes processes, folders, registry/preferences, temp/cache, DNS, and (optional) stored credentials.
- Toggle-friendly: each Windows step can be enabled `[+]` or skipped `[-]` interactively.
- Cross-platform: `cleaner.bat` for Windows, `cleaner.sh` for macOS.

## Quick Start

### Windows (`cleaner.bat`)
1) **Run as Administrator** (right-click → Run as administrator).
2) **Answer toggles**: `[+]` to run a step, `[-]` to skip.
3) Let it finish, then **restart** before reinstalling Roblox.

### macOS (`cleaner.sh`)
```bash
chmod +x cleaner.sh
sudo ./cleaner.sh
```
Follow prompts, then restart.

## What It Cleans (Windows)
- Processes: `RobloxPlayerBeta.exe`, `RobloxStudioBeta.exe`, `RobloxCrashHandler.exe`, `RobloxInstaller.exe`.
- Folders: `%LOCALAPPDATA%`, `%APPDATA%`, `%ProgramFiles%`, `%ProgramFiles(x86)%`, `C:\ProgramData`, `AppData\LocalLow` (Roblox paths).
- Registry: `HKCU/HKLM Software\Roblox`, WOW6432Node entries.
- Temp & cache: `%TEMP%\Roblox*` and `%TEMP%\Roblox` folder.
- DNS cache flush.
- Optional: Roblox-related credentials via `cmdkey`.

## Safety & Notes
- Always run as admin on Windows for full cleanup.
- Backup anything important before running; this is meant to remove all Roblox traces.
- Restart after the script completes.

## Contributing
Issues and PRs welcome—especially for adding detections, new paths, or platform tweaks.