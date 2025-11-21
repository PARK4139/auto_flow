import sys
from pathlib import Path

# This script is intended to be imported by other scripts in the project
# to ensure that the Python path is set up correctly, especially when
# scripts are run directly.

def setup_paths():
    """
    Adds the necessary project directories to sys.path to allow for absolute
    imports from the project's source and submodule directories.
    """
    # The root of the 'auto_flow' project
    project_root = Path(__file__).resolve().parent.parent

    # The path to the 'pk_system' submodule
    pk_system_path = project_root / 'assets' / 'pk_system'

    # The path to the 'pk_system_sources' directory within the submodule
    pk_system_sources_path = pk_system_path / 'pk_system_sources'

    # Add paths to sys.path if they are not already there.
    # We insert at the beginning to ensure they have priority.
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    if str(pk_system_path) not in sys.path:
        sys.path.insert(0, str(pk_system_path))

    if str(pk_system_sources_path) not in sys.path:
        sys.path.insert(0, str(pk_system_sources_path))

# Run the setup automatically when this module is imported.
setup_paths()
