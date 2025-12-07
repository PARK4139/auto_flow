from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
# @ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10) # pk_option
def get_gemini_version_installed():
    import logging

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    output_list, error_list = ensure_command_executed("gemini --version")
    gemini_version = None
    for line in output_list:
        if isinstance(line, str) and len(line.split(".")) >= 2:
            logging.debug(f'gemini is installed')
            if not QC_MODE:
                ensure_spoken(f'gemini version {line} 설치 확인되었습니다.')
            logging.debug(f'gemini version {line} 설치 확인되었습니다.')
            gemini_version = line
    return gemini_version
