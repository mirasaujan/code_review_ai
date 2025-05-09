from collector import GitDiff
import json
from pprint import pprint
import os
import argparse
import sys

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Review changes in a Git repository')
    parser.add_argument('repo_path', nargs='?', default=None,
                      help='Path to the Git repository (default: current directory)')
    parser.add_argument('--ref', default='HEAD~1..HEAD',
                      help='Git reference spec (default: HEAD~1..HEAD)')
    
    args = parser.parse_args()
    
    # Use provided repo path or default to two levels up
    if args.repo_path:
        repo_path = args.repo_path
    else:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    try:
        # Initialize GitDiff with repository path
        collector = GitDiff(repo_path)
        
        print(f"Getting diff in repository: {repo_path}")
        print(f"Reference spec: {args.ref}")
        
        # Get diff between specified references
        hunks = collector.collect(args.ref)
        
        if not hunks:
            print("No changes found!")
            return
            
        # Print each hunk in JSON format
        print("\nChanges in JSON format:")
        print(json.dumps(hunks, indent=2))
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 