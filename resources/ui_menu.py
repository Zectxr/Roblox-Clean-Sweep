"""User interface and menu module."""

import sys
from resources.utils import Colors


def print_header():
    """Print the application header banner."""
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

    print("\n" + border)
    print(framed_line("Roblox Clean Sweep", Colors.GREEN))
    print(framed_line("Fast, thorough Roblox removal tool", Colors.YELLOW))
    print(framed_line("[ Processes | Folders | Registry/Prefs | Cache | DNS | Credentials ]", Colors.CYAN))
    print(border + "\n")


def show_step_info(steps: dict):
    """Display information about each cleanup step."""
    print(f"\n{Colors.CYAN}What each step does:{Colors.RESET}")
    info = {
        1: "Kill any running Roblox executables to avoid file locks.",
        2: "Remove installs, cache, shortcuts, and Store/UWP package.",
        3: "Delete registry keys plus MUICache/UserAssist and appcompat traces.",
        4: "Clear temp/cache, prefetch, jump lists, crash dumps, recent items.",
        5: "Reset networking, flush DNS, clean firewall rules, hosts, tasks.",
        6: "Delete saved Windows credentials related to Roblox.",
    }
    for idx in range(1, 7):
        print(f"  {idx}) {steps[idx][0]} - {info[idx]}")
    print("")


def display_menu(steps: dict):
    """Display the step configuration menu."""
    print("\nConfigure steps (toggle number, A=all [+], S=start):")
    for step_num in range(1, 7):
        name, enabled = steps[step_num]
        status = "+" if enabled else "-"
        print(f"  {step_num}) {name:<35} [{status}]")
    print("  A) Enable all [+]   S) Start run   Q) Exit")


def toggle_menu(steps: dict):
    """Interactive menu to toggle cleanup steps."""
    print(f"\n{Colors.YELLOW}Configure steps (toggle number, A=all [+], S=start):{Colors.RESET}")
    while True:
        display_menu(steps)
        choice = input("Select: ").strip().upper()
        
        if choice in ["1", "2", "3", "4", "5", "6"]:
            step_num = int(choice)
            name, enabled = steps[step_num]
            steps[step_num] = (name, not enabled)
        elif choice == "A":
            for i in range(1, 7):
                name, _ = steps[i]
                steps[i] = (name, True)
        elif choice == "Q":
            print("[INFO] Exiting.")
            sys.exit(0)
        elif choice == "S":
            break
        else:
            print("[ERROR] Invalid choice.")


def select_mode() -> int:
    """Display and handle mode selection menu."""
    print("Select mode:")
    print("  1) Deep Cleaning")
    print("  2) Configure steps individually")
    print("  3) MAC address tools (Windows)")
    print("  4) About steps (what they do)")
    print("  0) Exit")
    while True:
        choice = input("\nChoose 1, 2, 3, or 4: ").strip()
        if choice == "0":
            print("[INFO] Exiting.")
            sys.exit(0)
        if choice == "3":
            print("[INFO] MAC tools require additional setup.")
            continue
        if choice == "4":
            # Will be called from main
            return 4
        if choice in ["1", "2"]:
            return int(choice)
        print("[ERROR] Invalid choice. Enter 1, 2, 3, or 4.")
