import textwrap
import os
import sys
import subprocess
import logging
from pathlib import Path

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def ensure_pk_sync_service_client_started():
    """
    Activates the appropriate virtual environment and starts the Watchdog sync client.
    """
    logging.info("Starting Watchdog Sync Client...")

    # Import project root from system directories definition
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    project_root = d_pk_root
    
    # Determine OS and virtual environment path
    if sys.platform == "win32":
        venv_path = project_root / ".venv"
        python_executable = venv_path / "Scripts" / "python.exe"
        
        command = [
            str(python_executable),
            "-m",
            "pk_internal_tools.pk_sync_service.pk_sync_service_client", # Run as a module
        ]
        shell = False
        
    elif sys.platform.startswith("linux"): # Includes WSL
        venv_path = project_root / ".venv"
        activate_script = venv_path / "bin" / "activate"
        python_executable = venv_path / "bin" / "python"
        
        command = [
            "bash", "-c",
            f"source {activate_script} && {python_executable} -m pk_internal_tools.pk_sync_service.pk_sync_service_client"
        ]
        shell = True
    else:
        logging.error(f"Unsupported operating system: {sys.platform}")
        return

    if not venv_path.exists():
        logging.error(f"Virtual environment not found at {venv_path}. Please ensure it's created and activated.")
        logging.info("You might need to run 'uv venv' or 'python -m venv .venv' / '.venv'")
        return

    logging.info(f"Using Python executable: {python_executable}")
    logging.info(f"Executing command: {' '.join(command) if not shell else command[2]}")

    try:
        subprocess.run(command, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start sync client: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    ensure_pk_sync_service_client_started()