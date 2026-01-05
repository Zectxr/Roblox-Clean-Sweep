# A Guide To Roblox's Creating Or Using Accounts To Avoid Enforcement Action Ban Wave or all

This repository contains Roblox cleanup tools (`cleaner.bat` for Windows and `cleaner.sh` for macOS) designed to help users maintain clean Roblox installations and potentially avoid enforcement actions by ensuring no residual data remains.

## What is Roblox Clean Sweep?

Roblox Clean Sweep provides scripts that thoroughly remove Roblox-related files, folders, registry entries (Windows), preferences (macOS), and cache from your system. This can be useful when switching accounts or starting fresh to minimize risks associated with account enforcement.

## How to Use

### Windows
1. **Run as Administrator**: Right-click on `cleaner.bat` and select "Run as administrator".
2. **Follow Prompts**: The script will guide you through the cleanup process.
3. **Restart**: After cleanup, restart your PC before reinstalling Roblox.

### macOS
1. **Make Executable**: Open Terminal and run `chmod +x cleaner.sh`.
2. **Run as Root**: Run `sudo ./cleaner.sh`.
3. **Follow Prompts**: The script will guide you through the cleanup process.
4. **Restart**: After cleanup, restart your Mac before reinstalling Roblox.

## Features

- Kills all running Roblox processes
- Deletes Roblox folders from various locations
- Cleans registry entries (Windows) or preferences (macOS)
- Clears temp files and cache
- Flushes DNS cache

## Disclaimer

This tool is provided as-is. Use at your own risk. Ensure you backup any important data before running.

## Contributing

Feel free to contribute improvements or report issues.