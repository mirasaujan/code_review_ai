"""
Environment variable loader for the code review tool.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

class EnvLoader:
    """Loads and validates environment variables from .env file."""
    
    REQUIRED_KEYS = {
        'OPENAI_API_KEY': 'OpenAI API key for GPT models',
        'ANTHROPIC_API_KEY': 'Anthropic API key for Claude models',
        'GOOGLE_API_KEY': 'Google API key for Gemini models',
        'LLAMA_SERVER_URL': 'URL for local Llama server'
    }
    
    def __init__(self, env_path: Optional[str] = None):
        """Initialize the environment loader.
        
        Args:
            env_path: Optional path to .env file. If None, looks in current directory.
        """
        self.env_path = env_path or '.env'
        self._load_env()
        
    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        env_file = Path(self.env_path)
        if not env_file.exists():
            print(f"Warning: {self.env_path} not found. Using environment variables if set.")
            return
            
        load_dotenv(env_file)
        
    def get_api_key(self, provider: str) -> str:
        """Get API key for specified provider.
        
        Args:
            provider: One of 'OPENAI', 'ANTHROPIC', 'GOOGLE', 'LLAMA'
            
        Returns:
            API key string
            
        Raises:
            ValueError: If provider is invalid or key is not set
        """
        key_name = f"{provider.upper()}_API_KEY"
        if provider.upper() == 'LLAMA':
            key_name = 'LLAMA_SERVER_URL'
            
        if key_name not in self.REQUIRED_KEYS:
            raise ValueError(f"Invalid provider: {provider}")
            
        key = os.getenv(key_name)
        if not key:
            raise ValueError(f"Missing {self.REQUIRED_KEYS[key_name]}")
            
        return key
        
    def validate_required_keys(self) -> None:
        """Validate that all required API keys are set.
        
        Raises:
            ValueError: If any required key is missing
        """
        missing = []
        for key, description in self.REQUIRED_KEYS.items():
            if not os.getenv(key):
                missing.append(f"{key} ({description})")
                
        if missing:
            raise ValueError(
                "Missing required environment variables:\n" + 
                "\n".join(f"- {key}" for key in missing)
            ) 