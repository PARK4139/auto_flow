def ensure_empty_directory_pnx_printed(root_dir: str) -> list:
    import os
    empty_dirs = []
    for current_dir, subdirs, files in os.walk(root_dir, topdown=False):
        # Check if the directory is empty (no files and no non-empty subdirs)
        if not subdirs and not files:
            empty_dirs.append(current_dir)
    return empty_dirs
