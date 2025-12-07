import textwrap
import os
import sys
import subprocess
import logging
from pathlib import Path

# --- Logging Setup ---
# This wrapper script will handle its own basic logging,
# as the main application's logging might not be initialized yet.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def ensure_pk_sync_service_server_started():
    """
    Activates the appropriate virtual environment and starts the FastAPI sync server.
    """
    logging.info("Starting FastAPI Sync Server...")

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
            "uvicorn",
            "pk_internal_tools.pk_sync_service.pk_sync_service_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        shell = False # subprocess.run with list of args is safer
        
    elif sys.platform.startswith("linux"): # Includes WSL
        venv_path = project_root / ".venv"
        activate_script = venv_path / "bin" / "activate"
        python_executable = venv_path / "bin" / "python"
        
        # For Linux, sourcing the activate script and then running uvicorn
        # in a single shell command is common.
        command = [
            "bash", "-c",
            f"source {activate_script} && {python_executable} -m uvicorn pk_internal_tools.pk_sync_service.pk_sync_service_server:app --host 0.0.0.0 --port 8000 --reload"
        ]
        shell = True # Needs shell=True for 'source' and '&&'
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
        # Start the server as a subprocess. It will block.
        subprocess.run(command, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start sync server: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    ensure_pk_sync_service_server_started()