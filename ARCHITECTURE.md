"""
ARCHITECTURE DOCUMENTATION
P2P File Sharing Application

This document describes the system architecture and design patterns.
"""

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

"""
peer-to-peer-file-sharing-application/
│
├── src/                           [Core Application Logic]
│   ├── __init__.py               [Package initialization]
│   ├── network_manager.py        [P2P networking & peer discovery]
│   └── file_manager.py           [File operations & management]
│
├── ui/                            [User Interface]
│   ├── main_app.py               [Main GUI application]
│   └── enhanced_ui.py            [Advanced UI components]
│
├── shared_files/                  [Shared file storage directory]
│   └── (user files)
│
├── config.py                      [Configuration settings]
├── requirements.txt               [Python dependencies]
├── run.bat                        [Windows launcher script]
├── README.md                      [Project overview]
├── SETUP.md                       [Installation & setup guide]
├── USER_GUIDE.md                  [User documentation]
└── ARCHITECTURE.md                [This file]
"""

# ============================================================================
# SYSTEM ARCHITECTURE DIAGRAM
# ============================================================================

"""
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                        │
│                    (Tkinter-based GUI)                           │
│                                                                   │
│  ┌─────────────┬──────────────┬──────────────┬──────────────┐   │
│  │   Control   │   Peers      │   Shared     │   Activity   │   │
│  │   Panel     │   Display    │   Files      │   Log        │   │
│  └──────┬──────┴──────┬───────┴──────┬───────┴──────┬───────┘   │
│         │             │              │               │           │
├─────────┼─────────────┼──────────────┼───────────────┼──────────┤
│          │             │              │               │          │
│ APPLICATION LOGIC LAYER (Business Logic)              │          │
│                                                       │          │
│  ┌─────────────────────────────────────────────┐    │          │
│  │  File Manager Module                        │    │          │
│  │  - Add files                                │    │          │
│  │  - Remove files                             │    │          │
│  │  - Get file list                            │    │          │
│  │  - Format file sizes                        │    │          │
│  └─────────────────────────────────────────────┘    │          │
│                                                       │          │
│  ┌─────────────────────────────────────────────┐    │          │
│  │  Network Manager Module                     │◄───┘          │
│  │  - Start/stop server                        │               │
│  │  - Peer discovery                           │               │
│  │  - Connection handling                      │               │
│  │  - File transfer protocol                   │               │
│  │  - Socket communication                     │               │
│  └─────────────────────────────────────────────┘               │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                    NETWORK LAYER                                  │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │  TCP Server      │         │  UDP Discovery   │              │
│  │  (Port 5000)     │         │  (Port 5001)     │              │
│  │                  │         │                  │              │
│  │ - Listen         │         │ - Broadcast      │              │
│  │ - Accept conns   │         │ - Respond        │              │
│  │ - Send files     │         │ - Discover peers │              │
│  │ - Recv files     │         │                  │              │
│  └────────┬─────────┘         └─────────┬────────┘              │
│           │                             │                       │
│           └──────────────┬──────────────┘                       │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │   LAN        │
                    │   Network    │
                    │              │
                    │ (Ethernet/   │
                    │  WiFi)       │
                    └──────────────┘
"""

# ============================================================================
# MODULE DESCRIPTIONS
# ============================================================================

