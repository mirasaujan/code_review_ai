"""Utility functions for language detection and mapping."""

LANGUAGE_MAP = {
    # Python
    'py': 'python',
    '.py': 'python',
    
    # JavaScript/TypeScript
    'js': 'javascript',
    '.js': 'javascript',
    'ts': 'typescript',
    '.ts': 'typescript',
    
    # Java
    'java': 'java',
    '.java': 'java',
    
    # C/C++
    'cpp': 'cpp',
    '.cpp': 'cpp',
    'c': 'c',
    '.c': 'c',
    'h': 'cpp',
    '.h': 'c',
    
    # C#
    'cs': 'csharp',
    '.cs': 'csharp',
    
    # Go
    'go': 'go',
    '.go': 'go',
    
    # Rust
    'rs': 'rust',
    '.rs': 'rust',
    
    # Ruby
    'rb': 'ruby',
    '.rb': 'ruby',
    
    # PHP
    'php': 'php',
    '.php': 'php',
    
    # Swift
    'swift': 'swift',
    '.swift': 'swift',
    
    # Kotlin
    'kt': 'kotlin',
    '.kt': 'kotlin',
    
    # Scala
    'scala': 'scala',
    '.scala': 'scala',
    
    # Shell
    'sh': 'shell',
    '.sh': 'shell',
    'bash': 'shell',
    '.bash': 'shell',
    'zsh': 'shell',
    '.zsh': 'shell',
    
    # Web
    'html': 'html',
    '.html': 'html',
    'css': 'css',
    '.css': 'css',
    
    # Data formats
    'json': 'json',
    '.json': 'json',
    'yaml': 'yaml',
    '.yaml': 'yaml',
    'yml': 'yaml',
    '.yml': 'yaml',
    
    # Documentation
    'md': 'markdown',
    '.md': 'markdown',
    'txt': 'text',
    '.txt': 'text'
}

def get_language_from_extension(file_path: str) -> str:
    """
    Determine the programming language from a file path.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: The detected language or 'text' if unknown
    """
    # Try with the full extension first
    ext = file_path.split('.')[-1].lower()
    if ext in LANGUAGE_MAP:
        return LANGUAGE_MAP[ext]
    
    # Try with dot prefix
    dot_ext = f'.{ext}'
    if dot_ext in LANGUAGE_MAP:
        return LANGUAGE_MAP[dot_ext]
    
    return 'text' 