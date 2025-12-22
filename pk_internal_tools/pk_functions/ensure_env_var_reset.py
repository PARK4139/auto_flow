import logging
from dotenv import unset_key

from pk_internal_tools.pk_functions.ensure_pk_env_file_setup import ensure_pk_env_file_setup
from pk_internal_tools.pk_functions.get_pk_env_var_id import get_pk_env_var_id

def ensure_env_var_reset(key_name: str, func_n) -> bool:
    """
    Removes a specific environment variable from the .env file.
    The actual environment variable name is derived from key_name and func_n.
    """
    env_path = ensure_pk_env_file_setup()
    
    key_name = key_name.upper() # Ensure consistency with how it's saved
    env_var_id = get_pk_env_var_id(key_name, func_n)

    try:
        # unset_key returns True if the key was found and removed, False otherwise
        success = unset_key(env_path, env_var_id)
        if success:
            logging.info(f"Environment variable '{env_var_id}' successfully removed from {env_path}")
            # Also remove from current process environment if it exists
            import os
            if env_var_id in os.environ:
                del os.environ[env_var_id]
                logging.info(f"Environment variable '{env_var_id}' also removed from current process environment.")
        else:
            logging.warning(f"Environment variable '{env_var_id}' not found in {env_path}. No action taken.")
        return success
    except Exception as e:
        logging.error(f"Failed to remove environment variable '{env_var_id}' from {env_path}: {e}")
        return False
