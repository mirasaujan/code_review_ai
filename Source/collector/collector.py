from abc import ABC, abstractmethod
from typing import List
from models import FileContent
from git_diff import GitDiffCollector
from file_loader import FileLoader
from directory_scanner import DirectoryScanner

class BaseCollector(ABC):
    @abstractmethod
    def collect(self) -> List[FileContent]:
        """Collect files for review."""
        pass

class GitDiff(BaseCollector):
    def __init__(self, repo_path: str = "."):
        self._collector = GitDiffCollector(repo_path)
        
    def collect(self, ref_spec: str):
        """
        Collect changes between Git references.
        
        Args:
            ref_spec: Git reference spec (e.g., "main..feature-branch")
            
        Returns:
            List of JSON objects containing the changes
        """
        return self._collector.collect(ref_spec)

class File(BaseCollector):
    def __init__(self):
        self._loader = FileLoader()
        
    def collect(self, file_path: str) -> FileContent:
        """
        Collect a single file for review.
        
        Args:
            file_path: Path to the file to collect
            
        Returns:
            FileContent object with file content and metadata
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        return self._loader.load(file_path)

class Directory(BaseCollector):
    def __init__(self, config_path: str = "codereview.yaml"):
        """
        Initialize directory collector.
        
        Args:
            config_path: Path to codereview.yaml config file
        """
        self._scanner = DirectoryScanner(config_path)
        
    def collect(self, directory: str) -> List[FileContent]:
        """
        Collect files from directory based on patterns.
        
        Args:
            directory: Path to directory to scan
            
        Returns:
            List of FileContent objects for matching files
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If directory can't be accessed
        """
        return self._scanner.scan(directory)