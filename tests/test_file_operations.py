import pytest
import shutil
from pathlib import Path
import sys

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[1]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)


from pk_internal_tools.pk_functions.ensure_target_filenames_and_file_content_texts_replaced import ensure_target_filenames_and_file_content_texts_replaced
from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForPnxReplacement

# Assuming D_PROJECT_ROOT_PATH and D_FUNCTIONS_PATH are correctly imported/defined in the main script
# For testing, we will mock or provide a controlled environment.

@pytest.fixture
def temp_test_environment(tmp_path):
    """
    Creates a temporary directory structure for testing file operations.
    """
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    # Create a test file with content and a name containing old_text
    (test_dir / "test_ensure_wrapper_started_file.py").write_text("def ensure_wrapper_started(): pass")
    (test_dir / "another_file.txt").write_text("This file also has ensure_wrapper_started in its content.")
    
    # Create a subdirectory to test recursive behavior
    (test_dir / "sub_dir").mkdir()
    (test_dir / "sub_dir" / "nested_ensure_wrapper_started.py").write_text("import ensure_wrapper_started")

    yield test_dir
    # Teardown - pytest's tmp_path fixture handles cleanup


def test_filename_and_content_replacement(temp_test_environment):
    """
    Tests if ensure_target_filenames_and_file_content_texts_replaced correctly
    renames files and replaces content.
    """
    d_target = temp_test_environment
    old_text = 'ensure_wrapper_started'
    new_text = 'ensure_custom_cli_started'
    target_extensions = [".py", ".txt"]
    ignored_directory_names = [] # No ignored directories for this test

    # Run the replacement script
    ensure_target_filenames_and_file_content_texts_replaced(
        d_target=d_target,
        old_text=old_text,
        new_text=new_text,
        target_extensions=target_extensions,
        ignored_directory_names=ignored_directory_names,
        operation_mode=SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY
    )

    # Verify changes
    # Check renamed file
    assert not (d_target / "test_ensure_wrapper_started_file.py").exists()
    assert (d_target / "test_ensure_custom_cli_started_file.py").exists()
    assert not (d_target / "sub_dir" / "nested_ensure_wrapper_started.py").exists()
    assert (d_target / "sub_dir" / "nested_ensure_custom_cli_started.py").exists()

    # Check content of renamed file
    assert "ensure_custom_cli_started" in (d_target / "test_ensure_custom_cli_started_file.py").read_text()
    assert "ensure_wrapper_started" not in (d_target / "test_ensure_custom_cli_started_file.py").read_text()

    # Check content of another_file.txt (only content replaced, not name)
    assert "ensure_custom_cli_started" in (d_target / "another_file.txt").read_text()
    assert "ensure_wrapper_started" not in (d_target / "another_file.txt").read_text()

    # Check content of nested file
    assert "ensure_custom_cli_started" in (d_target / "sub_dir" / "nested_ensure_custom_cli_started.py").read_text()
    assert "ensure_wrapper_started" not in (d_target / "sub_dir" / "nested_ensure_custom_cli_started.py").read_text()

