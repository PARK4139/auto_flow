import os
import sys
import stat
from pathlib import Path
import pytest
import sysconfig

def get_pk_system_path():
    """Helper function to find the path to the installed 'pk_system' library."""
    # Ensure the venv's site-packages is searched
    purelib = Path(sysconfig.get_path('purelib'))
    pk_system_path = purelib / "pk_system"
    if not pk_system_path.is_dir():
        # Fallback for some configurations
        for path in sys.path:
            if "site-packages" in path and Path(path, "pk_system").is_dir():
                pk_system_path = Path(path, "pk_system")
                return pk_system_path
        pytest.fail(f"'pk_system' directory not found in standard Python paths.")
    return pk_system_path

@pytest.mark.order(2)
def test_pk_system_files_are_readonly():
    """
    Verifies that files within the installed 'pk_system' package are read-only.
    This check is crucial to prevent accidental modification of the core library.
    """
    print("\n--- Verifying 'pk_system' file permissions ---")
    pk_system_path = get_pk_system_path()
    
    # Find a sample .py file to check. We don't need to check all 1900+ files.
    # A single file check is sufficient to confirm the 'attrib' or 'chmod' command ran.
    sample_file = next(pk_system_path.glob("**/*.py"), None)
    
    assert sample_file is not None, f"No Python files found in {pk_system_path} to test permissions."

    # os.access(path, os.W_OK) checks if the file is writable.
    # We assert that it is NOT writable.
    is_writable = os.access(sample_file, os.W_OK)
    
    assert not is_writable, f"Verification failed: File '{sample_file}' should be read-only, but it is writable."

    print(f"✅ Verification successful: Sample file '{sample_file.name}' is read-only as expected.")

