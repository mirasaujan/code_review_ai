# Collector Component

## Overview
The Collector component is responsible for building the work-set of files to be reviewed and preparing them for LLM analysis. It handles three main scenarios:
1. Git diff collection
2. Single file collection
3. Directory collection

## Components

### GitDiff
- Collects modified files and line spans between Git references
- Uses GitPython or subprocess for diff operations
- Handles both target and source branch comparisons
- Defaults to HEAD if source branch is not provided
- Prepares hunks for LLM analysis

### FileLoader
- Handles single file review scenarios
- Reads file content
- Ensures file is readable and accessible
- Prepares file content for LLM analysis

### DirectoryScanner
- Enumerates files recursively within provided path
- Honors glob patterns for file inclusion/exclusion
- Supports cascading directory review
- Filters files based on extensions and paths
- Groups files for batch LLM analysis

## Usage Examples

### Git Diff Collection
```python
# Example: Collect changes between branches
collector = GitDiff()
changes = collector.collect("main..feature-branch")
```

### Single File Collection
```python
# Example: Collect single file
loader = FileLoader()
file_content = loader.load("src/main.py")
```

### Directory Collection
```python
# Example: Collect files in directory using patterns from codereview.yaml
scanner = DirectoryScanner()
# Patterns are read from repository's codereview.yaml
files = scanner.scan("src/")
```

## Configuration
The collector reads include/exclude patterns from the repository's `codereview.yaml`:
```yaml
# codereview.yaml in repository root
include:
  - "*.py"
  - "*.js"
  - "*.ts"
exclude:
  - "tests/*"
  - "node_modules/*"
  - "*.test.*"
```

## Error Handling
- Bad Git references: Log and continue
- Unreadable files: Log and skip
- Invalid paths: Clear error messages
- Permission issues: Appropriate error handling

## Integration
- Works with Context Builder to prepare files for LLM analysis
- Provides files for review
- Supports both relative and absolute paths
- Maintains file metadata for context building
- Prepares content in LLM-friendly format

## Performance Considerations
- Efficient file reading
- Minimal memory footprint
- Parallel processing for directory scanning
