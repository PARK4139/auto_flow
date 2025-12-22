import logging
from pathlib import Path
from pk_internal_tools.pk_objects.pk_files import F_BIT_TORRENT_EXE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

def ensure_bittorrent_exe_opened():
    """Ensures the BitTorrent executable is opened."""
    
    # Convert the imported path string to a Path object for robust handling
    exe_path = Path(F_BIT_TORRENT_EXE)
    
    if not exe_path.exists():
        logging.error(f"BitTorrent executable not found at: {exe_path}")
        return

    # Using quotes around the path to handle spaces gracefully
    command_to_run = f'explorer.exe "{exe_path}"'
    
    ensure_command_executed(cmd=command_to_run)