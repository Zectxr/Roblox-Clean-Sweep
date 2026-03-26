"""Registry cleanup module for Roblox/Bloxstrap/Fishstrap entries."""

import sys
import subprocess
try:
    import winreg
except ImportError:
    winreg = None
from resources.utils import print_colored


def cleanup_registry() -> bool:
    """Delete all Roblox/Bloxstrap/Fishstrap registry entries."""
    if sys.platform != "win32":
        print("[INFO] Registry cleanup skipped (Windows only)")
        return True
    
    print("Removing registry entries...")
    reg_paths = [
        # Roblox
        r"HKCU\Software\Roblox",
        r"HKCU\Software\ROBLOX Corporation",
        r"HKLM\Software\Roblox",
        r"HKLM\Software\ROBLOX Corporation",
        r"HKLM\Software\WOW6432Node\Roblox",
        r"HKLM\Software\WOW6432Node\ROBLOX Corporation",
        r"HKCU\Software\Classes\roblox-player",
        r"HKCU\Software\Classes\roblox-player-1",
        r"HKCU\Software\Classes\roblox",
        r"HKCU\Software\Classes\roblox-studio",
        r"HKCU\Software\Classes\roblox-studio-auth",
        r"HKLM\Software\Classes\roblox-player",
        r"HKLM\Software\Classes\roblox-player-1",
        r"HKLM\Software\Classes\roblox",
        r"HKLM\Software\Classes\roblox-studio",
        r"HKLM\Software\Classes\roblox-studio-auth",
        r"HKCU\Software\Microsoft\Internet Explorer\ProtocolExecute\roblox-studio",
        r"HKCU\Software\Microsoft\Internet Explorer\ProtocolExecute\roblox-studio-auth",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.rbxl",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.rbxlx",
        # Bloxstrap
        r"HKCU\Software\Bloxstrap",
        r"HKLM\Software\Bloxstrap",
        r"HKLM\Software\WOW6432Node\Bloxstrap",
        r"HKCU\Software\Classes\bloxstrap",
        r"HKLM\Software\Classes\bloxstrap",
        # Fishstrap
        r"HKCU\Software\Fishstrap",
        r"HKLM\Software\Fishstrap",
        r"HKLM\Software\WOW6432Node\Fishstrap",
        r"HKCU\Software\Classes\fishstrap",
        r"HKLM\Software\Classes\fishstrap",
        # Legacy uninstall entries
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox Player",
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox",
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Roblox Player",
    ]
    
    for path in reg_paths:
        try:
            subprocess.run(f"reg delete \"{path}\" /f", shell=True, capture_output=True, timeout=5)
            print_colored(f"  Deleted {path}", "ok")
        except Exception as e:
            print_colored(f"  Could not delete {path}: {e}", "err")
    
    # Delete Run registry entries
    run_values = ["RobloxPlayerBeta"]
    run_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
    for value in run_values:
        try:
            subprocess.run(f"reg delete \"{run_path}\" /v {value} /f", shell=True, capture_output=True, timeout=5)
            print_colored(f"  Deleted {run_path} \\{value}", "ok")
        except Exception as e:
            print_colored(f"  Could not delete {run_path} \\{value}: {e}", "err")
    
    # CloudStore entries via PowerShell
    _cleanup_cloudstore()
    _remove_uninstall_entries()
    _cleanup_mui_cache()
    _cleanup_userassist()
    _amcache_shimcache_awareness()
    
    print("  Registry cleanup complete.")
    return True


