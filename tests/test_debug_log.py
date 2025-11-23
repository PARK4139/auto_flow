import sys
from pathlib import Path
import traceback
import logging

# Ensure project root is on sys.path for internal_setup
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import source.internal_setup

# Now, imports from pk_system should work (pk_system is installed as a library)
from pk_system_sources.pk_system_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system_sources.pk_system_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_system_sources.pk_system_objects.pk_system_files import F_PK_SYSTEM_ERROR_ISOLATED_LOG

def test_logging_error():
    """
    Intentionally raises an error to test the ensure_debug_loged_verbose function.
    """
    ensure_pk_system_log_initialized(__file__) # Initialize logging
    
    logging.info("Starting test for ensure_debug_loged_verbose...")
    
    try:
        # Simulate an error
        raise ValueError("This is an intentional test error for logging.")
    except Exception:
        logging.error("An error occurred, calling ensure_debug_loged_verbose.")
        ensure_debug_loged_verbose(traceback)
    
    logging.info(f"Test finished. Check log file: {F_PK_SYSTEM_ERROR_ISOLATED_LOG}")

if __name__ == "__main__":
    test_logging_error()
