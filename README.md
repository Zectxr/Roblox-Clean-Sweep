# Roblox Clean Sweep

Fast, toggleable Roblox removal for Windows and macOS. Use this when you need a truly clean slate (switching accounts, fixing corrupt installs, or prepping a fresh reinstall).

## Why Clean Sweep?
- **Deep removal by default**: processes, folders, registry/preferences, temp/cache, DNS, and stored credentials are all covered.
- **Every step is deliberate**: toggle each Windows action `[+]` run / `[-]` skip so you stay in control.
- **Cross-platform ready**: `cleaner.bat` for Windows, `cleaner.sh` for macOS.

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
- **Processes (critical to stop locks)**: `RobloxPlayerBeta.exe`, `RobloxStudioBeta.exe`, `RobloxCrashHandler.exe`, `RobloxInstaller.exe`.
- **All known folders (no leftovers)**: `%LOCALAPPDATA%`, `%APPDATA%`, `%ProgramFiles%`, `%ProgramFiles(x86)%`, `C:\ProgramData`, `AppData\LocalLow`.
- **Registry footprints (full sweep)**: `HKCU/HKLM Software\Roblox`, WOW6432Node entries.
- **Temp and cache (noise-free)**: `%TEMP%\Roblox*` and `%TEMP%\Roblox` folder.
- **Network hygiene**: DNS cache flush.
- **Account hygiene (optional)**: Roblox-related credentials removed via `cmdkey`.

## What It Cleans (macOS)
- **Processes**: kills Roblox app and related helpers before removal.
- **Folders**: `~/Library/Application Support/Roblox`, `~/Library/Caches/com.roblox.Roblox`, `~/Library/Preferences/com.roblox.Roblox.plist`, `~/Library/Logs/Roblox`, `~/Library/Saved Application State/com.roblox.Roblox.savedState`.
- **System-wide traces (if present)**: `/Library/Application Support/Roblox`, `/Library/Logs/Roblox`.
- **Temp/cache**: `/tmp` Roblox artifacts and cache folders under `~/Library/Caches`.
- **Network hygiene**: optional DNS cache flush (`dscacheutil -flushcache` and `sudo killall -HUP mDNSResponder`).

## Safety & Notes
- Always run as admin on Windows for full cleanup.
- Backup anything important before running; this is meant to remove all Roblox traces.
- Restart after the script completes.

## Contributing
Issues and PRs welcome—especially for adding detections, new paths, or platform tweaks.