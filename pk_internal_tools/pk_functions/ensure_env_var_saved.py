import logging
import traceback
from pathlib import Path
from dotenv import set_key, find_dotenv

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def ensure_env_var_saved(key_name: str, value: str, env_path: Path = None) -> bool:
    """
    Saves or updates an environment variable in a .env file, forcing the save even if the key already exists.

    Args:
        key_name (str): The name (key) of the environment variable.
        value (str): The value to save for the environment variable.
        env_path (Path, optional): The full path to the .env file. If not provided,
                                   it searches for the .env file in the current directory
                                   and its parents. Defaults to None.

    Returns:
        bool: True if the variable was successfully saved, False otherwise.
    """
    logging.info(f"Attempting to save environment variable '{key_name}' with value '{value}'.")
    
    try:
        # If env_path is not specified, find_dotenv will search for it.
        # If it's specified, we use that path directly.
        if env_path:
            dotenv_path = str(env_path)
            if not env_path.exists():
                logging.warning(f"Specified .env file does not exist, but will be created: {env_path}")
                # set_key will create the file if it doesn't exist.
        else:
            # find_dotenv() can return an empty string if it doesn't find a .env file.
            # In that case, set_key will create a '.env' in the current working directory.
            dotenv_path = find_dotenv()
            if not dotenv_path:
                logging.info("No .env file found. A new '.env' file will be created in the current directory.")
                # We can explicitly set it to be '.env' in the current directory
                dotenv_path = Path.cwd() / ".env"

        # set_key handles both adding a new key and updating an existing one.
        # The function returns a tuple (True/False for success, key, value)
        success, key, saved_value = set_key(str(dotenv_path), key_name, value, quote_mode="always")

        if success:
            logging.info(f"Successfully saved '{key}={saved_value}' to {dotenv_path}.")
            return True
        else:
            # This part of the code might be less likely to be reached as set_key often raises an exception on failure
            # rather than returning False, but we keep it for robustness.
            logging.error(f"Failed to save environment variable '{key_name}' to {dotenv_path} for an unknown reason.")
            return False

    except Exception as e:
        logging.error(f"An error occurred while saving '{key_name}' to the .env file: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False

