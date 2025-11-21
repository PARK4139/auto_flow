import os
import platform
import subprocess
import traceback
from pathlib import Path
import sys

# Add pk_system to sys.path to allow direct execution
try:
    from source.constants.directory_paths import D_PK_SYSTEM_SOURCES_PATH
    if str(D_PK_SYSTEM_SOURCES_PATH) not in sys.path:
        sys.path.insert(0, str(D_PK_SYSTEM_SOURCES_PATH))
except (ImportError, ModuleNotFoundError):
    _project_root = Path(__file__).resolve().parent.parent.parent
    _pk_system_sources = _project_root / "assets" / "pk_system" / "pk_system_sources"
    if str(_pk_system_sources) not in sys.path:
        sys.path.insert(0, str(_pk_system_sources))

from source.constants.directory_paths import D_PK_SYSTEM_PATH
from assets.pk_system.pk_system_sources.pk_system_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

def ensure_d_pk_system_opened():
    """
    Ensures that the pk_system directory is opened in the file explorer.
    """
    try:
        d_pk_system = D_PK_SYSTEM_PATH

        if not d_pk_system.exists() or not d_pk_system.is_dir():
            print(f"Error: Directory not found at {d_pk_system}")
            return

        print(f"Opening directory: {d_pk_system}")

        system = platform.system()
        if system == "Windows":
            os.startfile(d_pk_system)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(d_pk_system)])
        else:  # Linux
            subprocess.run(["xdg-open", str(d_pk_system)])
    except Exception:
        ensure_debug_loged_verbose(traceback)