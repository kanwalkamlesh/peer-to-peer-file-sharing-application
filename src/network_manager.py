"""
Network Manager - Handles P2P communication and peer discovery
"""
import socket
import threading
import json
import os
from typing import Callable, Dict, List, Tuple
import time


class NetworkManager:
    """Manages P2P networking and peer communication"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, callback: Callable = None):
        self.host = host
        self.port = port
        self.socket = None
        self.peer_id = self._generate_peer_id()  # Generate once at startup
        self.peers: Dict[str, Dict] = {}  # {peer_id: {ip, port, name}}
        self.callback = callback  # Callback for UI updates
        self.running = False
        self.listen_thread = None
        self.discover_thread = None
        
    def start(self) -> bool:
        """Start the P2P server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            # Start listening for incoming connections
            self.listen_thread = threading.Thread(target=self._listen_for_connections, daemon=True)
            self.listen_thread.start()
            
            # Start peer discovery
            self.discover_thread = threading.Thread(target=self._discover_peers, daemon=True)
            self.discover_thread.start()
            
            if self.callback:
                self.callback("Server started on {}:{}".format(self.host if self.host else "0.0.0.0", self.port))
            return True
        except Exception as e:
            if self.callback:
                self.callback(f"Error starting server: {str(e)}")
            return False
    
    def stop(self):
        """Stop the P2P server"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def _listen_for_connections(self):
        """Listen for incoming connections from peers"""
        while self.running:
            try:
                client_socket, addr = self.socket.accept()
                # Handle connection in a separate thread
                threading.Thread(
                    target=self._handle_peer_connection,
                    args=(client_socket, addr),
                    daemon=True
                ).start()
            except Exception as e:
                if self.running:
                    if self.callback:
                        self.callback(f"Connection error: {str(e)}")
                break
    
    def _handle_peer_connection(self, client_socket, addr):
        """Handle incoming connection from a peer"""
        try:
            # Receive peer info
            data = client_socket.recv(4096).decode('utf-8')
            if data:
                peer_info = json.loads(data)
                peer_id = peer_info.get('peer_id')
                peer_name = peer_info.get('name', 'Unknown')
                
                self.peers[peer_id] = {
                    'ip': addr[0],
                    'port': peer_info.get('port', addr[1]),
                    'name': peer_name
                }
                
                if self.callback:
                    self.callback(f"Peer connected: {peer_name} ({addr[0]})")
                
                # Send acknowledgment
                response = {'status': 'connected', 'peer_id': self.peer_id}
                client_socket.sendall(json.dumps(response).encode('utf-8'))
        except Exception as e:
            if self.callback:
                self.callback(f"Error handling peer connection: {str(e)}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def _discover_peers(self):
        """Discover peers on the LAN using UDP broadcast"""
        while self.running:
            try:
                # Get local IP
                local_ip = self.get_local_ip()
                
                # Create socket for broadcasting
                broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                broadcast_socket.settimeout(2)
                
                # Bind to listen for responses
                broadcast_socket.bind(('', 5001))
                
                message = {
                    'type': 'discovery',
                    'peer_id': self.peer_id,
                    'ip': local_ip,
                    'port': self.port
                }
                
                # Send discovery broadcast
                broadcast_socket.sendto(
                    json.dumps(message).encode('utf-8'),
                    ('<broadcast>', 5001)
                )
                
                # Listen for discovery responses
                try:
                    data, addr = broadcast_socket.recvfrom(4096)
                    peer_data = json.loads(data.decode('utf-8'))
                    if peer_data.get('type') == 'discovery_response':
                        peer_id = peer_data.get('peer_id')
                        if peer_id != self.peer_id:  # Don't add ourselves
                            self.peers[peer_id] = {
                                'ip': addr[0],
                                'port': peer_data.get('port'),
                                'name': peer_data.get('name', 'Unknown')
                            }
                except socket.timeout:
                    pass
                finally:
                    broadcast_socket.close()
                
                time.sleep(3)  # Discovery interval
            except Exception as e:
                if self.callback:
                    self.callback(f"Discovery error: {str(e)}")
                time.sleep(3)
    
    def connect_to_peer(self, peer_ip: str, peer_port: int, peer_name: str = "Unknown") -> bool:
        """Connect to a specific peer"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            sock.connect((peer_ip, peer_port))

            # Send our peer info
            peer_info = {
                'peer_id': self.peer_id,
                'name': peer_name,
                'port': self.port
            }
            sock.sendall(json.dumps(peer_info).encode('utf-8'))

            # Wait for response with timeout
            sock.settimeout(3)
            response = sock.recv(4096).decode('utf-8')
            if response:
                response_data = json.loads(response)
                remote_peer_id = response_data.get('peer_id', None)
                if remote_peer_id:
                    # Store the connected peer using their peer_id
                    self.peers[remote_peer_id] = {
                        'ip': peer_ip,
                        'port': peer_port,
                        'name': peer_name
                    }
                    if self.callback:
                        self.callback(f"Connected to peer: {peer_name} ({peer_ip}:{peer_port})")
                    return True
        except socket.timeout:
            if self.callback:
                self.callback(f"Connection timeout: Peer {peer_ip}:{peer_port} not responding")
        except ConnectionRefusedError:
            if self.callback:
                self.callback(f"Connection refused: Peer {peer_ip}:{peer_port} is offline")
        except Exception as e:
            if self.callback:
                self.callback(f"Failed to connect to peer: {str(e)}")
        finally:
            try:
                sock.close()
            except:
                pass
        return False
    
    def get_peers(self) -> List[Dict]:
        """Get list of connected peers"""
        return list(self.peers.values())
    
    def send_file(self, file_path: str, peer_ip: str, peer_port: int) -> bool:
        """Send a file to a peer"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_ip, peer_port))
            
            # Send file transfer request
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            transfer_request = {
                'type': 'file_transfer',
                'file_name': file_name,
                'file_size': file_size
            }
            sock.sendall(json.dumps(transfer_request).encode('utf-8'))
            
            # Wait for acceptance
            response = sock.recv(1024).decode('utf-8')
            if response == 'accepted':
                # Send file in chunks
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        sock.sendall(chunk)
                
                if self.callback:
                    self.callback(f"File sent: {file_name} to {peer_ip}")
                sock.close()
                return True
        except Exception as e:
            if self.callback:
                self.callback(f"Error sending file: {str(e)}")
        return False
    
    def receive_file(self, client_socket, download_path: str):
        """Receive a file from a peer"""
        try:
            # Receive transfer request
            data = client_socket.recv(4096).decode('utf-8')
            transfer_request = json.loads(data)
            
            file_name = transfer_request.get('file_name')
            file_size = transfer_request.get('file_size')
            
            # Send acceptance
            client_socket.sendall(b'accepted')
            
            # Receive file in chunks
            file_path = os.path.join(download_path, file_name)
            bytes_received = 0
            
            with open(file_path, 'wb') as f:
                while bytes_received < file_size:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
            
            if self.callback:
                self.callback(f"File received: {file_name}")
            
            client_socket.close()
        except Exception as e:
            if self.callback:
                self.callback(f"Error receiving file: {str(e)}")
    
    @staticmethod
    def get_local_ip() -> str:
        """Get local IP address"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def _generate_peer_id() -> str:
        """Generate a unique peer ID once at startup"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    @staticmethod
    def get_peer_id() -> str:
        """Get a new peer ID (for backward compatibility)"""
        import uuid
        return str(uuid.uuid4())[:8]
