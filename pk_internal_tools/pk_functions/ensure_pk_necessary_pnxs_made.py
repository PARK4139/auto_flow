from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_pk_necessary_pnxs_made(necessaries):
    """
        TODO: Write docstring for ensure_pk_necessary_pnxs_made.
    """
    try:
        import platform
        from os import environ
        from pathlib import Path
        for necessary in necessaries:
            if not necessary.is_file():
                directory = necessary
                if not directory.exists():
                    directory.mkdir(parents=True, exist_ok=True)
            else:
                file = necessary
                if not file.exists():
                    file.touch()
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
