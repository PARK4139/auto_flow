from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_reg_patterns import REGEX_PATTERNS_TO_IGNORE, FILENAME_PARTS_TO_IGNORE


@ensure_seconds_measured
def get_pk_file_name_pattern_options_with_stamp():
    """
        TODO: Write docstring for get_pk_file_name_pattern_options_with_stamp.
    """
    try:
        file_name_pattern_option = []
        for part in FILENAME_PARTS_TO_IGNORE:
            file_name_pattern_option.append(f"[PART] {part}")
        for regex in REGEX_PATTERNS_TO_IGNORE:
            file_name_pattern_option.append(f"[REGEX] {regex}")
        return file_name_pattern_option
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
