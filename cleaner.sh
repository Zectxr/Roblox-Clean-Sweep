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
killall RobloxPlayer 2>/dev/null && echo "Killed RobloxPlayer"
killall RobloxStudio 2>/dev/null && echo "Killed RobloxStudio"
killall RobloxCrashHandler 2>/dev/null && echo "Killed RobloxCrashHandler"
killall RobloxInstaller 2>/dev/null && echo "Killed RobloxInstaller"
echo "Process cleanup complete."

# ================================
# DELETE FOLDERS
# ================================
echo "Deleting leftover folders..."
USER_HOME=$(eval echo ~${SUDO_USER})
if [ -d "$USER_HOME/Library/Application Support/Roblox" ]; then
    rm -rf "$USER_HOME/Library/Application Support/Roblox"
    echo "Deleted $USER_HOME/Library/Application Support/Roblox"
fi
if [ -d "$USER_HOME/Library/Caches/com.roblox.RobloxPlayer" ]; then
    rm -rf "$USER_HOME/Library/Caches/com.roblox.RobloxPlayer"
    echo "Deleted $USER_HOME/Library/Caches/com.roblox.RobloxPlayer"
fi
if [ -d "$USER_HOME/Library/Caches/com.roblox.RobloxStudio" ]; then
    rm -rf "$USER_HOME/Library/Caches/com.roblox.RobloxStudio"
    echo "Deleted $USER_HOME/Library/Caches/com.roblox.RobloxStudio"
fi
if [ -f "$USER_HOME/Library/Preferences/com.roblox.RobloxPlayer.plist" ]; then
    rm -rf "$USER_HOME/Library/Preferences/com.roblox.RobloxPlayer.plist"
    echo "Deleted $USER_HOME/Library/Preferences/com.roblox.RobloxPlayer.plist"
fi
if [ -f "$USER_HOME/Library/Preferences/com.roblox.RobloxStudio.plist" ]; then
    rm -rf "$USER_HOME/Library/Preferences/com.roblox.RobloxStudio.plist"
    echo "Deleted $USER_HOME/Library/Preferences/com.roblox.RobloxStudio.plist"
fi
if [ -d "$USER_HOME/Library/Saved Application State/com.roblox.RobloxPlayer.savedState" ]; then
    rm -rf "$USER_HOME/Library/Saved Application State/com.roblox.RobloxPlayer.savedState"
    echo "Deleted $USER_HOME/Library/Saved Application State/com.roblox.RobloxPlayer.savedState"
fi
if [ -d "$USER_HOME/Library/Saved Application State/com.roblox.RobloxStudio.savedState" ]; then
    rm -rf "$USER_HOME/Library/Saved Application State/com.roblox.RobloxStudio.savedState"
    echo "Deleted $USER_HOME/Library/Saved Application State/com.roblox.RobloxStudio.savedState"
fi
if [ -d "$USER_HOME/Library/Logs/Roblox" ]; then
    rm -rf "$USER_HOME/Library/Logs/Roblox"
    echo "Deleted $USER_HOME/Library/Logs/Roblox"
fi
if [ -d "$USER_HOME/Library/WebKit/com.roblox.RobloxPlayer" ]; then
    rm -rf "$USER_HOME/Library/WebKit/com.roblox.RobloxPlayer"
    echo "Deleted $USER_HOME/Library/WebKit/com.roblox.RobloxPlayer"
fi
if [ -d "/Applications/Roblox.app" ]; then
    rm -rf "/Applications/Roblox.app"
    echo "Deleted /Applications/Roblox.app"
fi
if [ -d "/Applications/RobloxStudio.app" ]; then
    rm -rf "/Applications/RobloxStudio.app"
    echo "Deleted /Applications/RobloxStudio.app"
fi
echo "Folder cleanup complete."

# ================================
# CACHE + TEMP CLEANUP
# ================================
echo "Cleaning temp and cache files..."
rm -rf /tmp/Roblox* 2>/dev/null && echo "Cleaned /tmp/Roblox*"
rm -rf /var/tmp/Roblox* 2>/dev/null && echo "Cleaned /var/tmp/Roblox*"
echo "Temp cleanup complete."

# ================================
# NETWORK CLEAN
# ================================
echo "Flushing DNS cache..."
dscacheutil -flushcache
killall -HUP mDNSResponder 2>/dev/null
echo "DNS cache flushed."

echo ""
echo "=== CLEANUP COMPLETE ==="
echo "Restart your Mac before reinstalling Roblox."
echo "Press Enter to exit..."
read