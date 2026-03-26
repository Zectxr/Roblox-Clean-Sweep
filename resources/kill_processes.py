"""Process killing module for Roblox and related applications."""

import sys
import subprocess
from resources.utils import print_colored


def kill_processes() -> bool:
    """Kill all running Roblox and related processes."""
    if sys.platform != "win32":
        print("[INFO] Process killing skipped (Windows only)")
        return True
    
    processes = [
        # Roblox
        "RobloxPlayerBeta.exe",
        "RobloxPlayer.exe",
        "RobloxStudioBeta.exe",
        "RobloxStudio.exe",
        "RobloxCrashHandler.exe",
        "RobloxInstaller.exe",
        "RobloxPlayerLauncher.exe",
        # Tools
        "RbxFpsUnlocker.exe",
        # Bloxstrap
        "Bloxstrap.exe",
        "BloxstrapBootstrapper.exe",
        "BloxstrapRPC.exe",
        # Fishstrap
        "Fishstrap.exe",
        "FishstrapBootstrapper.exe",
    ]
    
    print("Killing Roblox processes...")
    for proc in processes:
        try:
            subprocess.run(f"taskkill /F /IM {proc}", shell=True, capture_output=True, timeout=5)
        except:
            print(f"  [WARN] {proc} not found or already terminated")
    print("  Done (some processes may not exist).")
    return True