def _cleanup_cloudstore():
    """Clean CloudStore entries."""
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "$root='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current';"
            "if (Test-Path $root) {"
            "Get-ChildItem $root -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '(?i)roblox|bloxstrap|fishstrap' } | ForEach-Object {"
            " try { Remove-Item -Path $_.PSPath -Recurse -Force -ErrorAction Stop;"
            "       Write-Output ('DELETED_CLOUD: ' + $_.Name) }"
            " catch { Write-Output ('FAILED_CLOUD: ' + $_.Name) } } }"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        deleted = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_CLOUD: "):
                deleted += 1
                print_colored(f"  Deleted CloudStore entry: {line.split(': ',1)[1]}", "ok")
            elif line.startswith("FAILED_CLOUD: "):
                print_colored(f"  Could not delete CloudStore entry: {line.split(': ',1)[1]}", "err")
        if deleted == 0:
            print_colored("  No matching CloudStore entries found.", "warn")
    except Exception as e:
        print_colored(f"  CloudStore cleanup error: {e}", "err")


def _remove_uninstall_entries():
    """Remove uninstall entries matching Roblox/Bloxstrap/Fishstrap."""
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "$roots = @('HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall',"
            "'HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall',"
            "'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall');"
            "foreach ($r in $roots) { if (Test-Path $r) {"
            "Get-ChildItem $r -ErrorAction SilentlyContinue | ForEach-Object {"
            "try { $p = Get-ItemProperty $_.PSPath -ErrorAction Stop;"
            " if ($p.DisplayName -match '(?i)Roblox|Bloxstrap|Fishstrap') {"
            "  try { Remove-Item -LiteralPath $_.PSPath -Recurse -Force -ErrorAction Stop;"
            "        Write-Output ('DELETED_UNINSTALL: ' + $p.DisplayName) }"
            "  catch { Write-Output ('FAILED_UNINSTALL: ' + $p.DisplayName) } } } catch {} } }"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        deleted = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_UNINSTALL: "):
                deleted += 1
                print_colored(f"  Deleted uninstall entry: {line.split(': ',1)[1]}", "ok")
            elif line.startswith("FAILED_UNINSTALL: "):
                print_colored(f"  Failed to remove uninstall entry: {line.split(': ',1)[1]}", "err")
        if deleted == 0:
            print_colored("  No matching uninstall entries found.", "warn")
    except Exception as e:
        print_colored(f"  Uninstall entries cleanup error: {e}", "err")


def _cleanup_mui_cache():
    """Clean MUICache entries for Roblox."""
    print("Cleaning MUICache entries...")
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "$keys = @('HKCU:\\Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache',"
            "'HKCU:\\Software\\Microsoft\\Windows\\ShellNoRoam\\MUICache');"
            "$terms = '(?i)roblox|bloxstrap|fishstrap';"
            "foreach ($k in $keys) { if (Test-Path $k) {"
            " try { $props = (Get-ItemProperty -Path $k -ErrorAction Stop).PSObject.Properties |"
            "        Where-Object { $_.Name -notmatch '^PS' -and ($_.Name -match $terms -or ([string]$_.Value) -match $terms) };"
            "       foreach ($p in $props) {"
            "         try { Remove-ItemProperty -Path $k -Name $p.Name -ErrorAction Stop;"
            "               Write-Output ('DELETED_MUI: ' + $k + ' -> ' + $p.Name) }"
            "         catch { Write-Output ('FAILED_MUI: ' + $k + ' -> ' + $p.Name) }"
            "       }"
            " } catch {} } }"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        deleted = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_MUI: "):
                deleted += 1
                print_colored(f"  Deleted MUICache value: {line.split(': ', 1)[1]}", "ok")
            elif line.startswith("FAILED_MUI: "):
                print_colored(f"  Failed MUICache value deletion: {line.split(': ', 1)[1]}", "err")
        if deleted == 0:
            print_colored("  No matching MUICache values found.", "warn")
    except Exception as e:
        print_colored(f"  MUICache cleanup error: {e}", "err")


