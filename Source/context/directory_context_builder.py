from typing import Dict, Any, List
from .base_context_builder import BaseContextBuilder

class DirectoryContextBuilder(BaseContextBuilder):
    """Builds context for directory contents"""
    
    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:
        files = data['files']
        
        return {
            'review_type': 'directory',
            'files': [
                {
                    'file': f['path'],
                    'language': f.get('metadata', {}).get('language', self._get_language(f['path'])),
                    'content': f['content']
                }
                for f in files
            ]
        } 