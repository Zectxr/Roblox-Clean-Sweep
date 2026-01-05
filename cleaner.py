#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import ctypes
from pathlib import Path
from typing import Dict, Tuple

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class RobloxCleaner:
    def __init__(self):
        self.total_steps = 6
        self.done_steps = 0
        self.steps = {
            1: ("Kill Roblox processes", False),
            2: ("Delete Roblox folders", False),
            3: ("Registry cleanup", False),
            4: ("Temp/cache cleanup", False),
            5: ("Flush DNS cache", False),
            6: ("Delete Roblox credentials", False),
        }
        self.platform = sys.platform
        
    def is_admin(self) -> bool:
        if self.platform == "win32":
            try:
                import ctypes
                return bool(ctypes.windll.shell.IsUserAnAdmin())
            except Exception as e:
                try:
                    subprocess.run("reg query HKLM", shell=True, capture_output=True, timeout=2)
                    return True
                except:
                    return False
        else:
            return os.geteuid() == 0
    
    def request_elevation(self):
        if self.platform == "win32":
            script_path = os.path.abspath(__file__)
            try:
                subprocess.Popen(
                    ['powershell', '-NoProfile', '-Command', 
                     f'Start-Process python -ArgumentList "{script_path}" -Verb RunAs'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE if self.platform == "win32" else 0
                )
                print("Elevation requested. A new window will open...")
                sys.exit(0)
            except Exception as e:
                print(f"[WARN] Could not request elevation: {e}")
                print("[WARN] Continuing without admin; some steps may fail.")
    
    def print_header(self):
        print(f"\n{Colors.CYAN}=== Roblox Clean Sweep (Python) ==={Colors.RESET}")
        print("Fast, thorough Roblox removal tool")
        print("Removes: processes, folders, registry/prefs, cache, DNS, credentials\n")
    
    def select_mode(self) -> int:
        print("Select mode:")
        print("  1) Run everything (all [+])")
        print("  2) Configure steps individually")
        while True:
            choice = input("\nChoose 1 or 2: ").strip()
            if choice in ["1", "2"]:
                return int(choice)
            print("[ERROR] Invalid choice. Enter 1 or 2.")
    
    def toggle_menu(self):
        print(f"\n{Colors.YELLOW}Configure steps (toggle number, A=all [+], S=start):{Colors.RESET}")
        while True:
            self.display_menu()
            choice = input("Select: ").strip().upper()
            
            if choice in ["1", "2", "3", "4", "5", "6"]:
                step_num = int(choice)
                name, enabled = self.steps[step_num]
                self.steps[step_num] = (name, not enabled)
            elif choice == "A":
                for i in range(1, 7):
                    name, _ = self.steps[i]
                    self.steps[i] = (name, True)
            elif choice == "S":
                break
            else:
                print("[ERROR] Invalid choice.")
    
    def display_menu(self):
        print("\nConfigure steps (toggle number, A=all [+], S=start):")
        for step_num in range(1, 7):
            name, enabled = self.steps[step_num]
            status = "+" if enabled else "-"
            print(f"  {step_num}) {name:<35} [{status}]")
        print("  A) Enable all [+]   S) Start run")
    
    def progress_bar(self, message: str):
        self.done_steps += 1
        pct = (self.done_steps * 100) // self.total_steps
        filled = (self.done_steps * 20) // self.total_steps
        empty = 20 - filled
        bar = "#" * filled + "-" * empty
        print(f"[{bar}] {pct}% - {message}")
    
    def run_step(self, step_num: int, func):
        name, enabled = self.steps[step_num]
        if enabled:
            try:
                result = func()
                self.progress_bar(f"{name} [Completed]")
                return True
            except Exception as e:
                print(f"[WARN] {name} error: {e}")
                self.progress_bar(f"{name} [Failed]")
                return False
        else:
            self.progress_bar(f"{name} [Skipped]")
            return True
    
    def kill_processes(self) -> bool:
        if self.platform != "win32":
            print("[INFO] Process killing skipped (Windows only)")
            return True
        
        processes = [
            "RobloxPlayerBeta.exe",
            "RobloxStudioBeta.exe",
            "RobloxCrashHandler.exe",
            "RobloxInstaller.exe",
        ]
        
        print("Killing Roblox processes...")
        for proc in processes:
            try:
                subprocess.run(f"taskkill /F /IM {proc}", shell=True, capture_output=True, timeout=5)
            except:
                print(f"  [WARN] {proc} not found or already terminated")
        print("  Done (some processes may not exist).")
        return True
    
    def delete_folders(self) -> bool:
        if self.platform == "win32":
            folders = [
                Path(os.environ.get("LOCALAPPDATA", "")) / "Roblox",
                Path(os.environ.get("APPDATA", "")) / "Roblox",
                Path(os.environ.get("ProgramFiles", "")) / "Roblox",
                Path(os.environ.get("ProgramFiles(x86)", "")) / "Roblox",
                Path("C:\\ProgramData\\Roblox"),
                Path(os.environ.get("USERPROFILE", "")) / "AppData\\LocalLow\\Roblox",
            ]
            
            shortcut_locations = [
                Path(os.environ.get("USERPROFILE", "")) / "Desktop",
                Path(os.environ.get("APPDATA", "")) / "Microsoft\\Windows\\Start Menu\\Programs",
                Path(os.environ.get("ProgramData", "")) / "Microsoft\\Windows\\Start Menu\\Programs",
                Path(os.environ.get("APPDATA", "")) / "Microsoft\\Internet Explorer\\Quick Launch",
                Path(os.environ.get("APPDATA", "")) / "Microsoft\\Windows\\Recent",
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
        for folder in folders:
            if folder.exists():
                try:
                    if folder.is_file():
                        folder.unlink()
                    else:
                        shutil.rmtree(folder)
                    print(f"  Deleted {folder}")
                except Exception as e:
                    print(f"  [WARN] Could not delete {folder}: {e}")
        
        if self.platform == "win32":
            print("Deleting shortcuts and icons...")
            for location in shortcut_locations:
                if location.exists():
                    try:
                        for shortcut in location.rglob("*roblox*.lnk"):
                            try:
                                shortcut.unlink()
                                print(f"  Deleted shortcut: {shortcut.name}")
                            except Exception as e:
                                print(f"  [WARN] Could not delete {shortcut}: {e}")
                    except Exception as e:
                        print(f"  [WARN] Error scanning {location}: {e}")
        
        print("  Folder cleanup complete.")
        return True
    
    def cleanup_registry(self) -> bool:
        if self.platform != "win32":
            print("[INFO] Registry cleanup skipped (Windows only)")
            return True
        
        print("Removing registry entries...")
        reg_paths = [
            r"HKCU\Software\Roblox",
            r"HKLM\Software\Roblox",
            r"HKLM\Software\WOW6432Node\Roblox",
        ]
        
        for path in reg_paths:
            try:
                subprocess.run(f"reg delete \"{path}\" /f", shell=True, capture_output=True, timeout=5)
                print(f"  Deleted {path}")
            except Exception as e:
                print(f"  [WARN] Could not delete {path}: {e}")
        print("  Registry cleanup complete.")
        return True
    
    def cleanup_temp(self) -> bool:
        if self.platform == "win32":
            temp_dir = Path(os.environ.get("TEMP", ""))
            roblox_temp = temp_dir / "Roblox"
        else:
            temp_dir = Path("/tmp")
            roblox_temp = temp_dir / "Roblox"
        
        print("Cleaning temp files...")
        try:
            if roblox_temp.exists():
                shutil.rmtree(roblox_temp)
                print(f"  Deleted {roblox_temp}")
            
            if self.platform == "win32":
                subprocess.run(f"del /F /Q \"{temp_dir}\\Roblox*.*\"", shell=True, capture_output=True)
        except Exception as e:
            print(f"  [WARN] Temp cleanup error: {e}")
        
        print("  Temp cleanup complete.")
        return True
    
    def flush_dns(self) -> bool:
        print("Flushing DNS cache and resetting IP...")
        try:
            if self.platform == "win32":
                subprocess.run("ipconfig /release", shell=True, capture_output=True, timeout=10)
                print("  IP released.")
                subprocess.run("ipconfig /renew", shell=True, capture_output=True, timeout=10)
                print("  IP renewed.")
                subprocess.run("ipconfig /flushdns", shell=True, capture_output=True, timeout=5)
                print("  DNS cache flushed.")
            else:
                subprocess.run("dscacheutil -flushcache", shell=True, capture_output=True, timeout=5)
                subprocess.run("sudo killall -HUP mDNSResponder", shell=True, capture_output=True, timeout=5)
                print("  DNS cache flushed.")
        except Exception as e:
            print(f"  [WARN] Network reset error: {e}")
        return True
    
    def delete_credentials(self) -> bool:
        if self.platform != "win32":
            print("[INFO] Credential deletion skipped (Windows only)")
            return True
        
        print("Deleting Roblox-related Windows credentials...")
        try:
            result = subprocess.run("cmdkey /list", shell=True, capture_output=True, text=True)
            lines = result.stdout.split('\n')
            removed_count = 0
            
            for line in lines:
                if 'Target:' in line and 'roblox' in line.lower():
                    target = line.split('Target:')[1].strip().split()[0] if 'Target:' in line else None
                    if target:
                        try:
                            subprocess.run(f"cmdkey /delete:\"{target}\"", shell=True, capture_output=True, timeout=5)
                            print(f"  Removed credential: {target}")
                            removed_count += 1
                        except Exception as e:
                            print(f"  [WARN] Could not delete credential {target}: {e}")
            
            if removed_count == 0:
                print("  No Roblox credentials found.")
        except Exception as e:
            print(f"  [WARN] Credential deletion error: {e}")
        
        print("  Credentials cleanup complete.")
        return True
    
    def run_cleanup(self):
        """Execute all enabled cleanup steps."""
        print(f"\n{Colors.GREEN}Starting cleanup...{Colors.RESET}\n")
        
        self.run_step(1, self.kill_processes)
        self.run_step(2, self.delete_folders)
        self.run_step(3, self.cleanup_registry)
        self.run_step(4, self.cleanup_temp)
        self.run_step(5, self.flush_dns)
        self.run_step(6, self.delete_credentials)
        
        print(f"\n{Colors.GREEN}=== CLEANUP COMPLETE ==={Colors.RESET}")
        print("Restart your system before reinstalling Roblox.\n")
    
    def main(self):
        """Main entry point."""
        self.print_header()
        
        # Check admin privileges
        if not self.is_admin():
            print("[INFO] Requesting administrator privileges...")
            self.request_elevation()
            return
        
        print("[OK] Running with elevated privileges.\n")
        
        # Select mode
        mode = self.select_mode()
        
        if mode == 1:
            # Run all
            print("\nRunning all steps with [+]\n")
            for i in range(1, 7):
                name, _ = self.steps[i]
                self.steps[i] = (name, True)
        else:
            # Configure
            self.toggle_menu()
        
        # Run cleanup
        self.run_cleanup()
        
        print("Press Ctrl+C to exit...")
        while True:
            import time
            time.sleep(1)

if __name__ == "__main__":
    cleaner = RobloxCleaner()
    try:
        cleaner.main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO] Cleanup canceled by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)
