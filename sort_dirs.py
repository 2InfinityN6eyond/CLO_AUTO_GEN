import os
from pathlib import Path
from datetime import datetime

def get_dir_mtime(dir_path):
    """Get the last modified time of a directory and its contents."""
    try:
        # Get the directory's own modification time
        dir_mtime = os.path.getmtime(dir_path)
        
        # Get the latest modification time of all files in the directory
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_mtime = os.path.getmtime(file_path)
                    dir_mtime = max(dir_mtime, file_mtime)
                except (OSError, FileNotFoundError):
                    continue
                    
        return dir_mtime
    except (OSError, FileNotFoundError):
        return 0

def sort_directories_by_mtime(directory_path, reverse=True):
    """
    Sort subdirectories by their last modified time.
    
    Args:
        directory_path (str): Path to the parent directory
        reverse (bool): If True, sort in descending order (newest first)
        
    Returns:
        list: List of tuples containing (directory_name, last_modified_time)
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"Directory does not exist: {directory_path}")
    
    # Get all subdirectories
    subdirs = [d for d in os.listdir(directory_path) 
              if os.path.isdir(os.path.join(directory_path, d))]
    
    # Create list of (directory_name, mtime) tuples
    dirs_with_mtime = []
    for dir_name in subdirs:
        full_path = os.path.join(directory_path, dir_name)
        mtime = get_dir_mtime(full_path)
        dirs_with_mtime.append((dir_name, mtime))
    
    # Sort by modification time
    sorted_dirs = sorted(dirs_with_mtime, 
                        key=lambda x: x[1], 
                        reverse=reverse)
    
    return sorted_dirs

def print_sorted_directories(directory_path, reverse=True):
    """
    Print sorted directories with their last modified times in a readable format.
    
    Args:
        directory_path (str): Path to the parent directory
        reverse (bool): If True, sort in descending order (newest first)
    """
    sorted_dirs = sort_directories_by_mtime(directory_path, reverse)
    
    print(f"\nDirectories in {directory_path} sorted by last modified time:")
    print("-" * 80)
    print(f"{'Directory Name':<40} {'Last Modified':<30}")
    print("-" * 80)
    
    for dir_name, mtime in sorted_dirs:
        mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{dir_name:<40} {mtime_str:<30}")

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = "."  # Current directory
        
    print_sorted_directories(directory_path) 