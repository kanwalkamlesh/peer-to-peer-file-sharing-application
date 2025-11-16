"""
QUICK REFERENCE & TROUBLESHOOTING GUIDE
P2P File Sharing Application
"""

# ============================================================================
# QUICK REFERENCE CARD
# ============================================================================

"""
╔════════════════════════════════════════════════════════════════╗
║            QUICK REFERENCE - P2P FILE SHARING APP             ║
╚════════════════════════════════════════════════════════════════╝

STARTING THE APP:
  Windows:  Double-click run.bat  OR  python ui/main_app.py
  Linux:    python3 ui/main_app.py
  macOS:    python3 ui/main_app.py

KEY BUTTONS:
  [Start Server]       → Begin P2P server (becomes green)
  [Stop Server]        → Stop P2P server
  [Refresh Peers]      → Manually refresh peer list
  [Add File]           → Select file to share
  [Remove File]        → Stop sharing selected file
  [Connect to Peer]    → Connect to specific peer

DEFAULT PORTS:
  5000 = P2P Server (TCP)
  5001 = Peer Discovery (UDP)

DEFAULT DIRECTORY:
  ./shared_files/

KEY FILES:
  main_app.py        = Main UI application
  network_manager.py = Networking core
  file_manager.py    = File operations
  config.py          = Settings

STATUS INDICATORS:
  Status: Offline (red)    = Server not running
  Status: Online (green)   = Server running
  IP: xxx.xxx.xxx.xxx:5000 = Your connection address

╔════════════════════════════════════════════════════════════════╗
║                    KEYBOARD SHORTCUTS                         ║
╚════════════════════════════════════════════════════════════════╝

Tab              = Navigate between elements
Enter            = Activate button
Escape           = Close dialog
Ctrl+C           = Force quit (terminal)

"""

# ============================================================================
# TROUBLESHOOTING GUIDE
# ============================================================================

