# Roblox Clean Sweep

<div align="center">

![Roblox Clean Sweep Banner](https://img.shields.io/badge/Roblox-Clean%20Sweep-111827?style=for-the-badge&logo=windows&logoColor=white)

![Windows](https://img.shields.io/badge/Windows-10%2F11-2563eb?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-Intel%20%26%20Apple%20Silicon-0ea5e9?style=for-the-badge&logo=apple&logoColor=white)
![Shell](https://img.shields.io/badge/Scripts-Batch%20%7C%20Python-10b981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)

<sub>Clean installs, fast resets, zero leftovers.</sub>

</div>

Fast, toggleable Roblox removal for Windows and macOS. Use this when you need a truly clean slate (switching accounts, fixing corrupt installs, or prepping a fresh reinstall).

## Why Clean Sweep?
- **Deep removal by default**: processes, folders, registry/preferences, temp/cache, DNS, and stored credentials are all covered.
- **Every step is deliberate**: toggle each step `[+]` run / `[-]` skip so you stay in control.
- **Cross-platform ready**: `run.bat` for Windows, `cleaner.py` for Windows/macOS.
- **Single-pass flow**: one run takes you from detection to cleanup, then restart.
- **Forensic-friendly**: documents exactly what is removed for auditability.

### What’s New (latest)
- Windows Store/UWP Roblox removal using `Get-AppxPackage ... | Remove-AppxPackage`.
- MAC address tools (Windows): list adapters, randomize/set custom MAC, revert to original.
- Extra sweep: deletes Roblox shortcuts, prefetch files, crash dumps, and “Recent” items.
- Network hygiene: removes Roblox-named firewall rules, scheduled tasks, and hosts entries.
- Color-coded output: green = removed, yellow = not found, red = error, cyan = info.
- Cleaner header banner and clearer exit options.

## Feature Snapshot
- Interactive toggle menu with user-controlled steps.
- Windows-only MAC tools (PowerShell + registry) to spoof/revert adapter MACs.
- Mirrors best-practice locations on macOS (user and system scopes).
- Targets credentials (Windows) and DNS cache hygiene on both platforms.
- Designed for reinstall prep, account switching, or remediation after issues.
- **No external dependencies** for Python version (uses standard library only).

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [What It Cleans (Windows)](#what-it-cleans-windows)
- [What It Cleans (macOS)](#what-it-cleans-macos)
- [Safety & Notes](#safety--notes)
- [Contributing](#contributing)
- [Inspiration](#inspiration)

## Installation

### Option 1: Python Version (Recommended)

**Requirements:**
- Python 3.7 or higher

**Install Python (if not already installed):**
- **Windows**: Download from [python.org](https://www.python.org/downloads/) or use `winget`:
  ```powershell
  winget install Python.Python.3.12
  ```
- **macOS**: Use Homebrew:
  ```bash
  brew install python3
  ```

**Install dependencies (none required, but to verify):**
```bash
pip install -r requirements.txt
```

### Option 2: Batch Script (Windows Only)

**Requirements:**
- Windows 10/11
- Administrator access
- No additional software needed

---

## Quick Start

### Python Version (`cleaner.py`)

**Windows:**
```powershell
cd "C:\Users\YourUsername\Desktop\Roblox Clean Sweep"
python cleaner.py
```

**macOS/Linux:**
```bash
cd ~/Desktop/Roblox\ Clean\ Sweep
python3 cleaner.py
```

Or make it executable:
```bash
chmod +x cleaner.py
./cleaner.py
```

### Batch Script (`run.bat`)

1. **Right-click** `run.bat` → **Run as administrator**
2. **Select mode**: 
  - `1` = Run everything (all [+])
  - `2` = Configure steps individually
  - `3` = MAC address tools (Windows)
  - `4` = About steps (what they do)
  - `0` = Exit
3. **Answer toggles** (if mode 2): enter number to toggle `[+]/[-]` status
4. **Review** and confirm cleanup
5. **Restart** your PC before reinstalling Roblox

---

## What It Cleans (Windows)
- **Processes (critical to stop locks)**: `RobloxPlayerBeta.exe`, `RobloxStudioBeta.exe`, `RobloxCrashHandler.exe`, `RobloxInstaller.exe`.
- **Folders & shortcuts**: `%LOCALAPPDATA%\Roblox`, `%APPDATA%\Roblox`, `%ProgramFiles%\Roblox`, `%ProgramFiles(x86)%\Roblox`, `C:\ProgramData\Roblox`, `%USERPROFILE%\AppData\LocalLow\Roblox`, plus desktop/start-menu/quick-launch shortcuts.
- **Registry & uninstall entries**: `HKCU/HKLM Software\Roblox`, WOW6432Node keys, uninstall entries, and protocol handlers (`roblox-player`, `roblox-player-1`).
- **Microsoft Store/UWP package**: removes `ROBLOXCORPORATION*` Appx package if present.
- **Temp, Prefetch, Crash dumps, Recent**: `%TEMP%\Roblox*`, `C:\Windows\Prefetch\ROBLOX*.pf`, `%LOCALAPPDATA%\CrashDumps\Roblox*.dmp`, and Recent items containing “roblox”.
- **Network hygiene**: flush DNS; remove Roblox-named firewall rules and scheduled tasks; strip “roblox” lines from the Windows hosts file.
- **Credentials**: deletes Windows Credential Manager entries that match Roblox.

## What It Cleans (macOS)
- **Processes**: kills Roblox app and related helpers before removal.
- **Folders**: `~/Library/Application Support/Roblox`, `~/Library/Caches/com.roblox.Roblox`, `~/Library/Preferences/com.roblox.Roblox.plist`, `~/Library/Logs/Roblox`, `~/Library/Saved Application State/com.roblox.Roblox.savedState`.
- **System-wide traces (if present)**: `/Library/Application Support/Roblox`, `/Library/Logs/Roblox`.
- **Temp/cache**: `/tmp` Roblox artifacts and cache folders under `~/Library/Caches`.
- **Network hygiene**: optional DNS cache flush (`dscacheutil -flushcache` and `sudo killall -HUP mDNSResponder`).

## Safety & Notes
- Always run as admin (Windows) or with `sudo` (macOS) for full cleanup.
- Backup anything important before running; this is meant to remove all Roblox traces.
- Restart after the script completes.
- Scripts are text-based; review before running if you need to audit.
- Both Python and Batch versions will show warnings for skipped/failed operations and continue instead of crashing.

### MAC Tools Safety
- MAC spoofing is Windows-only and requires admin. Some NIC drivers/brands may ignore `NetworkAddress` overrides or reset them after updates.
- Connectivity can briefly drop while the adapter is disabled/enabled to apply the change.
- You can revert any override via the MAC tools menu (option “Revert to original”).

### Hosts and Firewall
- The script removes hosts entries that contain “roblox” (case-insensitive). If you rely on custom host mappings, review before/after.
- Firewall rules and scheduled tasks with “Roblox” in their name are deleted.

## Usage Examples

### Windows - Python (Quick Run All)
```powershell
python cleaner.py
# Select: 1
```

### Windows - Batch (Configure Steps)
```cmd
run.bat
# Select: 2
# Toggle steps as needed
# Select: S to start
```

### macOS - Python (Configure Steps)
```bash
python3 cleaner.py
# Select: 2
# Toggle steps as needed (A for all, S to start)
```

### Windows - MAC Address Tools
```powershell
python cleaner.py
# Select: 3 (MAC address tools)
# Pick adapter → choose:
#  1) Randomize MAC
#  2) Set custom MAC (12 hex chars, no colons)
#  3) Revert to original
```

Color legend in output:
- Green = removed/updated successfully
- Yellow = item not found (already clean)
- Red = error (operation failed)
- Cyan = informational

## Contributing
Issues and PRs welcome—especially for:
- Adding detections for new Roblox paths
- Platform-specific tweaks
- Bug reports or stability improvements
- Documentation improvements

## Inspiration
- Clean, auditable resets for players and creators.
- Fast troubleshooting when reinstalling or switching accounts.
- Reduce support noise by ensuring no leftover state remains.

---

## Files Included
- `cleaner.py` - Python version (cross-platform, recommended)
- `run.bat` - Windows batch version (no dependencies)
- `requirements.txt` - Python dependencies (none required; for documentation)
- `README.md` - This file
