import tempfile
import os
import logging

def ensure_download_directory_is_ready(download_dir=None):
    """
    Ensures a download directory is ready.
    If download_dir is provided, it checks if it exists and is writable. If not, it tries to create it.
    If download_dir is not provided, it uses the system's temporary directory.
    Returns the path to the ready download directory.
    """
    if download_dir is None:
        download_dir = tempfile.gettempdir()

    try:
        # Check if the directory exists, and if not, create it.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            logging.info(f"Created download directory: {download_dir}")
        
        # Check if the directory is writable.
        if not os.access(download_dir, os.W_OK):
            raise PermissionError(f"Download directory is not writable: {download_dir}")

        return download_dir

    except Exception as e:
        logging.error(f"Could not prepare download directory {download_dir}: {e}")
        # Fallback to temp dir if the provided one fails
        if download_dir != tempfile.gettempdir():
            logging.warning(f"Falling back to system temporary directory.")
            return ensure_download_directory_is_ready(None)
        else:
            # If even the temp dir fails, we have a big problem.
            raise
