"""
USER GUIDE - P2P File Sharing Application
"""

# ============================================================================
# TABLE OF CONTENTS
# ============================================================================
"""
1. Getting Started
2. User Interface Overview
3. Basic Operations
4. Advanced Features
5. Network Concepts
6. Best Practices
7. FAQ
"""

# ============================================================================
# 1. GETTING STARTED
# ============================================================================

"""
Starting the Application:

Windows:
- Double-click run.bat
- Or: python ui/main_app.py

Linux/macOS:
- Terminal: python3 ui/main_app.py

Expected Output:
- A window titled "P2P File Sharing Application" opens
- "Status: Offline" is shown at the bottom
- Activity Log shows initialization messages
"""

# ============================================================================
# 2. USER INTERFACE OVERVIEW
# ============================================================================

"""
The main window is divided into 4 main sections:

┌─────────────────────────────────────────────────────────────────┐
│  P2P File Sharing Application                                   │
├────────────────────────────────────────────────────────────────┤
│ Control Panel                                                    │
│ Your Name: [Peer-XXXX]  [Start Server] [Stop] [Refresh Peers]  │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Connected Peers │ Shared Files │ Activity Log │                 │
│ ────────────    │ ────────────  │ ────────────                  │
│ [List]          │ [List]        │ [Text Box]                    │
│ ────────────    │ ────────────  │ ────────────                  │
│ [Actions]       │ [Actions]     │                               │
│                                                                  │
├────────────────────────────────────────────────────────────────┤
│ Status: Online    IP: 192.168.1.100:5000                       │
└────────────────────────────────────────────────────────────────┘

Key Components:

1. CONTROL PANEL
   - Your Name: Set your display name (default: Peer-XXXX)
   - Start Server: Begin P2P server
   - Stop Server: Stop P2P server
   - Refresh Peers: Manually refresh peer list

2. CONNECTED PEERS
   - Shows all discovered peers on the LAN
   - Displays peer name and IP address
   - Actions:
     * Connect to Peer: Manually add a peer by IP

3. SHARED FILES
   - Lists all files you're sharing
   - Shows file name and size
   - Actions:
     * Add File: Add file to share
     * Remove File: Stop sharing a file
     * Refresh: Update file list

4. ACTIVITY LOG
   - Real-time log of all network activities
   - Shows timestamps for each event
   - Useful for debugging and monitoring
"""

# ============================================================================
# 3. BASIC OPERATIONS
# ============================================================================

"""
OPERATION 1: Starting the Server
─────────────────────────────────

Step 1: Enter your name (or use default)
Step 2: Click "Start Server" button
Step 3: Confirm:
        - Status changes to "Online" (green)
        - IP address shows (e.g., 192.168.1.100:5000)
        - Activity log shows "Server started successfully"

Result:
- Your peer is now discoverable on the LAN
- Other peers can connect to you
- Your P2P server is listening on port 5000


OPERATION 2: Adding Files to Share
────────────────────────────────

Step 1: Click "Add File" button
Step 2: Browse dialog opens
Step 3: Select a file from your computer
Step 4: File is copied to shared directory
Step 5: Confirm:
        - File appears in "Shared Files" list
        - Shows file name and size
        - Activity log shows "File added: [filename]"

Result:
- File is now available for other peers to download
- File copy is in ./shared_files/ directory
- Original file is unchanged


OPERATION 3: Removing Files from Share
──────────────────────────────────

Step 1: Select file in "Shared Files" list
Step 2: Click "Remove File" button
Step 3: Confirm:
        - File disappears from list
        - Activity log shows "File removed: [filename]"

Result:
- File is deleted from shared directory
- No longer available to other peers


OPERATION 4: Discovering Peers
───────────────────────────

Automatic:
- When you start server, automatic peer discovery begins
- Every 3 seconds, your peer broadcasts a discovery message
- Other peers respond with their information
- Connected Peers list updates automatically

Manual:
Step 1: Click "Refresh Peers" button
Step 2: List updates with discovered peers
Step 3: Each entry shows: [Peer Name] ([IP]:[Port])

Result:
- See all other peers currently online on LAN
- Can manually refresh if needed


OPERATION 5: Connecting to a Peer
──────────────────────────────

Step 1: Click "Connect to Peer" button
Step 2: Dialog box opens
Step 3: Enter peer details:
        - Peer IP: e.g., 192.168.1.50
        - Peer Port: e.g., 5000
Step 4: Click "Connect" button
Step 5: Confirm:
        - Activity log shows connection result
        - Peer appears in "Connected Peers" list (if successful)

Result:
- Direct connection established with peer
- Can now transfer files with connected peer


OPERATION 6: Downloading Files from a Peer
─────────────────────────────────────

Step 1: Connect to a peer (See Operation 5)
Step 2: Access their shared files (requires connection)
Step 3: Select file to download
Step 4: Download starts automatically
Step 5: Confirm:
        - Activity log shows download progress
        - File saved to your downloads directory
        - Status message shows completion

Result:
- File transferred to your machine
- Original file remains on peer's machine
"""

