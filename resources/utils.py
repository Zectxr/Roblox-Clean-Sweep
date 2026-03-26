"""Utilities and color codes for terminal output."""

import os
import sys
import subprocess


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


def print_colored(message: str, level: str = "info"):
    """Print colored status messages."""
    colors = {
        "ok": Colors.GREEN,
        "warn": Colors.YELLOW,
        "err": Colors.RED,
        "info": Colors.CYAN,
    }
    color = colors.get(level, Colors.CYAN)
    print(f"{color}{message}{Colors.RESET}")


def is_admin() -> bool:
    """Check if running with admin privileges."""
    platform = sys.platform
    if platform == "win32":
        try:
            import ctypes
            return bool(ctypes.windll.shell.IsUserAnAdmin())
        except Exception:
            try:
                subprocess.run("reg query HKLM", shell=True, capture_output=True, timeout=2)
                return True
            except:
                return False
    else:
        return os.geteuid() == 0


def request_elevation():
    """Request admin elevation on Windows."""
    if sys.platform == "win32":
        script_path = os.path.abspath(__file__)
        try:
            subprocess.Popen(
                ['powershell', '-NoProfile', '-Command', 
                 f'Start-Process python -ArgumentList "{script_path}" -Verb RunAs'],
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            print("Elevation requested. A new window will open...")
            sys.exit(0)
        except Exception as e:
            print(f"[WARN] Could not request elevation: {e}")
            print("[WARN] Continuing without admin; some steps may fail.")
