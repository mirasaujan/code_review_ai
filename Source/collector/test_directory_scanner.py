"""
Test file for Directory collector.
"""

import os
import json
import yaml
from collector import Directory

def create_test_files():
    """Create test directory structure and files."""
    # Create test directory
    os.makedirs("test_dir/src", exist_ok=True)
    os.makedirs("test_dir/empty_dir", exist_ok=True)
    os.makedirs("test_dir/src/some_dir", exist_ok=True)
    
    # Create test files
    files = {
        "test_dir/src/main.py": "def main():\n    pass",
        "test_dir/src/utils.py": "def util():\n    pass",
        "test_dir/src/test_main.py": "def test_main():\n    pass",
        "test_dir/src/some_dir/test_main2.py": "def test_main():\n    pass",
        "test_dir/src/some_dir/test_main4.py": "def test_main():\n    pass",
        "test_dir/README.md": "# Test Project"
    }
    
    for path, content in files.items():
        if content == "":
            continue
        with open(path, 'w') as f:
            f.write(content)
            
    # Create config file
    config = {
        'include': ['*.py'],
        'exclude': ['*test*.py']
    }
    
    with open('test_dir/codereview.yaml', 'w') as f:
        yaml.dump(config, f)
        
def cleanup():
    """Remove test directory and files."""
    import shutil
    if os.path.exists("test_dir"):
        shutil.rmtree("test_dir")

def main():
    try:
        create_test_files()
        
        # Test directory scanning
        collector = Directory("test_dir/codereview.yaml")
        
        # Test main directory
        print("Testing main directory:")
        results = collector.collect("test_dir")
        print(json.dumps({
            'files': [r.to_dict() for r in results]
        }, indent=2))
        
        # Test empty directory
        print("\nTesting empty directory:")
        results = collector.collect("test_dir/empty_dir")
        print(json.dumps({
            'files': [r.to_dict() for r in results]
        }, indent=2))
        
    finally:
        cleanup()

if __name__ == "__main__":
    main() 