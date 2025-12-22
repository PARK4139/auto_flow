import logging
import traceback
from pathlib import Path
from typing import Optional, Literal

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_auto_flow_version_from_git_hub import get_auto_flow_version_from_git_hub
import re

# We need a function to get the local version. Let's define it here.
def _get_local_version_from_file(file_path: Path) -> Optional[str]:
    """
    Reads the version from a local pyproject.toml or __init__.py file.
    """
    if not file_path.exists():
        logging.warning(f"Local version file not found: {file_path}")
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
        version = None
        if file_path.name == "pyproject.toml":
            match = re.search(r'version\s*=\s*"(?P<version>\d+\.\d+\.\d+)"', content)
            if match:
                version = match.group("version")
        elif file_path.name == "__init__.py":
            match = re.search(r'__version__\s*=\s*"(?P<version>\d+\.\d+\.\d+)"', content)
            if match:
                version = match.group("version")
        
        if version:
            logging.info(f"Found local version {version} in {file_path}")
            return version
        else:
            logging.warning(f"Could not find version info in {file_path}")
            return None
    except Exception as e:
        logging.error(f"Error reading local version from {file_path}: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return None


def compare_auto_flow_versions_between_local_and_remote_branch_of_git_hub(
    local_project_path: Path,
    github_repo_url: str = "https://github.com/wjdgn0117/auto_flow",
) -> Literal["local_is_newer", "remote_is_newer", "same", "error", "not_found"]:
    """
    Compares the local version of the auto_flow project with the remote version on GitHub.

    Args:
        local_project_path (Path): The root path of the local auto_flow project checkout.
        github_repo_url (str): The URL of the GitHub repository.

    Returns:
        Literal["local_is_newer", "remote_is_newer", "same", "error", "not_found"]:
        The result of the comparison.
    """
    logging.info(f"Starting version comparison for auto_flow project.")
    logging.info(f"Local path: {local_project_path}")
    logging.info(f"Remote repo: {github_repo_url}")

    try:
        # 1. Get local version
        # Assuming the version is in pyproject.toml
        local_version_file = local_project_path / "pyproject.toml"
        local_version = _get_local_version_from_file(local_version_file)

        # 2. Get remote version
        # Assuming the version is in the same file on the 'main' branch
        remote_version = get_auto_flow_version_from_git_hub(
            github_repo_url=github_repo_url,
            file_path_in_repo="pyproject.toml"
        )

        if not local_version or not remote_version:
            logging.error("Could not determine either local or remote version. Comparison failed.")
            return "not_found"

        logging.info(f"Local version: {local_version} | Remote version: {remote_version}")

        # 3. Compare versions
        # Using simple string comparison for versions like "X.Y.Z"
        # For more complex scenarios, a library like 'packaging.version' would be better.
        if local_version > remote_version:
            logging.info("Local version is newer than remote version.")
            return "local_is_newer"
        elif remote_version > local_version:
            logging.info("Remote version is newer than local version.")
            return "remote_is_newer"
        else:
            logging.info("Local and remote versions are the same.")
            return "same"

    except Exception as e:
        logging.error(f"An unexpected error occurred during version comparison: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return "error"
