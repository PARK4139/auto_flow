from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_wrapper_executed(wrapper_file):
    try:
        from pk_internal_tools.pk_functions.ensure_pk_python_file_executed_in_uv_venv_windows import ensure_pk_python_file_executed_in_uv_venv_windows
        ensure_pk_python_file_executed_in_uv_venv_windows(python_file=wrapper_file)
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
