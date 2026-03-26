#!/usr/bin/env python3
"""
Roblox Clean Sweep - Modular Manager with Process Monitoring
Entry point that manages all cleanup modules as separate processes/threads.
"""

import os
import sys
import threading
import time
import queue
from datetime import datetime
from typing import Dict, Callable, Tuple
from pathlib import Path

# Import all modules
from resources.utils import Colors, is_admin, request_elevation, print_colored
from resources.ui_menu import print_header, show_step_info, display_menu, toggle_menu, select_mode
from resources.kill_processes import kill_processes
from resources.delete_folders import delete_folders
from resources.cleanup_registry import cleanup_registry
from resources.cleanup_temp import cleanup_temp
from resources.flush_dns import flush_dns
from resources.delete_credentials import delete_credentials


class ProcessMonitor:
    """Monitors and manages cleanup process health."""
    
    def __init__(self):
        self.processes: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self.status_queue = queue.Queue()
        self.results = {}
        
    def register_process(self, name: str, func: Callable, step_num: int):
        """Register a cleanup process."""
        with self.lock:
            self.processes[name] = {
                "func": func,
                "step_num": step_num,
                "thread": None,
                "status": "pending",
                "start_time": None,
                "end_time": None,
                "result": None,
                "error": None,
                "restarts": 0,
            }
    
    def start_process(self, name: str):
        """Start a registered process in a thread."""
        with self.lock:
            if name not in self.processes:
                return False
            
            proc = self.processes[name]
            if proc["status"] in ["running", "completed"]:
                return False
            
            proc["status"] = "running"
            proc["start_time"] = datetime.now()
            thread = threading.Thread(target=self._run_process, args=(name,), daemon=False)
            proc["thread"] = thread
            thread.start()
            return True
    
    def _run_process(self, name: str):
        """Execute a cleanup process safely."""
        try:
            proc = self.processes[name]
            result = proc["func"]()
            with self.lock:
                proc["result"] = result
                proc["status"] = "completed"
                proc["end_time"] = datetime.now()
                self.results[name] = result
            self.status_queue.put((name, "completed", result))
        except Exception as e:
            with self.lock:
                proc["error"] = str(e)
                proc["status"] = "failed"
                proc["end_time"] = datetime.now()
            self.status_queue.put((name, "failed", str(e)))
    
    def restart_process(self, name: str):
        """Restart a failed process."""
        with self.lock:
            if name not in self.processes:
                return False
            
            proc = self.processes[name]
            proc["restarts"] += 1
            print_colored(f"[RESTART] {name} (attempt {proc['restarts']})", "warn")
            
            if proc["restarts"] > 3:
                print_colored(f"[ERROR] {name} failed after 3 restarts. Giving up.", "err")
                return False
        
        return self.start_process(name)
    
    def wait_for_completion(self, timeout: int = 300) -> Dict[str, bool]:
        """Wait for all processes to complete with timeout."""
        start_time = time.time()
        completed = set()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print_colored(f"[TIMEOUT] Cleanup exceeded {timeout} seconds", "err")
                break
            
            try:
                name, status, info = self.status_queue.get(timeout=2)
                completed.add(name)
                
                if status == "completed":
                    print_colored(f"[OK] {name} completed successfully", "ok")
                else:
                    print_colored(f"[FAILED] {name}: {info}", "err")
                    # Auto-restart on failure
                    if not self.restart_process(name):
                        print_colored(f"[FATAL] {name} could not be restarted", "err")
            except queue.Empty:
                # Check if all are done
                with self.lock:
                    all_done = all(
                        self.processes[pname]["status"] in ["completed", "failed"] 
                        for pname in self.processes
                    )
                    if all_done:
                        break
        
        return self.results
    
    def get_status(self) -> str:
        """Get current monitoring status."""
        with self.lock:
            status_lines = []
            for name, proc in self.processes.items():
                elapsed = ""
                if proc["start_time"]:
                    end = proc["end_time"] or datetime.now()
                    elapsed = f" ({(end - proc['start_time']).total_seconds():.1f}s)"
                
                status = f"{name}: {proc['status'].upper()}{elapsed}"
                if proc["error"]:
                    status += f" [{proc['error']}]"
                status_lines.append(status)
            return "\n".join(status_lines)


class CleanupManager:
    """Orchestrates the entire cleanup process."""
    
    def __init__(self):
        self.steps = {
            1: ("Kill Roblox processes", False),
            2: ("Delete Roblox folders", False),
            3: ("Registry cleanup", False),
            4: ("Temp/cache cleanup", False),
            5: ("Flush DNS cache", False),
            6: ("Delete Roblox credentials", False),
        }
        self.platform = sys.platform
        self.total_steps = 6
        self.done_steps = 0
        self.monitor = ProcessMonitor()
    
    def progress_bar(self, message: str):
        """Display progress bar."""
        self.done_steps += 1
        pct = (self.done_steps * 100) // self.total_steps
        filled = (self.done_steps * 20) // self.total_steps
        empty = 20 - filled
        bar = "#" * filled + "-" * empty
        print(f"[{bar}] {pct}% - {message}")
    
    def run_cleanup(self):
        """Execute all enabled cleanup steps."""
        print(f"\n{Colors.GREEN}Starting modular cleanup...{Colors.RESET}\n")
        
        # Map steps to functions
        step_funcs = {
            1: ("kill_processes", kill_processes),
            2: ("delete_folders", delete_folders),
            3: ("cleanup_registry", cleanup_registry),
            4: ("cleanup_temp", cleanup_temp),
            5: ("flush_dns", flush_dns),
            6: ("delete_credentials", delete_credentials),
        }
        
        # Register enabled processes
        for step_num in range(1, 7):
            name, enabled = self.steps[step_num]
            if enabled:
                proc_name, func = step_funcs[step_num]
                self.monitor.register_process(proc_name, func, step_num)
        
        # Start all registered processes
        for proc_name in self.monitor.processes:
            print_colored(f"[START] Starting {proc_name}...", "info")
            self.monitor.start_process(proc_name)
        
        # Monitor progress
        results = self.monitor.wait_for_completion(timeout=600)
        
        # Display final status
        print(f"\n{Colors.GREEN}=== MONITORING REPORT ==={Colors.RESET}")
        print(self.monitor.get_status())
        
        print(f"\n{Colors.GREEN}=== CLEANUP COMPLETE ==={Colors.RESET}")
        print("Restart your system before reinstalling Roblox.\n")
    
    def main(self):
        """Main entry point."""
        print_header()
        
        if not is_admin():
            print_colored("[INFO] Admin privileges required for full cleanup", "warn")
            request_elevation()
        
        mode = select_mode()
        
        if mode == 4:
            show_step_info(self.steps)
            return self.main()  # Show menu again
        
        if mode == 2:
            toggle_menu(self.steps)
        else:  # mode == 1
            # Enable all steps
            for i in range(1, 7):
                name, _ = self.steps[i]
                self.steps[i] = (name, True)
        
        self.run_cleanup()


def main():
    """Application entry point."""
    try:
        manager = CleanupManager()
        manager.main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPT] Cleanup interrupted by user.{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_colored(f"[FATAL] Unexpected error: {e}", "err")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
