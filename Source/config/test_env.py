"""
Test file for environment variable loading.
"""

import os
import tempfile
import pytest
from pathlib import Path
from env import EnvLoader

@pytest.fixture(autouse=True)
def clean_env():
    """Clean environment variables before each test."""
    # Save existing env vars
    old_env = {}
    for key in EnvLoader.REQUIRED_KEYS:
        if key in os.environ:
            old_env[key] = os.environ[key]
            del os.environ[key]
    
    yield
    
    # Restore env vars
    for key, value in old_env.items():
        os.environ[key] = value

def create_test_env(content: str) -> Path:
    """Create a temporary .env file with given content."""
    fd, path = tempfile.mkstemp(suffix='.env')
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return Path(path)

def test_missing_env_file():
    """Test behavior when .env file doesn't exist."""
    loader = EnvLoader('nonexistent.env')
    with pytest.raises(ValueError, match="Missing required environment variables"):
        loader.validate_required_keys()

def test_valid_env_file():
    """Test loading valid environment variables."""
    env_content = """
    OPENAI_API_KEY=sk_test_123
    ANTHROPIC_API_KEY=sk_test_456
    GOOGLE_API_KEY=sk_test_789
    LLAMA_SERVER_URL=http://localhost:11434
    """
    
    env_path = create_test_env(env_content)
    try:
        loader = EnvLoader(str(env_path))
        loader.validate_required_keys()  # Should not raise
        
        # Test getting individual keys
        assert loader.get_api_key('OPENAI') == 'sk_test_123'
        assert loader.get_api_key('ANTHROPIC') == 'sk_test_456'
        assert loader.get_api_key('GOOGLE') == 'sk_test_789'
        assert loader.get_api_key('LLAMA') == 'http://localhost:11434'
        
    finally:
        env_path.unlink()

def test_invalid_provider():
    """Test getting API key for invalid provider."""
    loader = EnvLoader()
    with pytest.raises(ValueError, match="Invalid provider"):
        loader.get_api_key('INVALID')

def test_missing_api_key():
    """Test behavior when API key is missing."""
    env_content = """
    OPENAI_API_KEY=sk_test_123
    # Missing other keys
    """
    
    env_path = create_test_env(env_content)
    try:
        loader = EnvLoader(str(env_path))
        with pytest.raises(ValueError, match="Missing Anthropic API key for Claude models"):
            loader.get_api_key('ANTHROPIC')
    finally:
        env_path.unlink()

if __name__ == '__main__':
    pytest.main([__file__]) 