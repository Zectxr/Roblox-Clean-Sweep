#!/bin/bash

# Roblox Full Cleanup Tool for macOS
# Run with sudo: sudo ./cleaner.sh

# ================================
# ROOT CHECK
# ================================
if [ "$EUID" -ne 0 ]; then
    echo "[ERROR] Please run this script as root: sudo ./cleaner.sh"
    exit 1
fi

echo "=== Roblox Uninstall Helper for macOS ==="
echo "This will remove Roblox files, folders, cache, and preferences."
echo "Make sure Roblox is already uninstalled from Applications."
echo "Press Enter to continue..."
read

# ================================
# KILL ROBLOX PROCESSES
# ================================
echo "Killing Roblox processes..."
killall RobloxPlayer 2>/dev/null
killall RobloxStudio 2>/dev/null
killall RobloxCrashHandler 2>/dev/null

# ================================
# DELETE FOLDERS
# ================================
echo "Deleting leftover folders..."
rm -rf ~/Library/Application\ Support/Roblox
rm -rf ~/Library/Caches/com.roblox.RobloxPlayer
rm -rf ~/Library/Caches/com.roblox.RobloxStudio
rm -rf ~/Library/Preferences/com.roblox.RobloxPlayer.plist
rm -rf ~/Library/Preferences/com.roblox.RobloxStudio.plist
rm -rf ~/Library/Saved\ Application\ State/com.roblox.RobloxPlayer.savedState
rm -rf ~/Library/Saved\ Application\ State/com.roblox.RobloxStudio.savedState
rm -rf /Applications/Roblox.app  # If still present
rm -rf /Applications/RobloxStudio.app  # If still present

# ================================
# CACHE + TEMP CLEANUP
# ================================
echo "Cleaning temp and cache files..."
rm -rf /tmp/Roblox*
rm -rf /var/tmp/Roblox*

# ================================
# NETWORK CLEAN
# ================================
echo "Flushing DNS cache..."
dscacheutil -flushcache
killall -HUP mDNSResponder

echo ""
echo "=== CLEANUP COMPLETE ==="
echo "Restart your Mac before reinstalling Roblox."
echo "Press Enter to exit..."
read