def _cleanup_userassist():
    """Clean UserAssist entries for Roblox."""
    print("Cleaning UserAssist traces...")
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "$base='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist';"
            "$terms='(?i)roblox|bloxstrap|fishstrap';"
            "function Decode-Rot13([string]$s){"
            " if (-not $s) { return $s }"
            " $chars = $s.ToCharArray();"
            " for ($i=0; $i -lt $chars.Length; $i++) {"
            "   $c=[int][char]$chars[$i];"
            "   if (($c -ge 65 -and $c -le 90) -or ($c -ge 97 -and $c -le 122)) {"
            "     $b = if ($c -ge 97) {97} else {65};"
            "     $chars[$i] = [char]((($c - $b + 13) % 26) + $b)"
            "   }"
            " }"
            " return -join $chars"
            "}"
            "if (Test-Path $base) {"
            " Get-ChildItem -Path $base -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.PSChildName -eq 'Count' } | ForEach-Object {"
            "   $k = $_.PSPath;"
            "   try {"
            "     $props = (Get-ItemProperty -Path $k -ErrorAction Stop).PSObject.Properties | Where-Object { $_.Name -notmatch '^PS' };"
            "     foreach ($p in $props) {"
            "       $decoded = Decode-Rot13 $p.Name;"
            "       if ($decoded -match $terms -or $p.Name -match $terms) {"
            "         try { Remove-ItemProperty -Path $k -Name $p.Name -ErrorAction Stop;"
            "               Write-Output ('DELETED_UA: ' + $decoded) }"
            "         catch { Write-Output ('FAILED_UA: ' + $decoded) }"
            "       }"
            "     }"
            "   } catch {}"
            " }"
            "}"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        deleted = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_UA: "):
                deleted += 1
                print_colored(f"  Deleted UserAssist value: {line.split(': ', 1)[1]}", "ok")
            elif line.startswith("FAILED_UA: "):
                print_colored(f"  Failed UserAssist value deletion: {line.split(': ', 1)[1]}", "err")
        if deleted == 0:
            print_colored("  No matching UserAssist values found.", "warn")
    except Exception as e:
        print_colored(f"  UserAssist cleanup error: {e}", "err")


def _amcache_shimcache_awareness():
    """Check Amcache/ShimCache presence and remove AppCompat traces."""
    print("Checking Amcache/ShimCache traces...")
    cmd = [
        "powershell", "-NoProfile", "-Command",
        (
            "$terms='(?i)roblox|bloxstrap|fishstrap';"
            "$am='HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Compatibility Assistant\\Store';"
            "if (Test-Path $am) {"
            " try {"
            "  $props=(Get-ItemProperty -Path $am -ErrorAction Stop).PSObject.Properties |"
            "   Where-Object { $_.Name -notmatch '^PS' -and $_.Name -match $terms };"
            "  foreach ($p in $props) {"
            "   try { Remove-ItemProperty -Path $am -Name $p.Name -ErrorAction Stop;"
            "         Write-Output ('DELETED_COMPAT_STORE: ' + $p.Name) }"
            "   catch { Write-Output ('FAILED_COMPAT_STORE: ' + $p.Name) }"
            "  }"
            " } catch {}"
            "}"
            "Write-Output 'SHIMCACHE_PRESENT: System may have ShimCache data (kernel-managed, safe removal not possible)'"
        )
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        removed = 0
        for line in res.stdout.splitlines():
            if line.startswith("DELETED_COMPAT_STORE: "):
                removed += 1
                print_colored(f"  Deleted AppCompat trace: {line.split(': ', 1)[1]}", "ok")
            elif line.startswith("FAILED_COMPAT_STORE: "):
                print_colored(f"  Failed AppCompat trace deletion: {line.split(': ', 1)[1]}", "err")
            elif line.startswith("SHIMCACHE_PRESENT: "):
                print_colored("  ShimCache is kernel-managed; selective removal not safely supported.", "warn")
        if removed == 0:
            print_colored("  No matching Amcache/AppCompat trace values found.", "warn")
    except Exception as e:
        print_colored(f"  Amcache/ShimCache awareness error: {e}", "err")
