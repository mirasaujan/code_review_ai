# Context Builder Component

## Overview
The Context Builder is responsible for structuring file content and metadata into a format suitable for LLM analysis. It handles three main scenarios:
1. Git diff context
2. Single file context
3. Directory file context

## Components

### DiffContextBuilder
- Builds structured context for git diffs
- Includes before/after content for changed lines
- Preserves surrounding context for better analysis
- Handles both additions and deletions

### FileContextBuilder
- Prepares single file content for analysis
- Includes file metadata (path, language)
- Preserves file structure and formatting
- Handles file encoding and line endings

### DirectoryContextBuilder
- Groups related files for batch analysis
- Maintains file relationships and dependencies
- Optimizes context size for LLM processing
- Handles large directory structures

## Usage Examples

### Git Diff Context
**Input**
```python
# Example: Build context for git diff
builder = DiffContextBuilder()
context = builder.build({
    'file_path': 'src/main.py',
    'hunks': [
        {
            'start_line': 45,
            'end_line': 46,
            'before': 'def old_function():\n    return None',
            'after': 'def new_function():\n    return True'
        }
    ]
})
```

**Output**
```json
{
  "file": "src/main.py",
  "language": "python",
  "changes": {
    "type": "diff",
    "hunks": [
      {
        "start_line": 45,
        "end_line": 46,
        "before": "def old_function():\n    return None",
        "after": "def new_function():\n    return True"
      }
    ]
  },
  "full_content": "... entire file content ..."
}
```

### Single File Context
**Input**
```python
# Example: Build context for single file
builder = FileContextBuilder()
context = builder.build({
    'file_path': 'src/main.py',
    'content': 'def process_data():\n    data = fetch_data()\n    return transform(data)',
    'metadata': {
        'language': 'python',
        'size': 1024
    }
})
```
**Output**
```json
{
  "file": "src/main.py",
  "language": "python",
  "review_type": "file",
  "full_content": "def process_data():\n    data = fetch_data()\n    return transform(data)"
}
```

### Directory Context
**Input**
```python
# Example: Build context for directory
builder = DirectoryContextBuilder()
context = builder.build({
    'files': [
        {
            'path': 'src/main.py',
            'content': '...',
            'metadata': {...}
        },
        {
            'path': 'src/utils.py',
            'content': '...',
            'metadata': {...}
        }
    ]
})
```

**Output**
```json
{
  "file": "src/main.py",
  "language": "python",
  "review_type": "directory",
  "full_content": "def process_data():\n    data = fetch_data()\n    return transform(data)"
}
```

## Error Handling
- Invalid file encodings: Attempt recovery, fallback to binary
- Missing files: Clear error messages
- Large files: Chunking and size limits
- Memory constraints: Streaming for large contexts

## Integration
- Works with Collector for file content
- Prepares data for LLM analysis
- Maintains consistent context structure
- Supports all review modes

## Performance Considerations
- Efficient file reading
- Memory usage optimization
- Context size management
- Batch processing support
