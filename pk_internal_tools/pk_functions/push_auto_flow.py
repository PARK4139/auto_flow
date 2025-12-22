
import subprocess
import logging
import sys
import traceback
from pathlib import Path

from pk_internal_tools.pk_wrappers.ensure_pk_cicd_executed_based_on_pk_system import ensure_pk_wrapper_starting_routine_done


def run_command(command, cwd):
    """Executes a command and logs its output."""
    logging.info(f"Executing command: {' '.join(command)} in {cwd}")
    try:
        process = subprocess.run(
            command,
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if process.stdout:
            logging.debug(f"STDOUT:\n{process.stdout}")
        if process.stderr:
            logging.warning(f"STDERR:\n{process.stderr}")
        logging.info("Command executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with exit code {e.returncode}")
        if e.stdout:
            logging.error(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            logging.error(f"STDERR:\n{e.stderr}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while running command: {e}")
        logging.debug(traceback.format_exc())
        return False


if __name__ == "__main__":
    ensure_pk_wrapper_starting_routine_done(__file__, traceback)

    d_pk_root = Path(__file__).resolve().parent.parent.parent.parent
    auto_flow_dir = d_pk_root / 'auto_flow'
    remote_url = "https://github.com/your-username/auto_flow.git"

    if not auto_flow_dir.exists():
        logging.error(f"Directory not found: {auto_flow_dir}")
        sys.exit(1)

    logging.info(f"Setting up remote for {auto_flow_dir}")

    # Add remote
    if not run_command(["git", "remote", "add", "origin", remote_url], cwd=auto_flow_dir):
        logging.warning("Failed to add remote. It might already exist. Trying to set url.")
        if not run_command(["git", "remote", "set-url", "origin", remote_url], cwd=auto_flow_dir):
            logging.error("Failed to set remote url.")
            # We can still try to push

    # Push to remote
    logging.info("Pushing to the remote repository...")
    if not run_command(["git", "push", "-u", "origin", "master"], cwd=auto_flow_dir):
        logging.info("Pushing to master failed, trying main branch...")
        if not run_command(["git", "push", "-u", "origin", "main"], cwd=auto_flow_dir):
            logging.error("Failed to push to both master and main branches.")
        else:
            logging.info("Successfully pushed to main branch.")
    else:
        logging.info("Successfully pushed to master branch.")

