"""
Collector package for code review.
Provides functionality to collect and parse code changes from different sources.
"""

from .models import FileContent, DiffHunk
from .collector import GitDiff, File

__all__ = [
    'FileContent',
    'DiffHunk',
    'GitDiff',
    'File',
]
