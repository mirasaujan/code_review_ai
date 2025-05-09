"""
Directory scanner for collecting multiple files.
"""

import os
import yaml
from typing import List, Dict, Any
from models import FileContent

class DirectoryScanner:
    """Scans directories and collects files based on patterns."""
    
    def __init__(self, config_path: str = "codereview.yaml"):
        """
        Initialize scanner with config file.
        
        Args:
            config_path: Path to codereview.yaml config file
        """
        self.config_path = config_path
        self.include_patterns = []
        self.exclude_patterns = []
        self._load_config()
        
    def _load_config(self):
        """Load include/exclude patterns from config file."""
        if not os.path.exists(self.config_path):
            return
            
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            self.include_patterns = config.get('include', [])
            self.exclude_patterns = config.get('exclude', [])
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            
    def _should_include(self, file_path: str) -> bool:
        """Check if file should be included based on patterns."""
        # Check exclude patterns first
        for pattern in self.exclude_patterns:
            if self._matches_pattern(file_path, pattern):
                return False
                
        # If no include patterns, include all non-excluded files
        if not self.include_patterns:
            return True
            
        # Check include patterns
        for pattern in self.include_patterns:
            if self._matches_pattern(file_path, pattern):
                return True
                
        return False
        
    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file matches glob pattern."""
        import fnmatch
        return fnmatch.fnmatch(file_path, pattern)
        
    def scan(self, directory: str) -> List[FileContent]:
        """
        Scan directory and collect files.
        
        Args:
            directory: Path to directory to scan
            
        Returns:
            List of FileContent objects for matching files
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If directory can't be accessed
        """
        from collector import File
        file_collector = File()
        
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
            
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Not a directory: {directory}")
            
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, directory)
                
                if self._should_include(rel_path):
                    try:
                        file_content = file_collector.collect(file_path)
                        files.append(file_content)
                    except (FileNotFoundError, PermissionError) as e:
                        print(f"Warning: Could not read {file_path}: {e}")
                        
        return files