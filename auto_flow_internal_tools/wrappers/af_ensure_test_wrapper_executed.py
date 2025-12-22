import sys
from pathlib import Path
import logging
import pytest # Using pytest.main() directly

# --- Path Setup ---
# This wrapper will be an entry point, so it needs to ensure sys.path is correct.
# We will use the robust path setup logic here, similar to pk_ensure_pk_wrapper_starter_executed.py
try:
    current_path = Path(__file__).resolve().parent
    project_root = None
    for parent in [current_path] + list(current_path.parents):
        if (parent / 'pyproject.toml').exists() or (parent / '.git').exists():
            project_root = parent
            break

    if project_root:
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
    else:
        raise FileNotFoundError("Could not find project root.")
except Exception as e:
    print(f"Critical error during path setup: {e}", file=sys.stderr)
    sys.exit(1)

# --- After path setup, import project modules ---
from auto_flow_internal_tools.constants.af_directory_paths import D_PROJECT_ROOT_PATH
from pk_internal_tools.pk_objects.pk_tester import PkTester # For loading test env vars

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def af_ensure_test_wrapper_executed(test_path: str = None):
    """
    A wrapper to execute pytest tests.
    Loads test environment variables and runs specified test files or directories.

    Args:
        test_path (str, optional): The path to a specific test file or directory
                                   relative to the project root (e.g., "tests/test_my_feature.py").
                                   If None, runs all tests in the "tests/" directory.
    """
    logger.info("AF Test Wrapper: Starting test execution.")
    
    # Load test environment variables
    PkTester.load_test_env()

    args = []
    if test_path:
        full_test_path = D_PROJECT_ROOT_PATH / test_path
        if not full_test_path.exists():
            logger.error(f"Specified test path does not exist: {full_test_path}")
            sys.exit(1)
        args.append(str(full_test_path))
    else:
        # Default to running all tests in the tests/ directory
        args.append(str(D_PROJECT_ROOT_PATH / "tests"))

    # Add pytest common arguments
    args.extend(['-v', '-s', '--color=yes']) # -v for verbose, -s to show stdout, --color for colored output

    logger.info(f"Executing pytest with arguments: {' '.join(args)}")
    
    # Run pytest programmatically
    # pytest.main returns an ExitCode object or integer.
    # 0 means all tests passed. Non-zero indicates failure or error.
    exit_code = pytest.main(args)

    if exit_code != 0:
        logger.error(f"AF Test Wrapper: Test execution failed with exit code {exit_code}.")
        sys.exit(exit_code)
    else:
        logger.info("AF Test Wrapper: All tests passed successfully.")

if __name__ == "__main__":
    # Example usage when run directly
    # Can accept an argument for the test path
    # Example: python af_ensure_test_wrapper_executed.py tests/test_ekiss_flow.py
    
    import argparse
    parser = argparse.ArgumentParser(description="AF Test Wrapper to execute pytest tests.")
    parser.add_argument(
        "test_path",
        nargs="?", # 0 or 1 argument
        default=None,
        help="Path to a specific test file or directory (relative to project root)."
    )
    args = parser.parse_args()
    
    af_ensure_test_wrapper_executed(test_path=args.test_path)
