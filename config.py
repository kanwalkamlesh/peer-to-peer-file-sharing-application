"""
Configuration file for P2P File Sharing Application
"""

# Network Configuration
NETWORK_CONFIG = {
    'SERVER_PORT': 5000,          # Main server port for P2P connections
    'DISCOVERY_PORT': 5001,       # UDP broadcast port for peer discovery
    'BUFFER_SIZE': 4096,          # Size of data chunks for file transfer
    'DISCOVERY_INTERVAL': 3,      # Interval in seconds to broadcast discovery
    'CONNECTION_TIMEOUT': 5,      # Timeout for connection attempts in seconds
    'MAX_CONNECTIONS': 10,        # Maximum concurrent peer connections
}

# Application Configuration
APP_CONFIG = {
    'WINDOW_WIDTH': 1000,
    'WINDOW_HEIGHT': 700,
    'WINDOW_TITLE': 'P2P File Sharing Application',
    'LOG_MAX_LINES': 1000,        # Maximum lines to keep in activity log
    'AUTO_REFRESH_INTERVAL': 3000, # Milliseconds
}

# File Configuration
FILE_CONFIG = {
    'SHARED_FILES_DIR': './shared_files',
    'MAX_FILE_SIZE': 5 * 1024 * 1024 * 1024,  # 5 GB max file size
    'ALLOWED_EXTENSIONS': [],  # Empty means all extensions allowed
}

# UI Theme Configuration
THEME_CONFIG = {
    'BG_COLOR': '#f0f0f0',
    'PRIMARY_COLOR': '#0078d4',
    'SUCCESS_COLOR': '#107c10',
    'ERROR_COLOR': '#da3b01',
    'FONT_FAMILY': 'Helvetica',
    'FONT_SIZE': 10,
}
