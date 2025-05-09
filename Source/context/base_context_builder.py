from abc import ABC, abstractmethod
from typing import Dict, Any
from ..utils.language_utils import get_language_from_extension

class BaseContextBuilder(ABC):
    """Base class for all context builders"""
    
    @abstractmethod
    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build context from input data"""
        pass

    def _get_language(self, file_path: str) -> str:
        """Determine language from file extension"""
        return get_language_from_extension(file_path) 