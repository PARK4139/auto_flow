from typing import Dict


def import_pk_pakages_dynamic(package_name: str = "pk_internal_tools.pk_functions", recursive: bool = True) -> Dict:
    """
    Recursively discovers and imports all submodules within a given package, handling errors gracefully.

    This function walks through the package structure, attempting to import each module it finds.
    If a module fails to import for any reason (e.g., syntax errors, missing dependencies),
    it logs a warning and continues with the next module, ensuring that one problematic
    module does not halt the entire process.

    Args:
        package_name (str): The name of the root package to start the discovery from.
                            Defaults to "pk_internal_tools".
        recursive (bool): If True, walks through all sub-packages recursively. 
                          Note: `pkgutil.walk_packages` is inherently recursive, so this
                          flag is for conceptual clarity and future-proofing. Defaults to True.

    Returns:
        Dict: A dictionary where keys are the fully qualified module names and values are the
              corresponding imported module objects. Returns an empty dictionary if the
              base package cannot be imported.
    """
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    import importlib
    import logging
    import pkgutil
    import time

    if not recursive:
        logging.warning("`recursive=False` is not fully implemented as pkgutil.walk_packages is inherently recursive.")
        # Future implementation could limit the depth. For now, we proceed recursively.

    try:
        package = importlib.import_module(package_name)
        results = {package_name: package}
        logging.debug(f"Successfully imported base package: {package_name}")
    except ImportError as e:
        # ensure_debugged_verbose(traceback, e)
        traceback.print_exc()
        return {}
    except Exception as e:
        # ensure_debugged_verbose(traceback, e)
        traceback.print_exc()

    for _, name, _ in pkgutil.walk_packages(path=package.__path__, prefix=package.__name__ + "."):
        try:
            start_time = time.perf_counter()
            module = importlib.import_module(name)
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            results[name] = module
            logging.debug(f"Successfully imported module: {name} in {duration_ms:.2f}ms")
        except Exception as e:
            # ensure_debugged_verbose(traceback, e)
            traceback.print_exc()
    return results
