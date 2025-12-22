import logging
import subprocess
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done



def setup_auto_flow_venv():
    ensure_pk_wrapper_starting_routine_done(__file__, traceback)

    d_pk_root = Path(__file__).resolve().parent.parent.parent.parent
    auto_flow_dir = d_pk_root / 'auto_flow'

    if not auto_flow_dir.exists():
        logging.error(f"Directory not found: {auto_flow_dir}")
        return

    logging.info(f"Setting up virtual environment in {auto_flow_dir}")

    # Using 'uv.exe' from the parent project for now.
    uv_executable = d_pk_root / 'pk_system' / 'uv.exe'
    if not uv_executable.exists():
        # Fallback to assuming uv is in PATH
        uv_executable = 'uv'
    else:
        uv_executable = str(uv_executable)

    # Create virtual environment
    if not _run_command([uv_executable, "venv"], cwd=auto_flow_dir):
        logging.error("Failed to create virtual environment.")
        return

    # Install dependencies
    if not _run_command([uv_executable, "sync"], cwd=auto_flow_dir):
        logging.error("Failed to install dependencies.")
        return

    logging.info("Virtual environment setup completed successfully.")


