"""
File Manager - Handles file operations and sharing
"""
import os
import shutil
from typing import List, Dict
from pathlib import Path


class FileManager:
    """Manages files and sharing directories"""
    
    def __init__(self, shared_dir: str):
        self.shared_dir = shared_dir
        if not os.path.exists(shared_dir):
            os.makedirs(shared_dir)
    
    def get_shared_files(self) -> List[Dict]:
        """Get list of files in shared directory"""
        files = []
        try:
            for filename in os.listdir(self.shared_dir):
                file_path = os.path.join(self.shared_dir, filename)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    files.append({
                        'name': filename,
                        'path': file_path,
                        'size': file_size,
                        'size_readable': self._format_size(file_size)
                    })
        except Exception as e:
            print(f"Error reading shared files: {str(e)}")
        return sorted(files, key=lambda x: x['name'])
    
    def add_file_to_share(self, file_path: str) -> bool:
        """Add a file to the shared directory"""
        try:
            if not os.path.exists(file_path):
                return False
            
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.shared_dir, file_name)
            
            if os.path.isfile(file_path):
                shutil.copy2(file_path, dest_path)
                return True
        except Exception as e:
            print(f"Error adding file: {str(e)}")
        return False
    
    def remove_shared_file(self, file_name: str) -> bool:
        """Remove a file from shared directory"""
        try:
            file_path = os.path.join(self.shared_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error removing file: {str(e)}")
        return False
    
    def download_file(self, file_name: str, dest_path: str) -> bool:
        """Download a file from shared directory"""
        try:
            src_path = os.path.join(self.shared_dir, file_name)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                return True
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
        return False
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    @staticmethod
    def browse_file() -> str:
        """Open file browser dialog"""
        try:
            from tkinter import filedialog
            return filedialog.askopenfilename(title="Select a file to share")
        except:
            return ""
    
    @staticmethod
    def browse_directory() -> str:
        """Open directory browser dialog"""
        try:
            from tkinter import filedialog
            return filedialog.askdirectory(title="Select a directory to save files")
        except:
            return ""
