import pytest
from ..diff_context_builder import DiffContextBuilder
from ..file_context_builder import FileContextBuilder
from ..directory_context_builder import DirectoryContextBuilder

def test_diff_context_builder():
    builder = DiffContextBuilder()
    data = {
        'file_path': 'src/main.py',
        'hunks': [
            {
                'start_line': 45,
                'end_line': 46,
                'before': 'def old_function():\n    return None',
                'after': 'def new_function():\n    return True'
            }
        ]
    }
    
    result = builder.build(data)
    assert result['file'] == 'src/main.py'
    assert result['language'] == 'python'
    assert result['changes']['type'] == 'diff'
    assert len(result['changes']['hunks']) == 1

def test_file_context_builder():
    builder = FileContextBuilder()
    data = {
        'file_path': 'src/main.py',
        'content': 'def process_data():\n    return True',
        'metadata': {
            'language': 'python',
            'size': 1024
        }
    }
    
    result = builder.build(data)
    assert result['file'] == 'src/main.py'
    assert result['language'] == 'python'
    assert result['review_type'] == 'file'
    assert 'process_data' in result['full_content']

def test_directory_context_builder():
    builder = DirectoryContextBuilder()
    data = {
        'files': [
            {
                'path': 'src/main.py',
                'content': 'def main():\n    pass',
                'metadata': {'language': 'python'}
            },
            {
                'path': 'src/utils.py',
                'content': 'def util():\n    pass',
                'metadata': {'language': 'python'}
            }
        ]
    }
    
    result = builder.build(data)
    assert result['review_type'] == 'directory'
    assert len(result['files']) == 2
    assert result['files'][0]['file'] == 'src/main.py'
    assert result['files'][1]['file'] == 'src/utils.py' 