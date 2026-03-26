"""Windows credentials deletion module."""

import sys
import subprocess
from resources.utils import print_colored


def delete_credentials() -> bool:
    """Delete stored Windows credentials related to Roblox."""
    if sys.platform != "win32":
        print("[INFO] Credential deletion skipped (Windows only)")
        return True
    
    print("Deleting Roblox-related Windows credentials...")
    try:
        result = subprocess.run("cmdkey /list", shell=True, capture_output=True, text=True)
        lines = result.stdout.split('\n')
        removed_count = 0
        
        for line in lines:
            if 'Target:' in line and any(x in line.lower() for x in ['roblox','bloxstrap','fishstrap']):
                target = line.split('Target:')[1].strip().split()[0] if 'Target:' in line else None
                if target:
                    try:
                        subprocess.run(f"cmdkey /delete:\"{target}\"", shell=True, capture_output=True, timeout=5)
                        print_colored(f"  Removed credential: {target}", "ok")
                        removed_count += 1
                    except Exception as e:
                        print_colored(f"  Could not delete credential {target}: {e}", "err")
        
        if removed_count == 0:
            print_colored("  No Roblox credentials found.", "warn")
    except Exception as e:
        print_colored(f"  Credential deletion error: {e}", "err")
    
    print("  Credentials cleanup complete.")
    return True
