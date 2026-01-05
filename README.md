# Roblox Clean Sweep

<div align="center">

![Roblox Clean Sweep Banner](https://img.shields.io/badge/Roblox-Clean%20Sweep-111827?style=for-the-badge&logo=windows&logoColor=white)

![Windows](https://img.shields.io/badge/Windows-10%2F11-2563eb?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-Intel%20%26%20Apple%20Silicon-0ea5e9?style=for-the-badge&logo=apple&logoColor=white)
![Shell](https://img.shields.io/badge/Scripts-Batch%20%7C%20Bash-10b981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)

<sub>Clean installs, fast resets, zero leftovers.</sub>

</div>

Fast, toggleable Roblox removal for Windows and macOS. Use this when you need a truly clean slate (switching accounts, fixing corrupt installs, or prepping a fresh reinstall).

## Why Clean Sweep?
- **Deep removal by default**: processes, folders, registry/preferences, temp/cache, DNS, and stored credentials are all covered.
- **Every step is deliberate**: toggle each Windows action `[+]` run / `[-]` skip so you stay in control.
- **Cross-platform ready**: `cleaner.bat` for Windows, `cleaner.sh` for macOS.
- **Single-pass flow**: one run takes you from detection to cleanup, then restart.
- **Forensic-friendly**: documents exactly what is removed for auditability.

## Feature Snapshot
- One-run cleanup with user-controlled toggles on Windows.
- Mirrors best-practice locations on macOS (user and system scopes).
- Targets credentials (Windows) and DNS cache hygiene on both platforms.
- Designed for reinstall prep, account switching, or remediation after issues.

## Table of Contents
- [Quick Start](#quick-start)
- [What It Cleans (Windows)](#what-it-cleans-windows)
- [What It Cleans (macos)](#what-it-cleans-macos)
- [Safety & Notes](#safety--notes)
- [Contributing](#contributing)
- [Inspiration](#inspiration)

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
- Scripts are text-based; review before running if you need to audit.

## Contributing
Issues and PRs welcome—especially for adding detections, new paths, or platform tweaks.

## Inspiration
- Clean, auditable resets for players and creators.
- Fast troubleshooting when reinstalling or switching accounts.
- Reduce support noise by ensuring no leftover state remains.