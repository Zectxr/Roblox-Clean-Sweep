"""Temporary files and cache cleanup module."""

import os
import sys
import shutil
from pathlib import Path
from resources.utils import print_colored


def cleanup_prefetch_and_logs():
    """Clean prefetch files, crash dumps, and recent items."""
    try:
        prefetch_dir = Path("C:/Windows/Prefetch")
        if prefetch_dir.exists():
            for pf in prefetch_dir.glob("ROBLOX*.pf"):
                try:
                    pf.unlink()
                    print_colored(f"  Deleted prefetch: {pf.name}", "ok")
                except Exception as e:
                    print_colored(f"  Could not delete prefetch {pf}: {e}", "err")
    except Exception:
        pass

    try:
        crash_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "CrashDumps"
        if crash_dir.exists():
            for dump in crash_dir.glob("Roblox*.dmp"):
                try:
                    dump.unlink()
                    print_colored(f"  Deleted crash dump: {dump.name}", "ok")
                except Exception as e:
                    print_colored(f"  Could not delete crash dump {dump}: {e}", "err")
    except Exception:
        pass

    try:
        recent_dir = Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Recent"
        if recent_dir.exists():
            for item in recent_dir.glob("*roblox*.*"):
                try:
                    item.unlink()
                    print_colored(f"  Deleted recent item: {item.name}", "ok")
                except Exception:
                    pass
    except Exception:
        pass


def cleanup_jump_lists():
    """Clean jump list entries containing Roblox traces."""
    print("Cleaning jump list entries...")
    appdata = Path(os.environ.get("APPDATA", ""))
    locations = [
        appdata / "Microsoft/Windows/Recent/AutomaticDestinations",
        appdata / "Microsoft/Windows/Recent/CustomDestinations",
    ]
    keywords = [b"roblox", b"bloxstrap", b"fishstrap"]
    deleted = 0
    for location in locations:
        if not location.exists():
            continue
        try:
            for item in location.glob("*.automaticDestinations-ms"):
                try:
                    raw = item.read_bytes().lower()
                    if any(k in raw for k in keywords):
                        item.unlink()
                        deleted += 1
                        print_colored(f"  Deleted jump list: {item.name}", "ok")
                except Exception as e:
                    print_colored(f"  Could not inspect/delete jump list {item}: {e}", "err")
            for item in location.glob("*.customDestinations-ms"):
                try:
                    raw = item.read_bytes().lower()
                    if any(k in raw for k in keywords):
                        item.unlink()
                        deleted += 1
                        print_colored(f"  Deleted jump list: {item.name}", "ok")
                except Exception as e:
                    print_colored(f"  Could not inspect/delete jump list {item}: {e}", "err")
        except Exception as e:
            print_colored(f"  Error scanning jump list path {location}: {e}", "err")

    if deleted == 0:
        print_colored("  No matching jump list files found.", "warn")


def filter_event_logs():
    """Filter event logs for Roblox traces."""
    print("Filtering event logs for Roblox traces...")
    import subprocess
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "$logs = @('Application','System','Windows PowerShell','Microsoft-Windows-PowerShell/Operational');"
            "$terms = '(?i)roblox|bloxstrap|fishstrap';"
            "foreach ($log in $logs) {"
            " try {"
            "  $found = Get-WinEvent -LogName $log -MaxEvents 2500 -ErrorAction Stop | Where-Object {"
            "   $_.ProviderName -match $terms -or $_.Message -match $terms"
            "  } | Select-Object -First 1;"
            "  if ($found) {"
            "   try { wevtutil cl \"$log\"; Write-Output ('CLEARED_LOG: ' + $log) }"
            "   catch { Write-Output ('FAILED_LOG: ' + $log) }"
            "  }"
            " } catch {}"
            "}"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        cleared = 0
        for line in res.stdout.splitlines():
            if line.startswith("CLEARED_LOG: "):
                cleared += 1
                print_colored(f"  Cleared event log: {line.split(': ', 1)[1]}", "ok")
            elif line.startswith("FAILED_LOG: "):
                print_colored(f"  Could not clear event log: {line.split(': ', 1)[1]}", "err")
        if cleared == 0:
            print_colored("  No event logs with Roblox matches found.", "warn")
    except Exception as e:
        print_colored(f"  Event log filtering error: {e}", "err")


def cleanup_temp() -> bool:
    """Clean temporary and cache files."""
    if sys.platform == "win32":
        temp_dir = Path(os.environ.get("TEMP", ""))
        roblox_temp = temp_dir / "Roblox"
    else:
        temp_dir = Path("/tmp")
        roblox_temp = temp_dir / "Roblox"
    
    print("Cleaning temp files...")
    try:
        if roblox_temp.exists():
            shutil.rmtree(roblox_temp)
            print_colored(f"  Deleted {roblox_temp}", "ok")
        
        if sys.platform == "win32":
            for pattern in ["Roblox*.*", "Bloxstrap*.*", "Fishstrap*.*"]:
                for f in temp_dir.glob(pattern):
                    try:
                        if f.exists() and f.is_file():
                            f.unlink()
                            print_colored(f"  Deleted temp: {f}", "ok")
                    except Exception as fe:
                        print_colored(f"  Could not delete temp {f}: {fe}", "err")
            cleanup_prefetch_and_logs()
            cleanup_jump_lists()
            if sys.platform == "win32":
                filter_event_logs()
    except Exception as e:
        print_colored(f"  Temp cleanup error: {e}", "err")
    
    print("  Temp cleanup complete.")
    return True
