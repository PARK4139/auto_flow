import logging
import traceback
import requests
import re
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def get_auto_flow_version_from_git_hub(
    github_repo_url: str = "https://github.com/wjdgn0117/auto_flow",
    file_path_in_repo: str = "pyproject.toml"
) -> Optional[str]:
    """
    Retrieves the version of the auto_flow project from a specified file in its GitHub repository.

    Args:
        github_repo_url (str): The base URL of the GitHub repository (e.g., "https://github.com/wjdgn0117/auto_flow").
        file_path_in_repo (str): The path to the file containing the version information within the repository
                                 (e.g., "pyproject.toml" or "src/auto_flow/__init__.py").

    Returns:
        Optional[str]: The version string if found, otherwise None.
    """
    logging.info(f"Attempting to get auto_flow version from GitHub repository: {github_repo_url}/{file_path_in_repo}")
    
    # Construct the raw content URL for GitHub
    # Example: https://raw.githubusercontent.com/wjdgn0117/auto_flow/main/pyproject.toml
    # Assumes 'main' branch, but could be made configurable if needed.
    raw_url = github_repo_url.replace("https://github.com/", "https://raw.githubusercontent.com/")
    raw_url = f"{raw_url}/main/{file_path_in_repo}" # Assuming 'main' branch

    try:
        response = requests.get(raw_url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        content = response.text

        version = None
        if file_path_in_repo.endswith("pyproject.toml"):
            # Search for 'version = "X.Y.Z"' pattern
            match = re.search(r'version\s*=\s*"(?P<version>\d+\.\d+\.\d+)"', content)
            if match:
                version = match.group("version")
        elif file_path_in_repo.endswith("__init__.py"):
            # Search for '__version__ = "X.Y.Z"' pattern
            match = re.search(r'__version__\s*=\s*"(?P<version>\d+\.\d+\.\d+)"', content)
            if match:
                version = match.group("version")
        
        if version:
            logging.info(f"Successfully retrieved auto_flow version: {version}")
            return version
        else:
            logging.warning(f"Version information not found in {file_path_in_repo} from {raw_url}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Network or HTTP error fetching {raw_url}: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while parsing version from {raw_url}: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return None