"""
╔════════════════════════════════════════════════════════════════╗
║                    TROUBLESHOOTING GUIDE                      ║
╚════════════════════════════════════════════════════════════════╝

PROBLEM 1: "ModuleNotFoundError: No module named 'tkinter'"
─────────────────────────────────────────────────────────────

Symptom:
  Error message appears when starting application

Causes:
  - Python installed without tkinter
  - Wrong Python version
  - tkinter not in PATH

Solutions:

  Windows:
  1. Uninstall Python
  2. Download from python.org
  3. Run installer
  4. CHECK "tcl/tk and IDLE" during installation
  5. CHECK "Add Python to PATH"
  6. Reinstall and retry

  Linux (Ubuntu/Debian):
  $ sudo apt-get install python3-tk
  $ sudo apt-get install python3-dev

  Linux (Fedora):
  $ sudo dnf install python3-tkinter

  macOS:
  Usually pre-installed, try:
  $ python3 -m tkinter


PROBLEM 2: "Address already in use" error
──────────────────────────────────────────

Symptom:
  Error when trying to start server
  Port 5000 already in use

Causes:
  - Another app using port 5000
  - Previous app didn't close properly
  - Multiple instances of our app

Solutions:

  Option 1 - Wait for release:
    Wait 30-60 seconds for OS to release port

  Option 2 - Change port in code:
    Edit ui/main_app.py line ~40:
    self.network_manager = NetworkManager(port=5001)

  Option 3 - Force close process:
    Windows Command Prompt:
    $ netstat -ano | findstr :5000
    $ taskkill /PID <PID> /F

    Linux/macOS Terminal:
    $ lsof -i :5000
    $ kill -9 <PID>

  Option 4 - Restart computer:
    (Nuclear option - works every time)


PROBLEM 3: Peers not showing up in list
────────────────────────────────────────

Symptom:
  Connected Peers list is empty
  Can't see other computers on network

Causes:
  - Other peer hasn't started server
  - Different network/subnet
  - Firewall blocking
  - Discovery mechanism not working

Solutions:

  Step 1 - Verify other peer is online:
    Ask other user to check if server is running
    Status should show "Online" (green)

  Step 2 - Verify network connectivity:
    Both machines on same WiFi/network?
    Ping test (Windows):
      $ ping 192.168.1.100
    If packet loss, network issue

  Step 3 - Check firewall:
    Windows Defender Firewall:
    1. Control Panel > Firewall > Allow app through
    2. Find Python.exe
    3. Check "Public" and "Private"

    Third-party firewall:
    Add exception for port 5000 and 5001

  Step 4 - Manual connection:
    Use "Connect to Peer" button instead
    Enter peer's IP directly
    If this works, discovery mechanism needs help

  Step 5 - Activity Log inspection:
    Check for error messages in Activity Log
    Might reveal specific problem


PROBLEM 4: Cannot connect to specific peer
───────────────────────────────────────────

Symptom:
  "Connect to Peer" button clicked
  Dialog shows IP and port
  Connection fails

Causes:
  - Wrong IP address
  - Wrong port number
  - Peer server not running
  - Firewall blocking connection
  - Network path blocked

Solutions:

  Step 1 - Verify IP address:
    On target peer:
    - Look at status bar "IP: xxx.xxx.xxx.xxx:5000"
    - Enter exact same IP in dialog

  Step 2 - Verify port:
    Default port is 5000
    If changed, must enter same port
    Check config.py or code

  Step 3 - Verify target is online:
    Target should have "Status: Online"
    Activity Log should show "Server started"

  Step 4 - Test network path:
    Windows Command Prompt:
    $ ping <IP>          (should respond)
    $ telnet <IP> 5000   (should connect)

    Linux/macOS Terminal:
    $ ping <IP>
    $ nc -zv <IP> 5000

  Step 5 - Disable firewall temporarily:
    Windows:
    Settings > Firewall > Turn off (temporarily)
    Try connection again
    If it works, firewall is blocking
    Add permanent exception

  Step 6 - Check activity log:
    Look for specific error messages
    Copy error text for debugging


PROBLEM 5: File not showing up after adding
────────────────────────────────────────────

Symptom:
  Clicked "Add File"
  Selected file
  File doesn't appear in Shared Files list

Causes:
  - File copy failed
  - Permission denied
  - Shared directory doesn't exist
  - File already exists with same name

Solutions:

  Step 1 - Check for error messages:
    Look in Activity Log for errors
    May show specific reason

  Step 2 - Verify file permissions:
    File should be readable
    Right-click file > Properties > Check read permission

  Step 3 - Verify shared directory:
    Check if ./shared_files/ exists
    If not, create it manually

  Step 4 - Check disk space:
    Ensure enough free space
    File size should fit on disk

  Step 5 - Try different file:
    Use smaller test file
    Try different file format
    Try file from different location

  Step 6 - Manual file copy:
    Copy file to ./shared_files/ manually
    Click "Refresh" button
    File should appear


PROBLEM 6: File transfer fails
──────────────────────────────

Symptom:
  Started file transfer
  Transfer appears stuck
  Error in Activity Log
  Transfer didn't complete

Causes:
  - Network connection dropped
  - Insufficient disk space
  - File too large
  - Permission denied on destination
  - Transfer timeout

Solutions:

  Step 1 - Check network connection:
    Both peers still connected to network?
    Ping each other
    WiFi signal strength OK?

  Step 2 - Check available disk space:
    Windows: C: drive properties
    Linux: df -h
    Ensure enough space for file

  Step 3 - Check file permissions:
    Source file readable?
    Destination directory writable?
    No permission issues?

  Step 4 - Check firewall (again):
    Might interfere with ongoing connection
    Temporarily disable if needed

  Step 5 - Try smaller file:
    Test with small test file (1 MB)
    If small file works, large file might timeout

  Step 6 - Retry transfer:
    Network might be temporarily slow
    Wait and try again
    Future version will have resume

  Step 7 - Check Activity Log:
    Look for specific error messages
    "Error sending file: ..."
    "Error receiving file: ..."


PROBLEM 7: Application freezes/not responding
──────────────────────────────────────────────

Symptom:
  UI stops responding to clicks
  Window title shows "[Not Responding]"
  Activity Log stops updating

Causes:
  - Long operation (large file transfer)
  - Network timeout
  - Infinite loop in code
  - System resource exhaustion

Solutions:

  Step 1 - Wait:
    Long operations take time
    Wait 30-60 seconds
    Large files may appear frozen

  Step 2 - Check Activity Log:
    Look at last message
    Might indicate what's happening

  Step 3 - Check network:
    Ensure network still connected
    Try ping in another terminal
    If network down, app will wait for timeout

  Step 4 - Force quit:
    Windows:
      Alt+F4  (closes window)
      Ctrl+C  (in Command Prompt)
      Task Manager > End Task

    Linux/macOS:
      Cmd+Q  (macOS)
      Ctrl+C  (Terminal)
      killall python3

  Step 5 - Prevent freezing:
    Don't transfer huge files
    Avoid poor network
    Keep system resources available


PROBLEM 8: Activity Log filling up with errors
───────────────────────────────────────────────

Symptom:
  Many "[ERROR]" messages in Activity Log
  Pattern of repeated errors
  Performance might degrade

Causes:
  - Network instability
  - Firewall blocking repeatedly
  - Discovery loop errors
  - Connection attempts to offline peers

Solutions:

  Step 1 - Read error messages:
    Copy specific error
    Search this guide or README

  Step 2 - Check network:
    Is WiFi stable?
    Try wired connection
    Check signal strength

  Step 3 - Check firewall logs:
    Might be blocking legitimate traffic
    Adjust firewall rules

  Step 4 - Restart application:
    Stop server
    Close application
    Reopen and start fresh

  Step 5 - Reduce peer count:
    Too many connection attempts?
    Connect to fewer peers
    Cleaner error log


PROBLEM 9: Python not found / command not recognized
────────────────────────────────────────────────────

Symptom:
  Error: "python: command not found"
  Error: "'python' is not recognized"
  In terminal when typing python

Causes:
  - Python not installed
  - Python not in PATH
  - Python installed but not configured
  - Using wrong terminal

Solutions:

  Step 1 - Verify Python installed:
    Open new Command Prompt
    Type: python --version
    Should show Python 3.x.x

  Step 2 - Windows PATH issue:
    1. Uninstall Python (Add/Remove Programs)
    2. Download Python installer
    3. Run installer
    4. IMPORTANT: Check "Add Python to PATH"
    5. Continue with installation
    6. Restart Command Prompt
    7. Test: python --version

  Step 3 - Alternative command:
    Try: python3 ui/main_app.py
    Try: py ui/main_app.py

  Step 4 - Use full path:
    Windows (example):
    "C:\Program Files\Python39\python.exe" ui/main_app.py

    Linux (example):
    /usr/bin/python3 ui/main_app.py


PROBLEM 10: "Permission denied" errors
──────────────────────────────────────

Symptom:
  File operations fail with permission error
  Can't write to shared_files directory
  Can't delete files

Causes:
  - Directory permissions too restrictive
  - Running without required privileges
  - File locked by another process
  - Read-only filesystem

Solutions:

  Windows:
  1. Right-click shared_files folder
  2. Properties > Security > Edit
  3. Select your user
  4. Check all boxes
  5. Apply

  Linux:
  $ chmod 755 shared_files/
  $ chmod 755 shared_files/*

  macOS:
  $ chmod 755 shared_files/
  $ chmod 755 shared_files/*

  If running as different user:
  Change directory ownership
  $ chown -R username:group shared_files/


"""

