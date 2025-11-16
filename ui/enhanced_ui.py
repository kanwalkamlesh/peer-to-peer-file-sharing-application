"""
Enhanced UI Module - Additional UI components and themes
"""
import tkinter as tk
from tkinter import ttk


class ModernStyle:
    """Modern UI theme for the application"""
    
    COLORS = {
        'bg': '#f0f0f0',
        'fg': '#333333',
        'accent': '#0078d4',
        'success': '#107c10',
        'error': '#da3b01',
        'warning': '#ffd700',
        'border': '#d0d0d0',
        'hover': '#e8e8e8',
    }
    
    @staticmethod
    def configure_style():
        """Configure ttk style"""
        style = ttk.Style()
        
        # Set theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TLabel', background=ModernStyle.COLORS['bg'], foreground=ModernStyle.COLORS['fg'])
        style.configure('TFrame', background=ModernStyle.COLORS['bg'])
        style.configure('TLabelframe', background=ModernStyle.COLORS['bg'], foreground=ModernStyle.COLORS['fg'])
        style.configure('TButton', background=ModernStyle.COLORS['accent'])
        
        return style


class StatusIndicator(tk.Canvas):
    """Custom status indicator widget"""
    
    def __init__(self, parent, status='offline', **kwargs):
        super().__init__(parent, width=20, height=20, bg=kwargs.get('bg', '#f0f0f0'), 
                        highlightthickness=0, **kwargs)
        self.status = status
        self.draw_status()
    
    def draw_status(self):
        """Draw the status indicator"""
        self.delete("all")
        
        color = {
            'online': '#107c10',
            'offline': '#da3b01',
            'connecting': '#ffd700',
            'error': '#da3b01'
        }.get(self.status, '#999999')
        
        self.create_oval(2, 2, 18, 18, fill=color, outline='white', width=2)
    
    def set_status(self, status):
        """Set the status"""
        self.status = status
        self.draw_status()


class FileTransferProgressBar(ttk.Frame):
    """Custom progress bar for file transfers"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Progress bar
        self.progress = ttk.Progressbar(self, mode='determinate', length=200)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Percentage label
        self.label = ttk.Label(self, text="0%", width=5)
        self.label.pack(side=tk.LEFT, padx=5)
    
    def update_progress(self, current, total):
        """Update the progress bar"""
        if total > 0:
            percentage = (current / total) * 100
            self.progress['value'] = percentage
            self.label.config(text=f"{percentage:.0f}%")
            self.update_idletasks()


class PeerCard(ttk.Frame):
    """Card widget for displaying peer information"""
    
    def __init__(self, parent, peer_name, peer_ip, peer_port, **kwargs):
        super().__init__(parent, relief=tk.RAISED, borderwidth=1, **kwargs)
        
        # Peer info frame
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Peer name
        name_label = ttk.Label(info_frame, text=peer_name, font=("Helvetica", 11, "bold"))
        name_label.pack(anchor=tk.W)
        
        # Peer address
        addr_label = ttk.Label(info_frame, text=f"{peer_ip}:{peer_port}", 
                              font=("Helvetica", 9), foreground="#666666")
        addr_label.pack(anchor=tk.W)
        
        # Status indicator
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        indicator = StatusIndicator(status_frame, status='online')
        indicator.pack(side=tk.LEFT, padx=5)
        
        status_text = ttk.Label(status_frame, text="Connected", foreground="#107c10")
        status_text.pack(side=tk.LEFT)


class FileCard(ttk.Frame):
    """Card widget for displaying file information"""
    
    def __init__(self, parent, file_name, file_size, **kwargs):
        super().__init__(parent, relief=tk.RAISED, borderwidth=1, **kwargs)
        
        # File info frame
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File name
        name_label = ttk.Label(info_frame, text=file_name, font=("Helvetica", 11, "bold"))
        name_label.pack(anchor=tk.W)
        
        # File size
        size_label = ttk.Label(info_frame, text=f"Size: {file_size}", 
                              font=("Helvetica", 9), foreground="#666666")
        size_label.pack(anchor=tk.W)


class HoverButton(ttk.Button):
    """Button with hover effect"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
    
    def _on_hover(self, event):
        """Handle hover effect"""
        self.config(state=tk.ACTIVE)
    
    def _on_leave(self, event):
        """Handle leave effect"""
        if self.cget('state') != tk.DISABLED:
            self.config(state=tk.NORMAL)


class Tooltip:
    """Tooltip widget for hover help text"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Show tooltip"""
        if self.tipwindow or not self.text:
            return
        
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(tw, text=self.text, background="#ffffe0", 
                         relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)
    
    def hide_tooltip(self, event=None):
        """Hide tooltip"""
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