# ============================================================================
# 4. ADVANCED FEATURES
# ============================================================================

"""
FEATURE 1: Multiple Peer Connections
─────────────────────────────────

You can connect to multiple peers simultaneously:

Example:
- Connect to Peer A (192.168.1.50)
- Connect to Peer B (192.168.1.75)
- Connect to Peer C (192.168.1.100)

All three peers appear in "Connected Peers" list
Can transfer files with any peer independently


FEATURE 2: Activity Monitoring
──────────────────────────

The Activity Log shows:
- Server events: [Time] Server started on 0.0.0.0:5000
- Peer events: [Time] Peer connected: John (192.168.1.50)
- File events: [Time] File added: document.pdf (2.5 MB)
- Network events: [Time] Connected to 192.168.1.50:5000
- Error events: [Time] Error: Connection refused

Benefits:
- Track all network activity
- Identify problems quickly
- Monitor file transfers
- See connection attempts


FEATURE 3: Network Discovery
───────────────────────

How it works:
1. Each peer broadcasts UDP packets to the LAN
2. Other peers receive and respond
3. Information exchanged includes:
   - Peer ID (unique identifier)
   - Peer Name (user-defined)
   - IP Address
   - Port Number
4. Peers maintain a list of active peers

UDP Broadcast Details:
- Port: 5001
- Message format: JSON
- Interval: Every 3 seconds
- Scope: Limited to LAN


FEATURE 4: File Transfer Protocol
──────────────────────────────

Transfer Process:
1. Sender initiates connection to receiver's port 5000
2. Sends file metadata (name, size, hash)
3. Receiver accepts or rejects
4. File transmitted in 4KB chunks
5. Chunks sent sequentially
6. Receiver writes chunks to disk
7. Transfer complete when all bytes received

Benefits:
- Handles large files efficiently
- Chunked transfer prevents memory overflow
- Can resume interrupted transfers (future)
- Sequential transfer ensures data integrity
"""

# ============================================================================
# 5. NETWORK CONCEPTS
# ============================================================================

