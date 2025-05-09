from typing import Dict, Any
from .base_context_builder import BaseContextBuilder

class DiffContextBuilder(BaseContextBuilder):
    """Builds context for git diffs"""
    
    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:
        file_path = data['file_path']
        hunks = data['hunks']
        
        return {
            'file': file_path,
            'language': self._get_language(file_path),
            'changes': {
                'type': 'diff',
                'hunks': hunks
            }
        } 