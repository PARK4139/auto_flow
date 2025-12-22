import logging
import os
import shutil
import stat
import subprocess
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name


def handle_rmtree_error(func, path, exc_info):
    """
    Error handler for shutil.rmtree.
    If the error is a permission error, it tries to change the file's permissions and re-attempt the operation.
    """
    # Check if it's a permission error
    if not isinstance(exc_info[1], PermissionError):
        # If not a permission error, re-raise the exception
        raise exc_info[1]

    logging.warning(f"Permission error deleting {path}. Attempting to change permissions...")
    try:
        # Change the file to be writable
        os.chmod(path, stat.S_IWRITE)
        # Try to execute the function again (e.g., os.unlink)
        func(path)
    except Exception as e:
        logging.error(f"Failed to handle rmtree error for {path}: {e}")
        raise


# pk_system 프로젝트의 로깅 규칙을 준수합니다.
# ensure_pk_system_log_initialized()는 래퍼 스크립트에서 호출되므로, 함수 내에서는 basicConfig를 호출하지 않습니다.


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


def _delete_existing_directory(path):
    """Deletes the specified directory if it exists."""
    if path.exists():
        logging.info(f"Directory '{path}' already exists. Deleting it.")
        try:
            shutil.rmtree(path, onerror=handle_rmtree_error)
            logging.info(f"Successfully deleted directory: {path}")
        except Exception as e:
            logging.error(f"Failed to delete directory {path}: {e}")
            raise
    else:
        logging.info(f"Directory '{path}' does not exist. No need to delete.")


def _copy_project(source_path, dest_path, ignore_patterns):
    """Copies the project from source to destination, ignoring specified patterns."""
    logging.info(f"Copying project from '{source_path}' to '{dest_path}'...")
    try:
        shutil.copytree(
            source_path,
            dest_path,
            ignore=shutil.ignore_patterns(*ignore_patterns),
            dirs_exist_ok=True
        )
        logging.info("Project copied successfully.")
    except Exception as e:
        logging.error(f"Failed to copy project: {e}")
        raise


def _replace_string_in_files(target_dir, old_str, new_str):
    """Replaces all occurrences of old_str with new_str in all text files in a directory."""
    logging.info(f"Replacing '{old_str}' with '{new_str}' in all text files under '{target_dir}'...")
    for root, _, files in os.walk(target_dir):
        for filename in files:
            file_path = Path(root) / filename
            try:
                # Process only text files
                content = file_path.read_text(encoding='utf-8')
                if old_str in content:
                    new_content = content.replace(old_str, new_str)
                    file_path.write_text(new_content, encoding='utf-8')
                    logging.debug(f"Replaced content in: {file_path}")
            except (UnicodeDecodeError, IOError) as e:
                logging.debug(f"Skipping binary or unreadable file {file_path}: {e}")
            except Exception as e:
                logging.error(f"An error occurred while processing file {file_path}: {e}")


def _rename_files_and_dirs(target_dir, old_str, new_str):
    """Renames files and directories containing old_str."""
    logging.info(f"Renaming files and directories containing '{old_str}' to '{new_str}'...")
    paths_to_rename = []
    for root, dirs, files in os.walk(str(target_dir), topdown=False):
        for name in files + dirs:
            if old_str in name:
                old_path = Path(root) / name
                new_name = name.replace(old_str, new_str)
                new_path = Path(root) / new_name
                paths_to_rename.append((old_path, new_path))

    for old_path, new_path in paths_to_rename:
        try:
            if old_path.exists():
                old_path.rename(new_path)
                logging.debug(f"Renamed '{old_path}' to '{new_path}'")
        except Exception as e:
            logging.error(f"Failed to rename '{old_path}' to '{new_path}': {e}")


def ensure_pk_cicd_executed_based_on_pk_system(d_pk_root):
    """
    Creates the auto_flow project based on pk_system.
    """
    source_project_name = "pk_system"
    new_project_name = "auto_flow"

    source_path = d_pk_root / source_project_name
    dest_path = d_pk_root / new_project_name

    blacklist = [
        '.git', '.idea', '.vscode', '.venv', '__pycache__', '.pytest_cache',
        '*.pyc', '*.pyo', '*.pyd', 'pk_logs', 'latest_logs', 'archived_logs',
        'downloaded_files', '.gemini', '.cursor', 'auto_flow', '.pk_system',
        '*.egg-info', 'dist', 'build'
    ]

    try:
        # 1. Delete existing auto_flow directory
        _delete_existing_directory(dest_path)

        # 2. Copy pk_system to auto_flow
        _copy_project(source_path, dest_path, blacklist)

        # 3. Replace strings in content
        _replace_string_in_files(dest_path, source_project_name, new_project_name)
        _replace_string_in_files(dest_path, source_project_name.replace("_", "-"), new_project_name.replace("_", "-"))

        # 4. Rename files and directories
        _rename_files_and_dirs(dest_path, source_project_name, new_project_name)

        # 5. Initialize git repository
        logging.info("Initializing new Git repository...")
        if not run_command(["git", "init"], cwd=dest_path):
            raise Exception("Git init failed")
        if not run_command(["git", "add", "."], cwd=dest_path):
            raise Exception("Git add failed")
        commit_message = f"Initial commit: Cloned from {source_project_name}"
        if not run_command(["git", "commit", "-m", commit_message], cwd=dest_path):
            logging.warning("Git commit failed. Maybe no changes to commit.")

        # 6. Run test
        run_cmd_path = dest_path / "run.cmd"
        if run_cmd_path.exists():
            logging.info("Executing run.cmd to test the new project...")
            run_command([str(run_cmd_path)], cwd=dest_path)
        else:
            logging.warning("run.cmd not found, skipping test execution.")

        # 7. Git push
        func_n = get_caller_name()
        remote_url = ensure_value_completed(
            key_name="auto_flow_remote_url",
            func_n=func_n,
            guide_text="Please enter the remote git repository URL for auto_flow:"
        )

        if remote_url and remote_url.strip():
            remote_url = remote_url.strip()
            logging.info(f"Adding remote 'origin' with URL: {remote_url}")
            run_command(["git", "remote", "add", "origin", remote_url], cwd=dest_path)

            logging.info("Pushing to the remote repository...")
            if not run_command(["git", "push", "-u", "origin", "master"], cwd=dest_path):
                # try main branch if master fails
                logging.info("Pushing to master failed, trying main branch...")
                if not run_command(["git", "push", "-u", "origin", "main"], cwd=dest_path):
                    logging.error("Failed to push to both master and main branches.")
        else:
            logging.warning("No remote URL provided. Skipping git push.")

        logging.info("auto_flow project creation process completed successfully!")
        return True

    except Exception as e:
        logging.error(f"An error occurred during the process: {e}")
        logging.error(traceback.format_exc())
        return False
