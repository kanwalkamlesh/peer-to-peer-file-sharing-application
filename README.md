# P2P File Sharing Application

A peer-to-peer file sharing application that allows users to share files with other peers on the same local area network (LAN).

## Features

- **Peer Discovery**: Automatically discover other peers on the LAN
- **File Sharing**: Add files to a shared directory for other peers to download
- **Multiple Peers**: Connect to multiple peers simultaneously
- **Activity Log**: Real-time activity logging for monitoring operations
- **User-Friendly UI**: Clean and intuitive graphical user interface built with tkinter
- **Network Management**: Handles P2P socket communication and file transfers
- **File Management**: Easy file addition, removal, and management

## Project Structure

```
peer-to-peer-file-sharing-application/
├── src/
│   ├── network_manager.py       # P2P networking and peer discovery
│   └── file_manager.py          # File operations and management
├── ui/
│   └── main_app.py              # Main GUI application
├── shared_files/                # Directory for shared files
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Requirements

- Python 3.6+
- tkinter (usually comes with Python)
- No external dependencies (uses standard library)

## Installation

1. Clone or download the project:
```bash
cd peer-to-peer-file-sharing-application
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

## Running the Application

1. **Start the application**:
```bash
python ui/main_app.py
```

2. **Enter your peer name** in the "Your Name" field

3. **Click "Start Server"** to start your P2P server

4. **Add files to share** by clicking "Add File" button

5. **Connect to other peers** by entering their IP and port

## How It Works

### Peer Discovery
- The application uses UDP broadcasting to discover peers on the LAN
- Peers listen on port 5001 for discovery messages
- Each peer responds with its connection details

### File Sharing
1. Peers can add files to their shared directory
2. Other peers can view shared files and connect to transfer
3. Files are transferred using TCP sockets for reliability
4. File transfer happens in 4KB chunks to handle large files

### Network Architecture
- **Server Component**: Each peer runs a TCP server on port 5000
- **Discovery Component**: UDP-based peer discovery on port 5001
- **P2P Communication**: Direct peer-to-peer socket connections

## Usage Guide

### Sharing Files
1. Click "Add File" button
2. Select a file from your computer
3. File is copied to the shared directory
4. Other peers can now see and download it

### Downloading Files
1. Connect to a peer using their IP address
2. View their shared files
3. Select and download files

### Managing Connections
- **Refresh Peers**: Click to manually refresh the peer list
- **Connect to Peer**: Enter IP and port of a specific peer
- **Activity Log**: View all network activities and status messages

## Configuration

Default settings:
- **Server Port**: 5000 (configurable in network_manager.py)
- **Discovery Port**: 5001 (UDP broadcast)
- **File Transfer Chunk Size**: 4096 bytes
- **Discovery Interval**: 3 seconds
- **Shared Files Directory**: `./shared_files/`

## Limitations

- Currently works best on the same LAN
- File transfers are sequential (one at a time)
- No user authentication
- No file encryption
- Limited to peers that can reach each other

## Future Enhancements

- [ ] Multi-threaded file transfers
- [ ] File encryption and security
- [ ] User authentication and access control
- [ ] Web-based UI
- [ ] File search functionality
- [ ] Download progress indicators
- [ ] Resume partial transfers
- [ ] Support for multiple simultaneous transfers

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the port in `main_app.py`:
```python
self.network_manager = NetworkManager(port=5001)
```

### Peers Not Discovered
- Ensure all peers are on the same network
- Check firewall settings
- Verify that ports 5000 and 5001 are not blocked

### File Transfer Errors
- Check that the file path is valid
- Ensure sufficient disk space
- Verify network connectivity

## License

This project is open source and available for educational purposes.

## Author

Created as an Operating Systems Project (OS_PBL)

## Support

For issues or questions, please refer to the activity log in the application for detailed error messages.
