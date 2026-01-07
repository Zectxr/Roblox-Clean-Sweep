#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import ctypes
import json
import random
import string
try:
    import winreg
except ImportError:
    winreg = None
from pathlib import Path
from typing import Dict, Tuple, List, Optional

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
        plain_lines = [
            "Roblox Clean Sweep",
            "Fast, thorough Roblox removal tool",
            "[ Processes | Folders | Registry/Prefs | Cache | DNS | Credentials ]",
        ]
        width = max(60, max(len(line) for line in plain_lines) + 4)
        border = f"{Colors.CYAN}{'=' * width}{Colors.RESET}"

        def framed_line(text: str, color: str) -> str:
            padded = text.ljust(width - 4)
            return f"{Colors.CYAN}|{Colors.RESET} {color}{padded}{Colors.RESET} {Colors.CYAN}|{Colors.RESET}"

        detail_line = f"{Colors.CYAN}[{Colors.RESET} Processes | Folders | Registry/Prefs | Cache | DNS | Credentials {Colors.CYAN}]{Colors.RESET}"

        print("\n" + border)
        print(framed_line("Roblox Clean Sweep", Colors.GREEN))
        print(framed_line("Fast, thorough Roblox removal tool", Colors.YELLOW))
        print(framed_line("[ Processes | Folders | Registry/Prefs | Cache | DNS | Credentials ]", Colors.CYAN))
        print(border + "\n")
    
    def select_mode(self) -> int:
        print("Select mode:")
        print("  1) Run everything")
        print("  2) Configure steps individually")
        print("  3) About steps (what they do)")
        print("  4) MAC address tools (Windows)")
        print("  0) Exit")
        while True:
            choice = input("\nChoose 1, 2, 3, or 4: ").strip()
            if choice == "0":
                print("[INFO] Exiting.")
                sys.exit(0)
            if choice == "3":
                self.show_step_info()
                continue
            if choice == "4":
                self.mac_tools_menu()
                continue
            if choice in ["1", "2"]:
                return int(choice)
            print("[ERROR] Invalid choice. Enter 1, 2, 3, or 4.")

    def show_step_info(self):
        print(f"\n{Colors.CYAN}What each step does:{Colors.RESET}")
        info = {
            1: "Kill any running Roblox executables to avoid file locks.",
            2: "Remove installs, cache, shortcuts, and Store/UWP package.",
            3: "Delete Roblox registry keys, uninstall entries, protocol handlers.",
            4: "Clear temp/cache, prefetch, crash dumps, recent items.",
            5: "Reset networking, flush DNS, clean firewall rules, hosts, tasks.",
            6: "Delete saved Windows credentials related to Roblox.",
        }
        for idx in range(1, 7):
            print(f"  {idx}) {self.steps[idx][0]} - {info[idx]}")
        print("")

    # ---------- MAC address tools (Windows) ----------
    def mac_tools_menu(self):
        if self.platform != "win32":
            print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} MAC tools are Windows-only.")
            return
        if winreg is None:
            print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} winreg not available; MAC tools require Windows Python.")
            return
        while True:
            adapters = self.list_adapters()
            if not adapters:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} No active adapters found or PowerShell unavailable.")
                return
            print(f"\n{Colors.CYAN}Active network adapters (select number):{Colors.RESET}")
            for idx, adp in enumerate(adapters, start=1):
                print(f"  {idx}) {adp['Name']} ({adp['MacAddress']})")
            print("  0) Back")
            choice = input("Select adapter: ").strip()
            if choice == "0":
                return
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(adapters):
                print("[ERROR] Invalid adapter selection.")
                continue
            adapter = adapters[int(choice) - 1]
            self.mac_action_menu(adapter)

    def mac_action_menu(self, adapter: Dict[str, str]):
        while True:
            print(f"\n{Colors.CYAN}Adapter:{Colors.RESET} {adapter['Name']}")
            print(f"  Current MAC: {adapter['MacAddress']}")
            print("  1) Randomize MAC")
            print("  2) Set custom MAC")
            print("  3) Revert to original (remove override)")
            print("  0) Back")
            choice = input("Select action: ").strip()
            if choice == "0":
                return
            if choice == "1":
                new_mac = self.generate_random_mac()
                self.apply_mac(adapter, new_mac)
            elif choice == "2":
                new_mac = self.prompt_custom_mac()
                if new_mac:
                    self.apply_mac(adapter, new_mac)
            elif choice == "3":
                self.revert_mac(adapter)
            else:
                print("[ERROR] Invalid action.")
            adapter = self.refresh_adapter(adapter)

    def list_adapters(self) -> List[Dict[str, str]]:
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object Name,InterfaceDescription,MacAddress,InterfaceGuid | ConvertTo-Json"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode != 0 or not res.stdout.strip():
                return []
            data = json.loads(res.stdout)
            if isinstance(data, dict):
                data = [data]
            adapters = []
            for item in data:
                mac = (item.get("MacAddress") or "").strip()
                name = (item.get("Name") or item.get("InterfaceDescription") or "Unknown").strip()
                guid = (item.get("InterfaceGuid") or "").strip()
                adapters.append({
                    "Name": name,
                    "MacAddress": mac if mac else "Unknown",
                    "Guid": guid,
                })
            return adapters
        except Exception:
            return []

    def refresh_adapter(self, adapter: Dict[str, str]) -> Dict[str, str]:
        adapters = self.list_adapters()
        for adp in adapters:
            if adp.get("Guid") and adapter.get("Guid") and adp["Guid"].lower() == adapter["Guid"].lower():
                return adp
            if adp.get("Name") == adapter.get("Name"):
                return adp
        return adapter

    def generate_random_mac(self) -> str:
        first = random.randint(0x00, 0xFF)
        first |= 0x02  # locally administered
        first &= 0xFE  # unicast
        tail = [random.randint(0x00, 0xFF) for _ in range(5)]
        octets = [first] + tail
        return "".join(f"{b:02X}" for b in octets)

    def prompt_custom_mac(self) -> Optional[str]:
        mac = input("Enter 12-digit hex MAC (no colons): ").strip().upper()
        if len(mac) != 12 or any(c not in string.hexdigits for c in mac):
            print("[ERROR] Invalid MAC format. Use 12 hex characters (0-9, A-F).")
            return None
        return mac

    def find_adapter_reg_key(self, guid: str) -> Optional[str]:
        if winreg is None:
            return None
        base_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path, 0, winreg.KEY_READ) as base:
                i = 0
                while True:
                    try:
                        sub = winreg.EnumKey(base, i)
                    except OSError:
                        break
                    i += 1
                    full = f"{base_path}\\{sub}"
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, full, 0, winreg.KEY_READ) as sk:
                            val, _ = winreg.QueryValueEx(sk, "NetCfgInstanceId")
                            if str(val).lower() == guid.lower():
                                return full
                    except FileNotFoundError:
                        continue
        except Exception:
            return None
        return None

    def apply_mac(self, adapter: Dict[str, str], mac: str):
        if winreg is None:
            print("[ERROR] winreg not available; cannot set MAC.")
            return
        if not adapter.get("Guid"):
            print("[ERROR] Cannot locate adapter GUID; aborting.")
            return
        reg_path = self.find_adapter_reg_key(adapter["Guid"])
        if not reg_path:
            print("[ERROR] Could not locate registry key for adapter.")
            return
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE) as sk:
                winreg.SetValueEx(sk, "NetworkAddress", 0, winreg.REG_SZ, mac)
            self.disable_enable_adapter(adapter["Name"])
            print(f"[OK] MAC updated to {mac} for {adapter['Name']}.")
        except PermissionError:
            print("[ERROR] Permission denied while writing registry. Run as administrator.")
        except Exception as e:
            print(f"[ERROR] Failed to set MAC: {e}")

    def revert_mac(self, adapter: Dict[str, str]):
        if winreg is None:
            print("[ERROR] winreg not available; cannot revert MAC.")
            return
        if not adapter.get("Guid"):
            print("[ERROR] Cannot locate adapter GUID; aborting.")
            return
        reg_path = self.find_adapter_reg_key(adapter["Guid"])
        if not reg_path:
            print("[ERROR] Could not locate registry key for adapter.")
            return
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE) as sk:
                try:
                    winreg.DeleteValue(sk, "NetworkAddress")
                except FileNotFoundError:
                    print("[INFO] No override present; already at original.")
                    return
            self.disable_enable_adapter(adapter["Name"])
            print(f"[OK] MAC override removed for {adapter['Name']}.")
        except PermissionError:
            print("[ERROR] Permission denied while modifying registry. Run as administrator.")
        except Exception as e:
            print(f"[ERROR] Failed to revert MAC: {e}")

    def disable_enable_adapter(self, name: str):
        # Disable and re-enable adapter to apply MAC changes.
        try:
            subprocess.run(f"netsh interface set interface '{name}' admin=disable", shell=True, capture_output=True, timeout=8)
            subprocess.run(f"netsh interface set interface '{name}' admin=enable", shell=True, capture_output=True, timeout=8)
        except Exception as e:
            print(f"[WARN] Could not bounce adapter: {e}")
    
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
            elif choice == "Q":
                print("[INFO] Exiting.")
                sys.exit(0)
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
        print("  A) Enable all [+]   S) Start run   Q) Exit")
    
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
            # Remove Microsoft Store/UWP Roblox package if installed
            self.remove_store_package()
        
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
            r"HKCU\Software\Roblox Corporation",
            r"HKCU\Software\Classes\roblox-player",
            r"HKCU\Software\Classes\roblox-player-1",
            r"HKLM\Software\Classes\roblox-player",
            r"HKLM\Software\Classes\roblox-player-1",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox Player",
            r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox",
            r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox Player",
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
                self.cleanup_prefetch_and_logs()
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
                self.remove_firewall_rules()
                self.remove_scheduled_tasks()
                self.cleanup_hosts_file()
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

    # ---------- Extra cleanup helpers ----------
    def remove_store_package(self):
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-AppxPackage -Name ROBLOXCORPORATION* | Remove-AppxPackage"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                if res.stdout.strip():
                    print("  Removed Microsoft Store Roblox package(s).")
                else:
                    print("  No Store/UWP Roblox package found.")
            else:
                print(f"  [WARN] Store package removal may have failed: {res.stderr.strip()}")
        except Exception as e:
            print(f"  [WARN] Store package removal error: {e}")

    def cleanup_prefetch_and_logs(self):
        try:
            prefetch_dir = Path("C:/Windows/Prefetch")
            if prefetch_dir.exists():
                for pf in prefetch_dir.glob("ROBLOX*.pf"):
                    try:
                        pf.unlink()
                        print(f"  Deleted prefetch: {pf.name}")
                    except Exception as e:
                        print(f"  [WARN] Could not delete prefetch {pf}: {e}")
        except Exception:
            pass

        try:
            crash_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "CrashDumps"
            if crash_dir.exists():
                for dump in crash_dir.glob("Roblox*.dmp"):
                    try:
                        dump.unlink()
                        print(f"  Deleted crash dump: {dump.name}")
                    except Exception as e:
                        print(f"  [WARN] Could not delete crash dump {dump}: {e}")
        except Exception:
            pass

        try:
            recent_dir = Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Recent"
            if recent_dir.exists():
                for item in recent_dir.glob("*roblox*.*"):
                    try:
                        item.unlink()
                        # Silent; avoid noisy output for many items
                    except Exception:
                        pass
        except Exception:
            pass

    def remove_firewall_rules(self):
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-NetFirewallRule | Where-Object { $_.DisplayName -like '*Roblox*' } | Remove-NetFirewallRule"
        ]
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print("  Removed Roblox firewall rules (if any).")
        except Exception as e:
            print(f"  [WARN] Firewall rule cleanup error: {e}")

    def remove_scheduled_tasks(self):
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-ScheduledTask | Where-Object { $_.TaskName -like '*Roblox*' } | Unregister-ScheduledTask -Confirm:$false"
        ]
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print("  Removed Roblox scheduled tasks (if any).")
        except Exception as e:
            print(f"  [WARN] Scheduled task cleanup error: {e}")

    def cleanup_hosts_file(self):
        hosts_path = Path(os.environ.get("SystemRoot", "C:/Windows")) / "System32/drivers/etc/hosts"
        try:
            if not hosts_path.exists():
                return
            original = hosts_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            filtered = [line for line in original if "roblox" not in line.lower()]
            if len(filtered) != len(original):
                hosts_path.write_text("\n".join(filtered) + "\n", encoding="utf-8")
                print("  Removed roblox entries from hosts file.")
        except Exception as e:
            print(f"  [WARN] Hosts cleanup error: {e}")
    
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
        
        input("Press Enter to exit...")

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
