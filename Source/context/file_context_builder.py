from typing import Dict, Any
from .base_context_builder import BaseContextBuilder

class FileContextBuilder(BaseContextBuilder):
    """Builds context for single files"""
    
    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:
        file_path = data['file_path']
        content = data['content']
        metadata = data.get('metadata', {})
        
        return {
            'file': file_path,
            'language': metadata.get('language', self._get_language(file_path)),
            'review_type': 'file',
            'full_content': content
        } 