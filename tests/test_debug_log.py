import sys
import traceback
import logging
from pathlib import Path
import os
import pytest

# Ensure project root is on sys.path for local imports if any
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Now, imports from pk_system should work (pk_system is installed as a library)
from pk_system.pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_system.pk_internal_tools.pk_objects.pk_system_files import F_PK_SYSTEM_ERROR_ISOLATED_LOG

@pytest.mark.order(1)
def test_ensure_debug_loged_verbose_creates_and_writes_to_log():
    """
    Tests that ensure_debug_loged_verbose correctly captures a traceback
    and writes it to the designated log file.
    """
    # --- Setup ---
    # Ensure logging is initialized for the test context
    ensure_pk_system_log_initialized(__file__)
    
    log_file = Path(F_PK_SYSTEM_ERROR_ISOLATED_LOG)
    
    # Ensure the log file from previous runs is deleted
    if log_file.exists():
        log_file.unlink()
        
    error_message = "This is an intentional test error for logging."

    # --- Act ---
    try:
        # Simulate an error
        raise ValueError(error_message)
    except Exception:
        # Call the function to be tested
        ensure_debug_loged_verbose(traceback)
    
    # --- Assert ---
    # 1. Check if the log file was created
    assert log_file.exists(), f"Log file was not created at {log_file}"
    
    # 2. Check the content of the log file
    log_content = log_file.read_text(encoding='utf-8')
    
    assert "Traceback (most recent call last):" in log_content
    assert "ValueError" in log_content
    assert error_message in log_content
    
    # --- Teardown (optional, good practice) ---
    if log_file.exists():
        log_file.unlink()
