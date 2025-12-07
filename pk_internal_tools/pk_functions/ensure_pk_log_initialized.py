from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
# @ensure_pk_ttl_cached(ttl_seconds=10 * 1 * 1, maxsize=128)
# @lru_cache(maxsize=1)
def ensure_pk_log_initialized(__file__, with_file_logging_mode=True):
    import logging

    from pk_internal_tools.pk_objects.pk_colorful_logging_formatter import PkColorfulLoggingFormatter
    from pk_internal_tools.pk_objects.pk_files import F_PK_TEMP_LOG
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_functions.ansi_stripping_formatter import AnsiStrippingFormatter  # Import the new formatter
    from pk_internal_tools.pk_functions.cleanup_old_log_files import cleanup_old_log_files
    from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
    from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG

    if hasattr(ensure_pk_log_initialized, '_initialized'):
        return
    ensure_pk_log_initialized._initialized = True

    # pk_option: 콘솔 로깅 활성화/비활성화 (하드코딩 옵션)
    ENABLE_CONSOLE_LOGGING = True
    # ENABLE_CONSOLE_LOGGING = False

    logging_file = None
    if with_file_logging_mode:
        logging_file = F_PK_LOG
    else:
        logging_file = F_PK_TEMP_LOG


    # pk_system language setting (lazy initialization)
    from pk_internal_tools.pk_functions.ensure_pk_language_initialized import ensure_pk_language_initialized
    ensure_pk_language_initialized()

    d_pk_logs.mkdir(parents=True, exist_ok=True)

    # pk_option : 하루 이상 지난 로그 파일 삭제
    if not QC_MODE:
        cleanup_old_log_files(d_pk_logs)

    if QC_MODE:
        ensure_console_cleared()

    # 컬러풀 로깅 포맷터 import
    try:
        colorful_formatter = PkColorfulLoggingFormatter(use_pkmessage=True)
    except ImportError:
        # fallback: 기본 포맷터 사용
        log_format = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(message)s]"
        colorful_formatter = logging.Formatter(log_format)

    # QC_MODE 모드에서는 새 파일로, 일반 모드에서는 append 모드로
    file_mode = "w" if QC_MODE else "a"

    # 파일 핸들러 (ANSI 코드 제거 포맷)
    file_handler = logging.FileHandler(logging_file, encoding="utf-8", mode=file_mode)
    file_format = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(message)s]"
    file_handler.setFormatter(AnsiStrippingFormatter(file_format))  # Use AnsiStrippingFormatter

    # 콘솔 핸들러 (컬러풀 포맷)
    if ENABLE_CONSOLE_LOGGING:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(colorful_formatter)
        console_handler.setLevel(logging.DEBUG)

    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 기존 핸들러 제거 후 새 핸들러 추가
    logger.handlers.clear()
    logger.addHandler(file_handler)
    if ENABLE_CONSOLE_LOGGING:
        logger.addHandler(console_handler)
        console_handler.flush()

    # 로깅 시스템 상태 확인 (디버깅용)
    logging.debug(PK_UNDERLINE)
    logging.debug(f"루트 로거 레벨: {logging.getLevelName(logger.level)}")
    logging.debug(f"루트 로거 핸들러 수: {len(logger.handlers)}")
    for i, handler in enumerate(logger.handlers):
        logging.debug(f"핸들러 {i}:")
        logging.debug(f"타입: {type(handler)}")
        logging.debug(f"레벨: {logging.getLevelName(handler.level)}")
        if hasattr(handler, 'formatter') and handler.formatter:
            logging.debug(f"포맷터: {type(handler.formatter)}")
        else:
            logging.debug(f"포맷터: 없음")
    logging.debug(PK_UNDERLINE)

    # yt-dlp 로그 레벨 조정
    # logging.getLogger('yt_dlp').setLevel(logging.WARNING)
    # logging.getLogger('urllib3').setLevel(logging.WARNING)

    # 로그 시작 메시지
    # print(f"pk_system log is saved at {logging_file}")
    logging.debug(f"pk_system logging started at {logging_file}")
