"""
P2P File Sharing Application - Main UI
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from datetime import datetime
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from network_manager import NetworkManager
from file_manager import FileManager


class P2PFileShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P File Sharing Application")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize managers
        shared_files_dir = os.path.join(os.path.dirname(__file__), '..', 'shared_files')
        self.file_manager = FileManager(shared_files_dir)
        self.network_manager = NetworkManager(callback=self.log_message)
        
        # Variables
        self.peer_name_var = tk.StringVar(value=f"Peer-{self.network_manager.peer_id}")
        self.is_running = False
        
        # Setup UI
        self.setup_ui()
        self.refresh_peers()
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="P2P File Sharing Application",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_container, text="Control Panel", padding=10)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Peer name input
        name_frame = ttk.Frame(control_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Your Name:").pack(side=tk.LEFT, padx=5)
        name_entry = ttk.Entry(name_frame, textvariable=self.peer_name_var, width=20)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        # Server control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="Start Server", command=self.start_server)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Refresh Peers", command=self.refresh_peers).pack(side=tk.LEFT, padx=5)
        
        # Main content - Paned window
        paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left panel - Peers
        left_frame = ttk.LabelFrame(paned, text="Connected Peers", padding=10)
        paned.add(left_frame, weight=1)
        
        # Peers listbox
        peers_scroll = ttk.Scrollbar(left_frame)
        peers_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.peers_listbox = tk.Listbox(left_frame, yscrollcommand=peers_scroll.set, height=15)
        self.peers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        peers_scroll.config(command=self.peers_listbox.yview)
        
        # Peer actions
        peer_action_frame = ttk.Frame(left_frame)
        peer_action_frame.pack(fill=tk.X, pady=5)
        ttk.Button(peer_action_frame, text="Connect to Peer", command=self.connect_to_peer).pack(side=tk.LEFT, padx=2)
        
        # Middle panel - Shared Files
        middle_frame = ttk.LabelFrame(paned, text="Shared Files", padding=10)
        paned.add(middle_frame, weight=1)
        
        # Files listbox
        files_scroll = ttk.Scrollbar(middle_frame)
        files_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(middle_frame, yscrollcommand=files_scroll.set, height=15)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        files_scroll.config(command=self.files_listbox.yview)
        
        # File actions
        file_action_frame = ttk.Frame(middle_frame)
        file_action_frame.pack(fill=tk.X, pady=5)
        ttk.Button(file_action_frame, text="Add File", command=self.add_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_action_frame, text="Remove File", command=self.remove_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_action_frame, text="Refresh", command=self.refresh_files).pack(side=tk.LEFT, padx=2)
        
        # Right panel - Logs
        right_frame = ttk.LabelFrame(paned, text="Activity Log", padding=10)
        paned.add(right_frame, weight=1)
        
        # Log text area
        log_scroll = ttk.Scrollbar(right_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(right_frame, yscrollcommand=log_scroll.set, height=15, width=30)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        log_scroll.config(command=self.log_text.yview)
        
        # Status bar
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Status: Offline", font=("Helvetica", 10))
        self.status_label.pack(side=tk.LEFT)
        
        self.ip_label = ttk.Label(status_frame, text="", font=("Helvetica", 10))
        self.ip_label.pack(side=tk.RIGHT)
    
    def start_server(self):
        """Start the P2P server"""
        if self.network_manager.start():
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Online", foreground="green")
            local_ip = NetworkManager.get_local_ip()
            self.ip_label.config(text=f"IP: {local_ip}:5000")
            self.log_message(f"Server started successfully")
            self.log_message(f"Local IP: {local_ip}")
            
            # Start periodic refresh
            self.auto_refresh()
    
    def stop_server(self):
        """Stop the P2P server"""
        self.network_manager.stop()
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Offline", foreground="red")
        self.log_message("Server stopped")
    
    def add_file(self):
        """Add a file to share"""
        file_path = filedialog.askopenfilename(title="Select a file to share")
        if file_path:
            if self.file_manager.add_file_to_share(file_path):
                file_name = os.path.basename(file_path)
                self.log_message(f"File added: {file_name}")
                self.refresh_files()
            else:
                messagebox.showerror("Error", "Failed to add file")
    
    def remove_file(self):
        """Remove a file from sharing"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            files = self.file_manager.get_shared_files()
            if index < len(files):
                file_name = files[index]['name']
                if self.file_manager.remove_shared_file(file_name):
                    self.log_message(f"File removed: {file_name}")
                    self.refresh_files()
    
    def refresh_files(self):
        """Refresh the shared files list"""
        self.files_listbox.delete(0, tk.END)
        files = self.file_manager.get_shared_files()
        for file_info in files:
            display_text = f"{file_info['name']} ({file_info['size_readable']})"
            self.files_listbox.insert(tk.END, display_text)
    
    def refresh_peers(self):
        """Refresh the peers list"""
        threading.Thread(target=self._refresh_peers_thread, daemon=True).start()
    
    def _refresh_peers_thread(self):
        """Refresh peers in a separate thread"""
        peers = self.network_manager.get_peers()
        self.peers_listbox.delete(0, tk.END)
        
        if not peers:
            self.peers_listbox.insert(tk.END, "No peers connected")
        else:
            for peer in peers:
                display_text = f"{peer['name']} ({peer['ip']}:{peer['port']})"
                self.peers_listbox.insert(tk.END, display_text)
    
    def connect_to_peer(self):
        """Connect to a specific peer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Connect to Peer")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Peer IP:").pack(pady=5)
        ip_entry = ttk.Entry(dialog)
        ip_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Peer Port:").pack(pady=5)
        port_entry = ttk.Entry(dialog)
        port_entry.insert(0, "5000")
        port_entry.pack(pady=5)
        
        def do_connect():
            try:
                peer_ip = ip_entry.get()
                peer_port = int(port_entry.get())
                
                if self.network_manager.connect_to_peer(peer_ip, peer_port, self.peer_name_var.get()):
                    self.log_message(f"Connected to {peer_ip}:{peer_port}")
                    self.refresh_peers()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to connect")
            except ValueError:
                messagebox.showerror("Error", "Invalid port number")
        
        ttk.Button(dialog, text="Connect", command=do_connect).pack(pady=10)
    
    def log_message(self, message: str):
        """Log a message to the activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def auto_refresh(self):
        """Auto-refresh peers periodically"""
        if self.is_running:
            self.refresh_peers()
            self.root.after(3000, self.auto_refresh)
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            self.stop_server()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = P2PFileShareApp(root)
    
    # Initial log messages
    app.log_message("P2P File Sharing Application Started")
    app.log_message(f"Your Peer ID: {app.network_manager.peer_id}")
    app.refresh_files()
    
    root.mainloop()


if __name__ == "__main__":
    main()
