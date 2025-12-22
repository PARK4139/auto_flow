def ensure_pk_log_cleared():
    """
    시스템 로그 파일을 초기화합니다.
    콘솔에 출력된 로그와 파일의 내용을 비웁니다.
    F_PK_LOG 에 정의된 로그 파일의 내용을 비웁니다.
    """
    import logging
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG
    try:
        ensure_console_cleared()
        log_file_path = Path(F_PK_LOG)
        if log_file_path.exists():
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.truncate(0)
        else:
            logging.warning(f"로그 파일 '{log_file_path}'이(가) 존재하지 않아 초기화할 수 없습니다.")
        if QC_MODE:
            logging.info(f"디버깅관심영역 아이솔레이션을 위해서, pk system log를 초기화하였습니다.")
        else:
            logging.info(f"pk system log 초기화 완료.")
    except Exception as e:
        logging.error(f"로그 파일 초기화 중 오류 발생: {e}")