# ============================================================================
# DIAGNOSTIC COMMANDS
# ============================================================================

"""
Run these commands to diagnose problems:

1. CHECK PYTHON INSTALLATION:
   $ python --version
   Expected: Python 3.6+

2. CHECK TKINTER:
   $ python -m tkinter
   Expected: Small window appears

3. TEST NETWORK (Windows):
   $ ipconfig
   Shows your IP address
   
   $ ping 192.168.1.50
   Tests connectivity (replace with peer IP)

   $ netstat -an | findstr 5000
   Shows if port 5000 is in use

4. TEST NETWORK (Linux/macOS):
   $ ifconfig or $ ip addr
   Shows your IP address
   
   $ ping 192.168.1.50
   Tests connectivity
   
   $ lsof -i :5000
   Shows if port 5000 is in use

5. CHECK PYTHON MODULES:
   $ python -c "import socket; print('socket OK')"
   $ python -c "import threading; print('threading OK')"
   $ python -c "import tkinter; print('tkinter OK')"

"""

# ============================================================================
# GETTING HELP
# ============================================================================

"""
If you're stuck:

1. CHECK ACTIVITY LOG:
   - Look for error messages
   - Most common issues shown there
   - Copy exact error text

2. READ DOCUMENTATION:
   - README.md - Overview
   - SETUP.md - Installation
   - USER_GUIDE.md - Operations
   - ARCHITECTURE.md - Technical details

3. COMMON SOLUTIONS:
   - Restart application
   - Restart computer
   - Disable firewall temporarily
   - Use manual peer connection

4. LAST RESORT:
   - Fresh install (delete, re-download)
   - Different Python version
   - Different machine for testing
   - Ask for help (include error messages)

"""

# ============================================================================
# END OF TROUBLESHOOTING GUIDE
# ============================================================================
