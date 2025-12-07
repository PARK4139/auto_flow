import sys
import logging
from pathlib import Path
import re
import importlib.metadata

from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


class ProjectInfo:
    """Class representing project info loaded from pyproject.toml."""

    def __init__(self, data: dict):
        self.data = data

    def __repr__(self):
        try:
            if self.data and isinstance(self.data, dict):
                name = get_project_name(self) or "N/A"
                version = get_pk_version(self) or "N/A"
                description = self.data.get("description", "N/A")
                authors = self.data.get("authors", [])

                # Format author details
                author_details = []
                if isinstance(authors, list):
                    for author in authors:
                        author_details.append(f"  Name: {author.get('name', 'N/A')}")
                        author_details.append(f"  Email: {author.get('email', 'N/A')}")
                else:
                    author_details.append(f"  {authors}")
                author_str = "\n".join(author_details)

                uv_version = get_uv_version() # Get uv version
                # Build the final string with correct colors
                return (
                    f"Project Name: {name}\n"
                    f"Project Version: {version}\n"
                    f"Project Description: {description}\n"
                    f"Project Author(s):\n{author_str}\n"
                    f"Project Python version: {sys.version}\n"
                    f"Project Virtual Environment Version : uv {uv_version}\n" # Added uv version
                    f"Project Virtual Environment Path: {sys.prefix}\n" # Added virtual environment path
                )
            else:
                return (
                    f"Failed to load {PK_ANSI_COLOR_MAP['RED']}pyproject.toml"
                    f"{PK_ANSI_COLOR_MAP['RESET']} or cache issue occurred.\n"
                    f"{PK_ANSI_COLOR_MAP['BRIGHT_MAGENTA']}Debug Info: "
                    f"project_info = {self.data}, type = {type(self.data)}"
                    f"{PK_ANSI_COLOR_MAP['RESET']}"
                )
        except Exception as e:
            return f"{PK_ANSI_COLOR_MAP['RED']}[ProjectInfo __repr__ Error]{PK_ANSI_COLOR_MAP['RESET']} {e}"

import subprocess

def get_uv_version():
    """Attempts to get the uv version by running 'uv --version'."""
    try:
        # Run uv --version command
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=False, # Do not raise CalledProcessError for non-zero exit codes
            encoding="utf-8"
        )
        # Output is typically "uv 0.1.x (hash)"
        match = re.search(r"uv (\d+\.\d+\.\d+)", result.stdout)
        if match:
            return match.group(1)
    except (FileNotFoundError) as e: # FileNotFoundError if 'uv' command is not found
        logging.debug(f"Could not get uv version (FileNotFoundError): {e}")
    except Exception as e: # Catch other potential errors
        logging.debug(f"Could not get uv version (General Error): {e}")
    return "N/A"


def get_project_name(project_info: ProjectInfo):
    """Extract project name from ProjectInfo."""
    return project_info.data.get("name")


def get_pk_version(project_info: ProjectInfo):
    """Extract project version from ProjectInfo, handling dynamic versioning."""
    # Try to get version from the dynamically generated _version.py file
    version_file_path = Path(__file__).parent.parent / "pk_info" / "_version.py"
    if version_file_path.exists():
        try:
            with open(version_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Look for a line like __version__ = "X.Y.Z"
            match = re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", content)
            if match:
                return match.group(1)
        except Exception as e:
            logging.warning(f"Failed to read version from {version_file_path}: {e}")

    # Fallback: Try to get from importlib.metadata if the package is installed
    try:
        # Assuming the package name is "pk_system" as per pyproject.toml
        return importlib.metadata.version("pk_system")
    except importlib.metadata.PackageNotFoundError:
        pass # Package not installed or version not found via metadata

    # Final fallback if dynamic versioning or metadata fails
    return None # Explicitly return None if version cannot be determined


@ensure_seconds_measured
def get_project_info_from_pyproject():
    import toml
    from pk_internal_tools.pk_objects.pk_files import F_PYPROJECT_TOML
    from pathlib import Path

    try:
        pyproject_path: Path = F_PYPROJECT_TOML

        if not pyproject_path.exists():
            # TODO : print in red (file missing)
            return None

        # Load pyproject.toml
        with open(pyproject_path, "r", encoding="utf-8") as f:
            config = toml.load(f)

        # Extract [project] section
        if "project" in config:
            project_info = config["project"].copy()
            return ProjectInfo(project_info)
        else:
            return None

    except Exception:
        return None
