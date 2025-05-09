from abc import ABC, abstractmethod
from typing import List
from models import FileContent
from git_diff import GitDiffCollector

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