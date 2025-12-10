import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure the project root is in sys.path for internal imports
# This module itself needs to be importable, so it should handle its own path
# if it's potentially an entry point or directly run.
# However, for a utility class, it's expected that the caller has set up sys.path.
# We will rely on af_directory_paths to handle this if it's imported first in an entry script.

# Import D_PROJECT_ROOT_PATH after ensuring it's available via sys.path
# We need to make sure af_directory_paths.py runs its path setup logic first.
# To do this, we explicitly import it here.
from af_internal_tools.constants.af_directory_paths import D_PROJECT_ROOT_PATH

# Configure logging for this module
logger = logging.getLogger(__name__)

class PkTester:
    """
    A utility class for managing test-specific environment variables.
    It loads variables from a `.env_test` file located in the project root.
    """

    @staticmethod
    def load_test_env(project_root: Path = None):
        """
        Loads environment variables from a .env_test file.
        Searches for .env_test in the provided project_root or D_PROJECT_ROOT_PATH.
        """
        if project_root is None:
            project_root = D_PROJECT_ROOT_PATH

        env_test_path = None
        # Search for .env_test in project_root and its parent directory
        possible_env_paths = [
            project_root / ".env_test",
            project_root.parent / ".env_test"
        ]
        
        for p in possible_env_paths:
            if p.is_file():
                env_test_path = p
                break
        
        if env_test_path:
            logger.info(f"Loading test environment variables from: {env_test_path}")
            load_dotenv(dotenv_path=env_test_path, override=True)
            logger.info("Test environment variables loaded successfully.")
            
            # Log loaded variables for debugging (mask sensitive info)
            for key in ["TEST_LOGIN_URL", "TEST_USER_ID", "TEST_PASSWORD"]:
                if key in os.environ:
                    value = os.environ[key]
                    if "PASSWORD" in key:
                        logger.debug(f"  {key}: {'*' * len(value)}")
                    else:
                        logger.debug(f"  {key}: {value}")
        else:
            logger.warning(f"'.env_test' file not found at {env_test_path}. No test environment variables loaded.")

# Example usage (for testing this module directly)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Testing PkTester.load_test_env()")
    
    # Create a dummy .env_test file for demonstration
    dummy_env_path = D_PROJECT_ROOT_PATH / ".env_test"
    with open(dummy_env_path, "w") as f:
        f.write("TEST_LOGIN_URL=http://test.example.com\n")
        f.write("TEST_USER_ID=testuser\n")
        f.write("TEST_PASSWORD=testpass123\n")
        f.write("ANOTHER_VAR=somevalue\n")
    logger.info(f"Created dummy .env_test at {dummy_env_path}")

    PkTester.load_test_env()

    logger.info(f"TEST_LOGIN_URL: {os.getenv('TEST_LOGIN_URL')}")
    logger.info(f"TEST_USER_ID: {os.getenv('TEST_USER_ID')}")
    logger.info(f"TEST_PASSWORD: {os.getenv('TEST_PASSWORD')}") # Should be masked if log level is DEBUG
    logger.info(f"ANOTHER_VAR: {os.getenv('ANOTHER_VAR')}")

    # Clean up dummy file
    os.remove(dummy_env_path)
    logger.info(f"Cleaned up dummy .env_test at {dummy_env_path}")