"""
1. NETWORK MANAGER (src/network_manager.py)
   ─────────────────────────────────────────

   Purpose: Handle all network communication and peer discovery

   Key Classes:
   - NetworkManager: Main class for P2P networking

   Key Methods:
   - start()                    : Start P2P server
   - stop()                     : Stop P2P server
   - connect_to_peer()          : Connect to specific peer
   - send_file()                : Send file to peer
   - receive_file()             : Receive file from peer
   - get_peers()                : Get list of connected peers
   - _discover_peers()          : Discover peers on LAN
   - _listen_for_connections()  : Listen for incoming connections
   - _handle_peer_connection()  : Handle peer connection

   Threading:
   - Main thread: UI event loop
   - listen_thread: Listens for incoming connections
   - discover_thread: Broadcasts peer discovery
   - Connection threads: Handle each peer connection

   Networking Flows:

   a) Server Startup:
      1. Create TCP socket
      2. Bind to port 5000
      3. Set to listen mode
      4. Start listen_thread
      5. Start discover_thread

   b) Peer Discovery:
      1. Get local IP address
      2. Create UDP socket
      3. Send discovery broadcast (port 5001)
      4. Listen for responses
      5. Store responding peers in peers dictionary
      6. Repeat every 3 seconds

   c) Incoming Connection:
      1. Accept connection on port 5000
      2. Receive peer information (JSON)
      3. Store peer details
      4. Send acknowledgment
      5. Handle in separate thread

   d) Outgoing File Transfer:
      1. Create TCP connection to peer
      2. Send file metadata
      3. Wait for acceptance
      4. Send file in 4KB chunks
      5. Close connection


2. FILE MANAGER (src/file_manager.py)
   ──────────────────────────────────

   Purpose: Handle file operations and sharing directory management

   Key Classes:
   - FileManager: Main class for file operations

   Key Methods:
   - get_shared_files()    : Get list of files in shared directory
   - add_file_to_share()   : Copy file to shared directory
   - remove_shared_file()  : Delete file from shared directory
   - download_file()       : Download file from shared directory
   - _format_size()        : Format file size in human readable format
   - browse_file()         : Open file browser dialog
   - browse_directory()    : Open directory browser dialog

   File Management:
   - Shared directory: ./shared_files/
   - Files are copied (not moved) to shared directory
   - Original files remain unchanged
   - File list sorted alphabetically
   - Includes file metadata (name, path, size)


3. MAIN APPLICATION (ui/main_app.py)
   ──────────────────────────────────

   Purpose: Provide user interface and coordinate managers

   Key Classes:
   - P2PFileShareApp: Main application class

   Key Methods:
   - setup_ui()          : Setup user interface
   - start_server()      : Start P2P server
   - stop_server()       : Stop P2P server
   - add_file()          : Add file to sharing
   - remove_file()       : Remove file from sharing
   - refresh_files()     : Refresh file list display
   - refresh_peers()     : Refresh peer list display
   - connect_to_peer()   : Connect to specific peer
   - log_message()       : Log message to activity log

   UI Components:
   - Control Panel: Server control and peer name
   - Connected Peers: List of discovered peers
   - Shared Files: List of files being shared
   - Activity Log: Real-time event logging

   Threading:
   - Main thread: UI event loop and user interactions
   - Worker threads: Peer refresh, file operations


4. ENHANCED UI (ui/enhanced_ui.py)
   ───────────────────────────────

   Purpose: Provide advanced UI components and theming

   Key Classes:
   - ModernStyle: Theme configuration
   - StatusIndicator: Custom status indicator widget
   - FileTransferProgressBar: Progress bar for transfers
   - PeerCard: Card display for peer information
   - FileCard: Card display for file information
   - HoverButton: Button with hover effects
   - Tooltip: Tooltip widget for help text

   Features:
   - Color theming
   - Custom widgets
   - Status indicators
   - Progress visualization
   - Tooltip support
"""

# ============================================================================
# COMMUNICATION PROTOCOLS
# ============================================================================

"""
1. PEER DISCOVERY PROTOCOL (UDP)
   ────────────────────────────

   Message Format (JSON):
   {
       "type": "discovery",
       "peer_id": "abc12345",
       "ip": "192.168.1.100",
       "port": 5000,
       "name": "John's Computer"
   }

   Response Format:
   {
       "type": "discovery_response",
       "peer_id": "xyz98765",
       "ip": "192.168.1.50",
       "port": 5000,
       "name": "Jane's Computer"
   }

   Process:
   1. Send broadcast to 255.255.255.255:5001 every 3 seconds
   2. Listen on port 5001 for responses
   3. Update peer list with responses
   4. Timeout after 2 seconds
   5. Repeat cycle


2. PEER CONNECTION PROTOCOL (TCP)
   ──────────────────────────────

   Initial Connection:
   Client sends:
   {
       "peer_id": "abc12345",
       "name": "John's Computer",
       "port": 5000
   }

   Server responds:
   {
       "status": "connected",
       "peer_id": "abc12345"
   }


3. FILE TRANSFER PROTOCOL (TCP)
   ────────────────────────────

   File Transfer Request:
   {
       "type": "file_transfer",
       "file_name": "document.pdf",
       "file_size": 102400
   }

   Receiver Response:
   "accepted" or "rejected"

   File Transfer:
   - Raw file bytes sent in 4KB chunks
   - Sequential sending (no parallelization)
   - Receiver writes bytes to disk
   - Total bytes = file_size


4. DATA STRUCTURES
   ───────────────

   Peer Dictionary:
   {
       "peer_id": {
           "ip": "192.168.1.100",
           "port": 5000,
           "name": "John's Computer"
       }
   }

   File Information:
   {
       "name": "document.pdf",
       "path": "/full/path/to/document.pdf",
       "size": 102400,
       "size_readable": "100.00 KB"
   }
"""

