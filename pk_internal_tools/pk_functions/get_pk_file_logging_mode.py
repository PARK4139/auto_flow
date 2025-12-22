# @ensure_seconds_measured
def get_pk_file_logging_mode():
    """
        TODO: Write docstring for get_pk_file_logging_mode.
    """
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_modes import PkModesForPkLogging as PkModes
    try:
        func_n = get_caller_name()
        pk_logging_modes = [
            PkModes.MODE_WITH_FILE_LOGGING.value,
            PkModes.MODE_WITHOUT_FILE_LOGGING.value,
        ]
        if QC_MODE:
            pk_logging_mode = ensure_value_completed(
                key_name="pk_logging_mode",
                func_n=func_n,
                options=pk_logging_modes,
            )
        else:
            pk_logging_mode = PkModes.MODE_WITH_FILE_LOGGING.value
        return pk_logging_mode
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
