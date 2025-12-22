from pathlib import Path # Moved import
from typing import Optional # Added for Optional type hint

def get_f_contained_signature(signature: str, d_pnx: Path, expected_extension: str = None) -> Optional[Path]:
    import logging
    import os

    d_pnx_path = Path(d_pnx) # Convert d_pnx to Path object

    if not d_pnx_path.exists(): # Use Path.exists()
        logging.debug(f'''Directory does not exist: {d_pnx_path}  ''')
        return None
    else:
        logging.debug(f'''Searching for signature="{signature}" in directory: {d_pnx_path} (extension: {expected_extension}) ''')

    for file_name in os.listdir(d_pnx_path): # Use Path object for os.listdir
        if expected_extension and not file_name.lower().endswith(expected_extension.lower()):
            continue

        if signature in file_name:
            full_path = d_pnx_path / file_name # Use Path / operator
            logging.debug(f'''Found file: {full_path}  ''')
            return full_path # Return Path object
    else:
        logging.debug(f'''No file containing signature="{signature}" found in directory: {d_pnx_path} (extension: {expected_extension}) ''')
    return None
