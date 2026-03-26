"""Network-related cleanup: DNS, firewall rules, scheduled tasks, hosts file."""

import os
import sys
import subprocess
from pathlib import Path
from typing import List
from resources.utils import print_colored


def remove_firewall_rules():
    """Remove firewall rules matching Roblox."""
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "Get-NetFirewallRule | Where-Object { $_.DisplayName -match '(?i)roblox|bloxstrap|fishstrap' } | ForEach-Object {"
            " $n = $_.DisplayName;"
            " try { $_ | Remove-NetFirewallRule -ErrorAction Stop; Write-Output ('DELETED_FW: ' + $n) }"
            " catch { Write-Output ('FAILED_FW: ' + $n) } }"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        deleted = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_FW: "):
                deleted += 1
                print_colored(f"  Deleted firewall rule: {line.split(': ',1)[1]}", "ok")
            elif line.startswith("FAILED_FW: "):
                print_colored(f"  Failed to delete firewall rule: {line.split(': ',1)[1]}", "err")
        if deleted == 0:
            print_colored("  No matching firewall rules found.", "warn")
    except Exception as e:
        print_colored(f"  Firewall rule cleanup error: {e}", "err")


def remove_scheduled_tasks():
    """Remove scheduled tasks matching Roblox."""
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "Get-ScheduledTask | Where-Object { $_.TaskName -match '(?i)roblox|bloxstrap|fishstrap' -or $_.TaskPath -match '(?i)roblox|bloxstrap|fishstrap' } | ForEach-Object {"
            " $n = $_.TaskName; $p = $_.TaskPath;"
            " try { Unregister-ScheduledTask -TaskName $n -TaskPath $p -Confirm:$false -ErrorAction Stop;"
            "       Write-Output ('DELETED_TASK: ' + $p + $n) }"
            " catch { Write-Output ('FAILED_TASK: ' + $p + $n) } }"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        deleted = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_TASK: "):
                deleted += 1
                print_colored(f"  Deleted scheduled task: {line.split(': ',1)[1]}", "ok")
            elif line.startswith("FAILED_TASK: "):
                print_colored(f"  Failed to delete scheduled task: {line.split(': ',1)[1]}", "err")
        if deleted == 0:
            print_colored("  No matching scheduled tasks found.", "warn")
    except Exception as e:
        print_colored(f"  Scheduled task cleanup error: {e}", "err")


def cleanup_hosts_file():
    """Remove Roblox entries from hosts file."""
    hosts_path = Path(os.environ.get("SystemRoot", "C:/Windows")) / "System32/drivers/etc/hosts"
    try:
        if not hosts_path.exists():
            return
        original = hosts_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        removed: List[str] = []
        kept: List[str] = []
        for line in original:
            lower = line.lower()
            if any(k in lower for k in ["roblox", "bloxstrap", "fishstrap"]):
                removed.append(line)
            else:
                kept.append(line)
        if removed:
            hosts_path.write_text("\n".join(kept) + "\n", encoding="utf-8")
            for r in removed:
                print_colored(f"  Removed hosts entry: {r.strip()}", "ok")
        else:
            print_colored("  No matching hosts entries found.", "warn")
    except Exception as e:
        print_colored(f"  Hosts cleanup error: {e}", "err")


def flush_dns() -> bool:
    """Flush DNS cache and reset IP configuration."""
    print("Flushing DNS cache and resetting IP...")
    try:
        if sys.platform == "win32":
            subprocess.run("ipconfig /release", shell=True, capture_output=True, timeout=10)
            print("  IP released.")
            subprocess.run("ipconfig /renew", shell=True, capture_output=True, timeout=10)
            print("  IP renewed.")
            subprocess.run("ipconfig /flushdns", shell=True, capture_output=True, timeout=5)
            print("  DNS cache flushed.")
            remove_firewall_rules()
            remove_scheduled_tasks()
            cleanup_hosts_file()
        else:
            subprocess.run("dscacheutil -flushcache", shell=True, capture_output=True, timeout=5)
            subprocess.run("sudo killall -HUP mDNSResponder", shell=True, capture_output=True, timeout=5)
            print("  DNS cache flushed.")
    except Exception as e:
        print(f"  [WARN] Network reset error: {e}")
    return True
