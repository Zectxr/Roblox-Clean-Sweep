"""
MODULAR ARCHITECTURE GUIDE
===========================

The refactored Roblox Clean Sweep has been redesigned into a modular architecture
with separate processes/threads for each cleanup function and a centralized monitoring system.

PROJECT STRUCTURE
=================

Roblox Clean Sweep/
├── main.py                          # Entry point with process manager
├── cleaner.py                       # Original monolithic version (legacy)
├── run.bat                          # Batch launcher for Windows
├── README.md                        # Main documentation
└── resources/                       # Modular cleanup functions
    ├── __init__.py                  # Package marker
    ├── utils.py                     # Utilities (Colors, Admin, Elevation)
    ├── ui_menu.py                   # UI and menu functions
    ├── kill_processes.py            # Process termination
    ├── delete_folders.py            # Folder and shortcut deletion
    ├── cleanup_registry.py          # Registry cleanup (main + helpers)
    ├── cleanup_temp.py              # Temp files, cache, jump lists, event logs
    ├── flush_dns.py                 # DNS, firewall, tasks, hosts cleanup
    └── delete_credentials.py        # Windows credentials deletion


KEY COMPONENTS
==============

1. ProcessMonitor (main.py)
   - Registers cleanup functions as separate processes
   - Manages threading for parallel execution
   - Monitors health and auto-restarts failed processes
   - Provides status reporting and progress tracking
   - Features:
     * Thread-safe status management
     * Automatic restart on failure (max 3 attempts)
     * Timeout protection
     * Real-time status queue
     * Result collection

2. CleanupManager (main.py)
   - Orchestrates the entire cleanup workflow
   - UI interaction for step selection
   - Progress bar display
   - Admin elevation checking
   - Wraps ProcessMonitor functionality

3. Utilities (resources/utils.py)
   - Color codes for terminal output
   - Admin privilege checking
   - Elevation request for Windows

4. UI Module (resources/ui_menu.py)
   - Header banner printing
   - Step information display
   - Interactive menu system
   - Mode selection (deep clean vs. configure)

5. Cleanup Modules
   Each module contains one primary function plus helpers:
   
   resources/kill_processes.py
   ├── kill_processes()          # Primary function
   
   resources/delete_folders.py
   ├── delete_folders()           # Primary function
   ├── _delete_path()            # Helper: safe file/dir deletion
   └── _on_rm_error()            # Helper: permission handling
   
   resources/cleanup_registry.py
   ├── cleanup_registry()         # Primary function
   ├── _cleanup_cloudstore()     # Helper: CloudStore cleanup
   ├── _remove_uninstall_entries() # Helper: Uninstall entries
   ├── _cleanup_mui_cache()       # Helper: MUICache entries
   ├── _cleanup_userassist()      # Helper: UserAssist entries
   └── _amcache_shimcache_awareness() # Helper: AppCompat traces
   
   resources/cleanup_temp.py
   ├── cleanup_temp()            # Primary function
   ├── cleanup_prefetch_and_logs() # Helper: Prefetch, crash dumps, recent
   ├── cleanup_jump_lists()       # Helper: Jump list cleanup
   └── filter_event_logs()        # Helper: Event log filtering
   
   resources/flush_dns.py
   ├── flush_dns()               # Primary function
   ├── remove_firewall_rules()    # Helper: Firewall rules
   ├── remove_scheduled_tasks()   # Helper: Scheduled tasks
   └── cleanup_hosts_file()       # Helper: Hosts file entries
   
   resources/delete_credentials.py
   └── delete_credentials()       # Primary function


EXECUTION FLOW
==============

1. User runs: python main.py
2. CleanupManager.main() initializes
3. AdminCheck → Prompts elevation if needed
4. UIDisplay → Shows header and menu
5. UserInput → Selects mode (deep clean vs. configure)
6. ProcessRegistration → Registers enabled steps with ProcessMonitor
7. ParallelExecution → Starts all processes as threads
8. MonitoringLoop → Continuously checks thread status
   - Detects completion/failure
   - Auto-restarts failed processes
   - Updates progress
9. ResultCollection → Gathers results from all threads
10. FinalReport → Displays status and completion message


THREADING MODEL
===============

ProcessMonitor uses threading for each cleanup function:
- Main thread: User interaction and monitoring
- Worker threads: Each cleanup function runs independently
- Thread-safe: Uses locks for shared state access
- Queue-based: Status updates via thread-safe queue
- Non-blocking: Monitor can restart while others run


MONITORING & RECOVERY
=====================

Each process has:
- Status tracking (pending → running → completed/failed)
- Start/end timestamps
- Error logging
- Restart counter (max 3 attempts)
- Result storage

Failure handling:
1. Process fails or crashes
2. Monitor detects failure via queue
3. Auto-restart triggered (if attempts < 3)
4. User notified of restart attempt
5. If max restarts exceeded, logs as fatal error
6. Continues with other processes


MEMORY & PERFORMANCE
====================

- Threading: Lower overhead than multiprocessing
- Shared memory: Thread-safe via locks
- Queue-based communication: Minimal memory footprint
- Status polling: 2-second default timeout (user-configurable)
- Result caching: Stores function return values for reporting


NEW vs. LEGACY
==============

LEGACY (cleaner.py)
- monolithic class-based design
- sequential step execution
- single thread
- limited error recovery

NEW (main.py + resources/)
- modular function-based design
- parallel step execution
- multithreaded processing
- auto-restart on failure
- real-time monitoring
- scalable architecture


ADDING NEW CLEANUP FUNCTIONS
=============================

To add a new cleanup step:

1. Create new file in resources/ (e.g., resources/cleanup_cache.py)
2. Define primary function: def cleanup_cache() -> bool:
3. Import in main.py: from resources.cleanup_cache import cleanup_cache
4. Add to CleanupManager.run_cleanup():
   - Add to step_funcs dictionary
   - Register with monitor
5. Update self.steps dict for UI display
6. Test standalone first
7. Test with manager
8. Update documentation


TESTING
=======

Test individual modules:
    python -c "from resources.kill_processes import kill_processes; kill_processes()"

Test with manager (dry run):
    python main.py
    # Select mode 2 (configure)
    # Toggle steps to test specific functions

Full cleanup:
    python main.py
    # Select mode 1 (deep clean)


TROUBLESHOOTING
===============

Processes not starting:
- Check imports in main.py
- Verify function signatures return bool
- Check for import errors in module files

Threading issues:
- Verify thread-safe operations in helper functions
- Check for shared state without locks
- Look for blocking calls

Permission errors:
- Ensure admin elevation before cleanup
- Check individual function error handling

Timeout issues:
- Increase timeout in wait_for_completion()
- Check for hanging subprocess calls
- Verify PowerShell command timeouts


FUTURE ENHANCEMENTS
====================

- Configuration file for cleanup preferences
- Logging to file for audit trail
- Dry-run mode (preview what would be deleted)
- Progress percentage reporting
- Cleanup profile saving/loading
- Multi-step recovery and resumption
- Cleanup history/rollback capability
- Performance metrics and timing
- Network-based progress monitoring
