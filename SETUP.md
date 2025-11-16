"""
SETUP AND INSTALLATION GUIDE
P2P File Sharing Application
"""

# ============================================================================
# QUICK START
# ============================================================================

# On Windows, simply run:
# 1. Double-click run.bat
# 2. Or open Command Prompt and execute: python ui/main_app.py

# ============================================================================
# DETAILED SETUP INSTRUCTIONS
# ============================================================================

## Prerequisites
- Windows/Linux/macOS with Python 3.6 or higher
- Administrator access to install software (if needed)
- Basic networking knowledge

## Installation Steps

### Step 1: Check Python Installation
1. Open Command Prompt (Windows) or Terminal (Linux/Mac)
2. Type: python --version
3. Should show Python 3.6 or higher

If not installed:
- Download from: https://www.python.org/downloads/
- During installation, CHECK "Add Python to PATH"
- Verify installation again with: python --version

### Step 2: Navigate to Project Directory
```
cd path\to\peer-to-peer-file-sharing-application
```

### Step 3: Verify tkinter (usually pre-installed)
```
python -m tkinter
```
A small window should appear confirming tkinter works.

### Step 4: Create Virtual Environment (Optional but Recommended)
```
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate
```

### Step 5: Run the Application
```
python ui/main_app.py
```

## Testing the Application

### Single Machine Test
1. Start the application (Peer 1)
2. Click "Start Server"
3. Open another instance on the same machine or another terminal
4. Start the second peer (Peer 2)
5. Click "Start Server"
6. Note the IP address shown (should be same LAN)

### File Sharing Test
1. In Peer 1, click "Add File" and select a test file
2. File should appear in Peer 1's "Shared Files" list
3. In Peer 2, click "Connect to Peer"
4. Enter Peer 1's IP (usually 192.168.x.x) and port 5000
5. If successful, Peer 1 should appear in Peer 2's "Connected Peers" list

### Multi-Machine Test
1. On Machine A: Start the application and click "Start Server"
   - Note the IP address shown
2. On Machine B: Start the application and click "Start Server"
3. In Machine B, click "Connect to Peer"
4. Enter Machine A's IP address and port 5000
5. Connection should establish
6. Add files on Machine A and download on Machine B

## Troubleshooting

### Issue: "Python not found" or "python: command not found"
Solution:
- Make sure Python is added to PATH environment variable
- Reinstall Python with "Add Python to PATH" checked
- Or use full path: C:\Python39\python.exe ui/main_app.py

### Issue: "No module named tkinter"
Solution:
- Windows: Reinstall Python and select "tcl/tk and IDLE"
- Linux: Install tkinter package:
  - Ubuntu/Debian: sudo apt-get install python3-tk
  - Fedora: sudo dnf install python3-tkinter
  - macOS: Usually pre-installed with Python

### Issue: Peers not discovering each other
Solution:
- Check both peers are on same network
- Disable Windows Firewall temporarily for testing:
  - Windows: Settings > Firewall & network protection > Allow app through firewall
- Check if ports 5000-5001 are not blocked by firewall
- Verify with: netstat -an | findstr 5000

### Issue: File transfer fails
Solution:
- Check file exists and is readable
- Verify target directory has write permissions
- Ensure sufficient disk space on receiving machine
- Check network connectivity

### Issue: UI freezes during operation
Solution:
- Operations are threaded, but very large files may appear to freeze
- Check activity log for status updates
- Wait for operation to complete

## Logs and Debug

The Activity Log in the application shows:
- Server start/stop events
- Peer connections
- File additions/removals
- File transfers
- Network errors

## Performance Tips

1. **For large files**: 
   - Ensure good network connectivity
   - Avoid simultaneous large transfers
   - Close unnecessary applications to free resources

2. **For many peers**:
   - Each peer requires its own connection thread
   - Limit to reasonable number of peers on same machine
   - Consider increasing BUFFER_SIZE in config.py for faster transfers

3. **For stability**:
   - Keep application updated
   - Restart application if experiencing lag
   - Monitor Activity Log for errors

## File Locations

- Shared files directory: ./shared_files/
- Application code: ./ui/ and ./src/
- Configuration: ./config.py
- Launcher script: ./run.bat (Windows only)

## Network Ports Used

- 5000: TCP - P2P server for peer connections
- 5001: UDP - Peer discovery broadcast

Make sure these ports are available on your machine.

## Next Steps

1. Read README.md for feature documentation
2. Review config.py to customize settings
3. Explore the source code in src/ directory
4. Check ui/main_app.py for UI customization options

## Support and Issues

If you encounter issues:
1. Check the Activity Log for error messages
2. Review the Troubleshooting section above
3. Verify your network connectivity
4. Check that Python and tkinter are properly installed
5. Review the source code comments for implementation details
