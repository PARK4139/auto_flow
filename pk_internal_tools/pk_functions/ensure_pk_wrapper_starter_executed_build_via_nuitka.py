import logging
import subprocess
import sys
from pathlib import Path
import textwrap

def ensure_pk_wrapper_starter_executed_build_via_nuitka():
    """
    Automates the process of building the pk_ensure_pk_wrapper_starter_executed.py
    script into a standalone executable using Nuitka.
    """
    # --- Configuration ---
    try:
        project_root = Path(__file__).resolve().parent.parent.parent
    except NameError:
        project_root = Path.cwd()

    target_script_relative = Path("pk_internal_tools/pk_wrappers/pk_ensure_pk_wrapper_starter_executed.py")
    target_script_absolute = project_root / target_script_relative
    output_dir = project_root / "dist"
    
    nuitka_packages = ["nuitka", "zstandard", "ordered-set"]

    logging.debug("--- Starting Nuitka Build Process ---")

    # --- Step 1: Ensure Nuitka and dependencies are installed ---
    logging.debug(f"Ensuring Nuitka and dependencies ({', '.join(nuitka_packages)}) are installed...")
    try:
        install_command = [
            "uv", "pip", "install"
        ] + nuitka_packages
        
        result = subprocess.run(install_command, check=True, capture_output=True, text=True, encoding='utf-8')
        logging.debug("Nuitka and dependencies are installed.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.debug(f"Error: Failed to install/find Nuitka.")
        if isinstance(e, subprocess.CalledProcessError):
            logging.debug(f"Stderr: {e.stderr}")
        logging.debug("Please ensure 'uv' is installed and in your system's PATH.")
        return

    # --- Step 2: Run Nuitka Compilation ---
    logging.debug("--- Starting Nuitka Compilation ---")
    logging.debug(f"Target script: {target_script_absolute}")
    logging.debug(f"Output directory: {output_dir}")
    
    output_dir.mkdir(exist_ok=True)

    nuitka_command = [
        sys.executable,
        "-m", "nuitka",
        "--onefile",
        "--windows-disable-console",
        f"--output-dir={output_dir}",
        str(target_script_absolute)
    ]

    logging.debug(f"Running command: {' '.join(nuitka_command)}")
    
    try:
        process = subprocess.run(
            nuitka_command, 
            check=True, 
            text=True, 
            capture_output=True,
            encoding='utf-8'
        )
        logging.debug("--- Nuitka Compilation Successful ---")
        logging.debug(f"Executable created in: {output_dir}")
        if process.stdout:
            logging.debug("Nuitka stdout:")
            logging.debug(process.stdout)
        if process.stderr:
            logging.debug("Nuitka stderr:")
            logging.debug(process.stderr)

    except subprocess.CalledProcessError as e:
        logging.debug("--- Nuitka Compilation Failed ---")
        logging.debug(f"Return code: {e.returncode}")
        if e.stdout:
            logging.debug("--- Nuitka stdout ---")
            logging.debug(e.stdout)
        if e.stderr:
            logging.debug("--- Nuitka stderr ---")
            logging.debug(e.stderr)
    except FileNotFoundError:
        logging.debug("Error: `python` or `nuitka` command not found.")
        logging.debug("Please ensure Python and Nuitka are correctly installed.")


if __name__ == "__main__":
    ensure_pk_wrapper_starter_executed_build_via_nuitka()
