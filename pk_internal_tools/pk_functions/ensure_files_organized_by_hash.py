import os
import hashlib
import shutil
import logging
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_pnx_moved import ensure_pnx_moved

def _remove_empty_dirs(path_to_scan: Path):
    """Recursively remove empty subdirectories."""
    for dirpath, dirnames, filenames in os.walk(path_to_scan, topdown=False):
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                logging.debug(f"Removed empty directory: {dirpath}")
            except OSError as e:
                logging.error(f"Error removing directory {dirpath}: {e}")

def ensure_files_organized_by_hash(source_directory: Path, destination_directory: Path, hash_algo: str = 'sha1', depth: int = 2, chunk_size: int = 2):
    """
    Organizes files from a source directory into a new hash-based directory structure.

    :param source_directory: The directory to scan for files.
    :param destination_directory: The root directory where the new hash structure will be created.
    :param hash_algo: The hashing algorithm to use (e.g., 'sha1', 'md5').
    :param depth: How many levels of subdirectories to create.
    :param chunk_size: How many characters of the hash to use for each directory level.
    """
    logging.info(f"Starting hash-based organization for: {source_directory}")
    logging.info(f"Destination: {destination_directory}")
    logging.info(f"Parameters: algo={hash_algo}, depth={depth}, chunk_size={chunk_size}")

    if source_directory == destination_directory:
        logging.error("Source and destination directories cannot be the same.")
        return

    destination_directory.mkdir(parents=True, exist_ok=True)
    
    moved_count = 0
    failed_count = 0

    # Using rglob to find all files recursively
    files_to_move = [f for f in source_directory.rglob('*') if f.is_file()]
    total_files = len(files_to_move)
    logging.info(f"Found {total_files} files to process.")

    for file_path in files_to_move:
        try:
            filename = file_path.name
            # Use filename bytes to ensure consistent hashing
            hasher = hashlib.new(hash_algo)
            hasher.update(filename.encode('utf-8'))
            file_hash = hasher.hexdigest()

            # Build destination path
            path_parts = [file_hash[i:i+chunk_size] for i in range(0, depth * chunk_size, chunk_size)]
            dest_subdir = destination_directory.joinpath(*path_parts)
            dest_subdir.mkdir(parents=True, exist_ok=True)

            moved_pnx = ensure_pnx_moved(
                pnx=file_path,
                d_dst=dest_subdir,
                with_overwrite=False,
                sequential_mode=True,
                timestamp_mode=False # Use sequential mode as requested
            )
            if moved_pnx:
                logging.debug(f"Moved: {file_path} -> {moved_pnx}")
                moved_count += 1
            else:
                logging.error(f"Failed to move {file_path} using ensure_pnx_moved.")
                failed_count += 1
        except Exception as e:
            logging.error(f"Failed to move {file_path}: {e}")
            failed_count += 1

    logging.info("File moving process completed.")
    
    logging.info("Cleaning up empty directories in source...")
    _remove_empty_dirs(source_directory)
    logging.info("Cleanup complete.")

    logging.info(f"Organization summary: Total={total_files}, Moved={moved_count}, Failed={failed_count}")

    return {"total": total_files, "moved": moved_count, "failed": failed_count}
