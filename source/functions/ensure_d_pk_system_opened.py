
def ensure_d_pk_system_opened():
    """
    Ensures that the pk_system directory is opened in the file explorer.
    """
    import os
    import platform
    import subprocess
    import traceback
    from pathlib import Path

    from pk_system.pk_system_sources.pk_system_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_system.pk_system_sources.pk_system_objects.pk_system_directories import get_pk_system_root
    try:
        d_pk_system = get_pk_system_root()

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