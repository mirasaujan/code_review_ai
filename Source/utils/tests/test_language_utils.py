import pytest
from ..language_utils import get_language_from_extension

def test_get_language_from_extension():
    # Test various file extensions
    assert get_language_from_extension('test.py') == 'python'
    assert get_language_from_extension('script.js') == 'javascript'
    assert get_language_from_extension('styles.css') == 'css'
    assert get_language_from_extension('data.json') == 'json'
    assert get_language_from_extension('doc.md') == 'markdown'
    
    # Test with uppercase extensions
    assert get_language_from_extension('TEST.PY') == 'python'
    assert get_language_from_extension('SCRIPT.JS') == 'javascript'
    
    # Test with no extension
    assert get_language_from_extension('README') == 'text'
    
    # Test with unknown extension
    assert get_language_from_extension('file.xyz') == 'text'
    
    # Test with multiple dots
    assert get_language_from_extension('test.min.js') == 'javascript'
    
    # Test shell script variations
    assert get_language_from_extension('script.sh') == 'shell'
    assert get_language_from_extension('script.bash') == 'shell'
    assert get_language_from_extension('script.zsh') == 'shell' 