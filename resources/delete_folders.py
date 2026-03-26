"""Folder deletion module for Roblox/Bloxstrap/Fishstrap directories and shortcuts."""

import os
import sys
import shutil
import stat
import glob
from pathlib import Path
from resources.utils import print_colored


def _on_rm_error(func, path, exc_info):
    """Handle removal errors by changing file permissions."""
    try:
        os.chmod(path, stat.S_IWRITE)
        try:
            os.remove(path)
        except Exception:
            pass
    except Exception:
        pass


def _delete_path(path: Path):
    """Delete a file or directory, handling permissions."""
    try:
        if path.is_file() or path.is_symlink():
            try:
                os.chmod(path, stat.S_IWRITE)
            except Exception:
                pass
            try:
                path.unlink(missing_ok=True)
            except TypeError:
                if path.exists():
                    path.unlink()
        elif path.exists():
            shutil.rmtree(path, onerror=_on_rm_error)
        print_colored(f"  Deleted {path}", "ok")
    except Exception as e:
        print_colored(f"  Could not delete {path}: {e}", "err")


def delete_folders() -> bool:
    """Delete all Roblox/Bloxstrap/Fishstrap related folders and shortcuts."""
    if sys.platform == "win32":
        env = os.environ
        folders_exact = [
            Path(env.get("LOCALAPPDATA", "")) / "Roblox",
            Path(env.get("APPDATA", "")) / "Roblox",
            Path(env.get("ProgramFiles", "")) / "Roblox",
            Path(env.get("ProgramFiles(x86)", "")) / "Roblox",
            Path("C:\\ProgramData\\Roblox"),
            Path(env.get("USERPROFILE", "")) / "AppData\\LocalLow\\Roblox",
            # Bloxstrap
            Path(env.get("LOCALAPPDATA", "")) / "Bloxstrap",
            Path(env.get("APPDATA", "")) / "Bloxstrap",
            Path(env.get("ProgramData", "")) / "Bloxstrap",
            Path(env.get("ProgramFiles", "")) / "Bloxstrap",
            Path(env.get("ProgramFiles(x86)", "")) / "Bloxstrap",
            # Fishstrap
            Path(env.get("LOCALAPPDATA", "")) / "Fishstrap",
            Path(env.get("APPDATA", "")) / "Fishstrap",
            Path(env.get("ProgramData", "")) / "Fishstrap",
            Path(env.get("ProgramFiles", "")) / "Fishstrap",
            Path(env.get("ProgramFiles(x86)", "")) / "Fishstrap",
        ]
        folders_patterns = [
            str(Path(env.get("LOCALAPPDATA", "")) / "Temp" / "Roblox"),
            str(Path(env.get("LOCALAPPDATA", "")) / "Temp" / "Bloxstrap"),
            str(Path(env.get("LOCALAPPDATA", "")) / "Temp" / "Fishstrap"),
            str(Path(env.get("LOCALAPPDATA", "")) / "Packages" / "ROBLOXCORPORATION.ROBLOX*"),
            str(Path(env.get("USERPROFILE", "")) / "Documents" / "Roblox*"),
        ]
        
        shortcut_locations = [
            Path(env.get("USERPROFILE", "")) / "Desktop",
            Path(env.get("PUBLIC", "C:/Users/Public")) / "Desktop",
            Path(env.get("APPDATA", "")) / "Microsoft\\Windows\\Start Menu\\Programs",
            Path(env.get("ProgramData", "")) / "Microsoft\\Windows\\Start Menu\\Programs",
            Path(env.get("APPDATA", "")) / "Microsoft\\Internet Explorer\\Quick Launch",
            Path(env.get("APPDATA", "")) / "Microsoft\\Windows\\Recent",
        ]
    else:
        folders = [
            Path.home() / "Library/Application Support/Roblox",
            Path.home() / "Library/Caches/com.roblox.Roblox",
            Path.home() / "Library/Preferences/com.roblox.Roblox.plist",
            Path.home() / "Library/Logs/Roblox",
            Path.home() / "Library/Saved Application State/com.roblox.Roblox.savedState",
        ]
        shortcut_locations = []
    
    print("Deleting leftover folders...")
    if sys.platform == "win32":
        for folder in folders_exact:
            if folder.exists():
                _delete_path(folder)
        for pattern in folders_patterns:
            for p in glob.glob(pattern):
                _delete_path(Path(p))
    else:
        for folder in folders:
            if folder.exists():
                _delete_path(folder)
    
    if sys.platform == "win32":
        print("Deleting shortcuts and icons...")
        for location in shortcut_locations:
            if location.exists():
                try:
                    for shortcut in list(location.rglob("*roblox*.lnk")) + list(location.rglob("*bloxstrap*.lnk")) + list(location.rglob("*fishstrap*.lnk")):
                        try:
                            shortcut.unlink()
                            print_colored(f"  Deleted shortcut: {shortcut.name}", "ok")
                        except Exception as e:
                            print_colored(f"  Could not delete {shortcut}: {e}", "err")
                except Exception as e:
                    print_colored(f"  Error scanning {location}: {e}", "err")
    
    print("  Folder cleanup complete.")
    return True
