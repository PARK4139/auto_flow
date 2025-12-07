from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_wrapper_executed(wrapper_file):
    try:
        from pk_internal_tools.pk_functions.ensure_pk_python_file_executed_in_uv_venv_windows import ensure_pk_python_file_executed_in_uv_venv_windows
        ensure_pk_python_file_executed_in_uv_venv_windows(python_file=wrapper_file)
        return True
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
