from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class FileContent:
    """Represents a file's content and metadata."""
    path: str
    content: str
    metadata: dict

    def to_dict(self) -> Dict[str, Any]:
        """Convert file content to dictionary format."""
        return {
            "path": self.path,
            "content": self.content,
            "metadata": self.metadata
        }

@dataclass
class DiffHunk:
    """Represents a chunk of changes in a file."""
    file_path: str
    start_line: int
    end_line: int
    old_lines: str
    new_lines: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert hunk to dictionary format."""
        return {
            "start_line": self.start_line,
            "end_line": self.end_line,
            "before": self.old_lines,
            "after": self.new_lines
        }
