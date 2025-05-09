"""
File loader for single file collection.
"""

import os
from typing import Dict, Any
from models import FileContent

class FileLoader:
    """Handles loading and parsing of single files with metadata."""
    
    def load(self, file_path: str) -> FileContent:
        """
        Load a single file and its metadata.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            FileContent object with file content and metadata
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            metadata = self._get_metadata(file_path, content)
            return FileContent(
                path=file_path,
                content=content,
                metadata=metadata
            )
        except PermissionError:
            raise PermissionError(f"Cannot read file: {file_path}")
            
    def _get_metadata(self, file_path: str, content: str) -> Dict[str, Any]:
        """Extract metadata from file."""
        return {
            'language': self._detect_language(file_path),
            'size': len(content.encode('utf-8'))
        }
        
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.sh': 'shell',
            '.bash': 'shell',
            '.zsh': 'shell',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text'
        }
        return lang_map.get(ext, 'unknown') 