# ============================================================================
# THREADING MODEL
# ============================================================================

"""
Thread Architecture:

┌─ Main Thread (Tkinter Event Loop)
│  ├─ UI Event Handling
│  ├─ User Interactions
│  └─ Log Updates
│
├─ Network Manager Threads
│  ├─ listen_thread (TCP Server)
│  │  └─ Accepts incoming peer connections
│  │
│  ├─ discover_thread (UDP Discovery)
│  │  └─ Broadcasts and listens for peers
│  │
│  └─ Per-Peer Connection Threads
│     └─ Handles each connected peer
│
└─ Application Threads
   ├─ Peer refresh thread
   ├─ File operation threads
   └─ Worker threads for long operations

Thread Safety:
- NetworkManager uses thread-safe dictionaries for peer storage
- UI updates happen in main thread via callbacks
- Socket operations are thread-safe
- File operations are isolated per file

Synchronization:
- Threading locks not heavily used (simplicity)
- Callbacks ensure UI thread safety
- Independent operations minimize conflicts
"""

# ============================================================================
# DATA FLOW EXAMPLES
# ============================================================================

"""
FLOW 1: Starting the Application
─────────────────────────────

User Action: Click "Start Server"
         │
         ▼
    start_server() in main_app.py
         │
         ├─ network_manager.start()
         │  ├─ Create TCP socket on port 5000
         │  ├─ Start listen_thread
         │  ├─ Start discover_thread
         │  └─ Return success/failure
         │
         ├─ Update UI (status, buttons)
         │
         ├─ log_message("Server started")
         │
         └─ auto_refresh() - Periodic peer refresh


FLOW 2: Adding a File to Share
────────────────────────────

User Action: Click "Add File"
         │
         ▼
    add_file() in main_app.py
         │
         ├─ Open file dialog
         │
         ├─ file_manager.add_file_to_share(path)
         │  ├─ Verify file exists
         │  ├─ Copy to ./shared_files/
         │  └─ Return success/failure
         │
         ├─ log_message("File added")
         │
         └─ refresh_files() - Update display


FLOW 3: Connecting to a Peer
──────────────────────────

User Action: Click "Connect to Peer"
         │
         ▼
    connect_to_peer() in main_app.py
         │
         ├─ Show connection dialog
         │
         ├─ Get peer IP and port
         │
         ├─ network_manager.connect_to_peer(ip, port, name)
         │  ├─ Create TCP socket
         │  ├─ Connect to ip:port
         │  ├─ Send peer info (JSON)
         │  ├─ Wait for acceptance
         │  └─ Return success/failure
         │
         ├─ log_message("Connected" or "Failed")
         │
         └─ refresh_peers() - Update display


FLOW 4: Receiving an Incoming Connection
─────────────────────────────────────

Network Event: Peer connects to port 5000
            │
            ▼
    TCP socket accepts connection
            │
            ▼
    _listen_for_connections() receives connection
            │
            ▼
    Spawn thread: _handle_peer_connection()
            │
            ├─ Receive peer info (JSON)
            ├─ Parse peer details
            ├─ Store in peers dictionary
            ├─ Send acknowledgment
            │
            └─ log_message("Peer connected")
"""

# ============================================================================
# DESIGN PATTERNS USED
# ============================================================================

