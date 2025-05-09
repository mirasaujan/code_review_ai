"""
Test file for File collector.
"""

import os
import json
from collector import File

def main():
    # Create a test file
    test_file = "test_file.py"
    test_content = """def process_data():
    data = fetch_data()
    return transform(data)"""
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_content)
            
        # Test file loading
        collector = File()
        result = collector.collect(test_file)
        
        # Print result in JSON format
        print(json.dumps(result.to_dict(), indent=2))
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    main() 