"""
CONCEPT 1: What is Peer-to-Peer (P2P)?
──────────────────────────────────

Traditional Client-Server:
[Client 1] \
            └─> [Central Server] <─┘ [Client 2]
[Client 3] /

Peer-to-Peer:
[Peer 1] <──────> [Peer 2]
  ^                  ^
  └──────────┬───────┘
          [Peer 3]

In P2P:
- Each computer is both client AND server
- Direct connections between peers
- No central authority
- Scalable and distributed
- Resilient (no single point of failure)


CONCEPT 2: Local Area Network (LAN)
────────────────────────────────

LAN = Network of computers in close proximity

Examples:
- Office network
- School network
- Home WiFi network
- Coffee shop WiFi

Characteristics:
- High speed (100 Mbps - 10 Gbps)
- Low latency (< 1 ms)
- All devices share same network prefix (e.g., 192.168.1.x)
- Broadcast capable (can send to all at once)

IP Address Ranges:
- 192.168.0.0 - 192.168.255.255 (most common)
- 10.0.0.0 - 10.255.255.255
- 172.16.0.0 - 172.31.255.255


CONCEPT 3: Network Ports
─────────────────────

What is a Port?
- Logical endpoint on a machine
- Numbers 0-65535
- Each service uses specific ports

Common Ports:
- 80: HTTP (Web)
- 443: HTTPS (Secure Web)
- 22: SSH (Remote Access)
- 5000-5001: Our application


CONCEPT 4: TCP vs UDP
──────────────────

TCP (Transmission Control Protocol):
- Reliable delivery
- Ordered packets
- Error checking
- Used for: File transfers, Web, Email
- Used by our app for: File transfers (port 5000)

UDP (User Datagram Protocol):
- Fast, connectionless
- No guarantee of delivery
- Lower overhead
- Used for: Video streaming, Gaming, VoIP
- Used by our app for: Peer discovery (port 5001)


CONCEPT 5: Socket Communication
──────────────────────────────

Socket = Virtual connection point

Server Socket:
- Listens on specific port
- Waits for connections
- Example: Port 5000 listening for peers

Client Socket:
- Initiates connection to server
- Sends/receives data
- Example: Connecting to peer's port 5000

Flow:
1. Server creates listening socket on port 5000
2. Client creates connection socket
3. Client connects to server's IP:5000
4. Connection established
5. Bidirectional communication possible
6. Both parties can send/receive data
"""

# ============================================================================
# 6. BEST PRACTICES
# ============================================================================

"""
BEST PRACTICE 1: Security
──────────────────────

DO:
✓ Only add files you want to share
✓ Use firewall to restrict ports if needed
✓ Verify peer identities before connecting
✓ Keep application updated

DON'T:
✗ Share sensitive personal files
✗ Disable firewall completely
✗ Connect to unknown IP addresses
✗ Share files with sensitive data


BEST PRACTICE 2: Performance
────────────────────────

DO:
✓ Use wired connection for large files
✓ Limit simultaneous transfers
✓ Close unused applications
✓ Monitor Activity Log for errors

DON'T:
✗ Transfer multiple large files at once
✗ Run on weak WiFi
✗ Run too many peer instances
✗ Ignore error messages


BEST PRACTICE 3: File Management
───────────────────────────

DO:
✓ Organize files in shared directory
✓ Use descriptive file names
✓ Keep shared files updated
✓ Regularly remove old files

DON'T:
✗ Share executable files unless necessary
✗ Use special characters in filenames
✗ Fill shared directory with unnecessary files
✗ Modify files during transfer


BEST PRACTICE 4: Network Connectivity
──────────────────────────────────

DO:
✓ Ensure all peers on same network
✓ Keep network stable
✓ Use static IPs if possible
✓ Test connectivity before transfers

DON'T:
✗ Disconnect during active transfers
✗ Change network during session
✗ Use public WiFi if possible
✗ Expect WAN connectivity (not supported)
"""

# ============================================================================
# 7. FAQ
# ============================================================================

"""
Q1: How do I find my IP address?
A: The application shows it in the status bar when server starts
   Or: Open Command Prompt and type: ipconfig

Q2: Can I share files across the internet?
A: No, only on LAN. For internet sharing, need additional setup
   (VPN, NAT configuration, etc.)

Q3: What's the maximum file size?
A: Limited by available disk space
   Default limit: 5 GB (configurable in config.py)

Q4: Can I share an entire folder?
A: Currently only individual files
   Future version may add folder support

Q5: What if I can't connect to a peer?
A: Check:
   - Peer is online (visible in Peers list)
   - IP address is correct
   - Firewall isn't blocking port 5000
   - Both on same network

Q6: How do I change the share directory?
A: Default: ./shared_files/
   Edit in config.py: FILE_CONFIG['SHARED_FILES_DIR']

Q7: Can multiple files transfer simultaneously?
A: Currently sequential (one at a time)
   Future version may add parallel transfers

Q8: What happens if transfer is interrupted?
A: Currently: Partial file is saved
   Future: Resume capability will be added

Q9: Is data encrypted?
A: No encryption by default
   Future: Encryption options may be added

Q10: How do I backup my files?
A: Copy entire ./shared_files/ directory to another location
"""

# ============================================================================
# END OF USER GUIDE
# ============================================================================