"""
1. OBSERVER PATTERN
   ────────────────
   Used for: Callback system for UI updates
   Implementation: callback parameter in NetworkManager
   Example: log_message function passed as callback

2. SINGLETON PATTERN
   ──────────────────
   Used for: NetworkManager and FileManager instances
   Implementation: Single instance per application
   Example: One network_manager per app instance

3. THREAD POOL PATTERN (Implicit)
   ───────────────────────────────
   Used for: Handling multiple peer connections
   Implementation: Spawn thread per connection
   Benefit: Handles concurrent peers efficiently

4. MVC PATTERN (Implicit)
   ──────────────────────
   Model: NetworkManager and FileManager
   View: Tkinter UI (main_app.py)
   Controller: P2PFileShareApp class

5. FACTORY PATTERN (Implicit)
   ──────────────────────────
   Used for: Creating sockets and threads
   Implementation: Built into socket and threading modules
"""

# ============================================================================
# PERFORMANCE CONSIDERATIONS
# ============================================================================

"""
1. NETWORK PERFORMANCE
   ───────────────────

   TCP File Transfer:
   - 4KB chunk size (good balance)
   - Sequential transfer (simple implementation)
   - No compression (direct transfer)
   - Typical speed: Limited by network (100 Mbps - 1 Gbps)

   Peer Discovery:
   - UDP broadcast every 3 seconds
   - Low bandwidth usage
   - Quick response (< 1 second typically)

   Scalability:
   - Can handle 10-50 peers on typical LAN
   - Limited by thread count and network bandwidth
   - Sequential transfers limit file throughput


2. MEMORY USAGE
   ────────────

   Per Peer: ~1 KB (metadata storage)
   Per File: 4 KB buffer during transfer
   UI Components: ~10-50 MB total
   Typical Usage: 100-200 MB at runtime

   Optimization:
   - Streaming file transfer (not loaded into memory)
   - Efficient socket buffers
   - Cleanup of old connections


3. DISK I/O
   ────────

   File Operations:
   - Shutil.copy() for adding files (efficient)
   - Sequential read/write for transfers
   - No disk caching issues
   - Suitable for typical SSDs and HDDs

   Bottlenecks:
   - Slow disks may bottleneck transfers
   - Network usually faster than disk I/O
"""

# ============================================================================
# ERROR HANDLING
# ============================================================================

"""
Error Handling Strategy:

1. NETWORK ERRORS
   ──────────────
   - Connection refused: Log and notify user
   - Timeout: Retry or fail gracefully
   - Socket errors: Cleanup and log
   - Protocol errors: Validate JSON, handle gracefully

2. FILE ERRORS
   ───────────
   - File not found: Notify user
   - Permission denied: Request elevated privileges
   - Disk full: Warn before transfer
   - Invalid path: Validate input

3. THREADING ERRORS
   ─────────────────
   - Thread crashes: Log and continue
   - Deadlocks: Prevent with careful design
   - Race conditions: Minimize shared state

4. USER ERRORS
   ────────────
   - Invalid IP: Validate format
   - Invalid port: Validate range (0-65535)
   - Duplicate names: Allow duplicates (no conflict)
"""

# ============================================================================
# FUTURE ENHANCEMENTS
# ============================================================================

"""
1. SECURITY
   ────────
   - SSL/TLS encryption for transfers
   - User authentication
   - File integrity verification (hashing)
   - Access control lists

2. FEATURES
   ────────
   - Parallel file transfers
   - Directory sharing
   - File search functionality
   - Download history
   - Bandwidth throttling
   - Progress indicators

3. UI
   ───
   - Web-based interface
   - Multiple language support
   - Dark mode theming
   - Drag-and-drop file support
   - File preview

4. PERFORMANCE
   ────────────
   - Multi-threaded file transfer
   - Compression support
   - Caching strategies
   - Network optimization

5. NETWORKING
   ───────────
   - Internet file sharing (with VPN/proxy)
   - Multi-segment transfers
   - Automatic retry logic
   - Better peer discovery
"""

# ============================================================================
# DEPLOYMENT
# ============================================================================

"""
Development:
- Run from source: python ui/main_app.py
- Edit config.py for customization
- Debug using activity log

Production:
- Use .bat launcher (Windows)
- Consider packaging with PyInstaller
- Firewall configuration
- Network monitoring

Distribution:
- Package as ZIP file
- Include all .py files and config
- Documentation included
- No external dependencies required
"""

# ============================================================================
# END OF ARCHITECTURE DOCUMENTATION
# ============================================================================
