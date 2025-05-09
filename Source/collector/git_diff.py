from typing import List, Dict, Any
import git
from collections import defaultdict
from models import DiffHunk

class GitDiffCollector:
    """Collects and parses Git diffs."""
    
    def __init__(self, repo_path: str = "."):
        self.repo = git.Repo(repo_path)
        
    def collect(self, ref_spec: str) -> List[Dict[str, Any]]:
        """
        Collect changes between Git references.
        
        Args:
            ref_spec: Git reference spec (e.g., "main..feature-branch")
            
        Returns:
            List of JSON objects containing the changes
        """
        try:
            # Parse ref_spec into target and source
            if ".." in ref_spec:
                source, target = ref_spec.split("..")
            else:
                source = "HEAD~1"  # Default to previous commit
                target = ref_spec
                
            # Get the diff using git diff command
            diff_output = self.repo.git.diff(source, target, unified=3)
            
            # Parse hunks from diff output
            hunks_by_file = defaultdict(list)
            current_file = None
            current_hunk = None
            old_lines = []
            new_lines = []
            current_line = 0
            
            for line in diff_output.splitlines():
                if line.startswith('diff --git'):
                    # New file
                    if current_hunk:
                        current_hunk.old_lines = ''.join(old_lines)
                        current_hunk.new_lines = ''.join(new_lines)
                        hunks_by_file[current_file].append(current_hunk)
                        current_hunk = None
                        old_lines = []
                        new_lines = []
                        current_line = 0
                    # Extract new file path
                    current_file = line.split(' b/')[-1]
                    
                elif line.startswith('@@'):
                    # New hunk
                    if current_hunk:
                        current_hunk.old_lines = ''.join(old_lines)
                        current_hunk.new_lines = ''.join(new_lines)
                        hunks_by_file[current_file].append(current_hunk)
                        old_lines = []
                        new_lines = []
                    
                    try:
                        # Parse hunk header
                        # Format: @@ -start,count +start,count @@
                        header = line.split('@@')[1].strip()
                        old_info, new_info = header.split(' ')
                        new_start = int(new_info.split(',')[0][1:])
                        current_line = new_start
                        
                        current_hunk = DiffHunk(
                            file_path=current_file,
                            start_line=new_start,
                            end_line=new_start,  # Will be updated
                            old_lines="",
                            new_lines=""
                        )
                    except (IndexError, ValueError) as e:
                        print(f"Warning: Failed to parse hunk header: {line}")
                        continue
                        
                elif current_hunk and line:
                    if line.startswith('-'):
                        old_lines.append(line[1:] + '\n')
                    elif line.startswith('+'):
                        new_lines.append(line[1:] + '\n')
                        current_hunk.end_line = current_line
                        current_line += 1
                    else:
                        # Context line
                        current_line += 1
            
            # Add the last hunk
            if current_hunk:
                current_hunk.old_lines = ''.join(old_lines)
                current_hunk.new_lines = ''.join(new_lines)
                hunks_by_file[current_file].append(current_hunk)
            
            # Convert to final format
            result = []
            for file_path, hunks in hunks_by_file.items():
                result.append({
                    'file_path': file_path,
                    'hunks': [h.to_dict() for h in hunks]
                })
            
            return result
            
        except git.GitCommandError as e:
            raise ValueError(f"Invalid Git reference: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to collect Git diff: {e}")
