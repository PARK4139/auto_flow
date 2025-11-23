import sys
from pathlib import Path

# This script is intended to be imported by other scripts in the project
# to ensure that the Python path is set up correctly, especially when
# scripts are run directly.

def setup_paths():
    """
    Adds the necessary project directories to sys.path to allow for absolute
    imports from the project's source directories.
    
    Note: pk_system is now installed as a library via pip/uv, so it doesn't need
    to be added to sys.path manually.
    """
    # The root of the 'auto_flow' project
    project_root = Path(__file__).resolve().parent.parent

    # Add project root to sys.path if it's not already there.
    # We insert at the beginning to ensure it has priority.
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# Run the setup automatically when this module is imported.
setup_paths()
