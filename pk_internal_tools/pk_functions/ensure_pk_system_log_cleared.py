from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_system_log_cleared():
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG
    from pk_internal_tools.pk_functions.ensure_target_file_cleared import ensure_target_file_cleared

    logging_file = F_PK_LOG

    # 중복 초기화 방지를 위한 플래그 체크
    # if hasattr(ensure_pk_system_log_initialized, '_initialized'):
    #     return
    # ensure_pk_system_log_initialized._initialized = True

    ensure_target_file_cleared(logging_file)
