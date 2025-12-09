import logging # Added logging import
from pathlib import Path # Added Path import

def get_auto_flow_path():
    import traceback

    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    try:
        func_n = get_caller_name()
        auto_flow_path = ensure_env_var_completed(
            key_name="auto_flow_path",
            func_n=func_n,
        )

        if auto_flow_path is None:
            # If ensure_env_var_completed couldn't get a value, default to current project root
            # The project root is assumed to be the directory containing this script, 3 levels up from here.
            # get_auto_flow_path is in af_internal_tools/functions/
            # So, parent[2] would be the project root.
            current_script_path = Path(__file__).resolve()
            project_root_default = current_script_path.parents[2]
            auto_flow_path = str(project_root_default)
            logging.info(f"auto_flow_path environment variable not set. Defaulting to project root: {auto_flow_path}") # Log that we are using the default
            
        # Ensure the path is a Path object for consistency
        auto_flow_path = Path(auto_flow_path)

        return auto_flow_path
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return None
