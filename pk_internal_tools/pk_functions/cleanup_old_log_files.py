from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def cleanup_old_log_files(log_directory, days_to_keep=1):
    """
    지정된 일수보다 오래된 로그 파일들을 삭제합니다.

    Args:
        log_directory (str | Path): 로그 파일들이 있는 디렉토리 경로
        days_to_keep (int): 보관할 일수 (기본값: 1일)
    """

    from pathlib import Path
    from pk_internal_tools.pk_functions.ensure_pnx_moved import ensure_pnx_moved
    from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    import time
    import logging

    # 함수 시작 로깅
    logging.debug(f"함수 시작 - log_directory: {log_directory}, days_to_keep: {days_to_keep}")

    try:
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)  # days_to_keep일 전 시간

        # 시간 계산 결과 로깅
        logging.debug(f"현재 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
        logging.debug(f"기준 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cutoff_time))}")
        logging.debug(f"보관 기간: {days_to_keep}일")

        log_dir = Path(log_directory)
        logging.debug(f"대상 디렉토리: {log_dir}")
        logging.debug(f"디렉토리 존재 여부: {log_dir.exists()}")

        if not log_dir.exists():
            error_msg = f"{PkTexts.LOG_CLEANUP_ERROR}: 대상 디렉토리가 존재하지 않습니다 - {log_dir}"
            logging.error(f"{error_msg}")
            logging.debug(error_msg)
            return

        # .log 파일들 찾기
        log_files = list(log_dir.glob("*.log"))
        logging.debug(f"발견된 .log 파일 수: {len(log_files)}")

        if log_files:
            logging.debug(f"발견된 파일 목록: {[f.name for f in log_files]}")

        deleted_count = 0
        kept_count = 0

        for log_file in log_files:
            try:
                logging.debug(f"파일 처리 중: {log_file.name}")

                # 파일의 수정 시간 확인
                file_modified_time = log_file.stat().st_mtime
                file_modified_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_modified_time))
                logging.debug(f"{log_file.name} 수정 시간: {file_modified_str}")

                # 파일 크기 정보도 로깅
                file_size = log_file.stat().st_size
                logging.debug(f"{log_file.name} 파일 크기: {file_size} bytes")

                if file_modified_time < cutoff_time:
                    logging.info(f"오래된 파일 발견: {log_file.name} (수정: {file_modified_str})")

                    # 휴지통으로 이동
                    ensure_pnx_moved(pnx=str(log_file), d_dst=D_PK_RECYCLE_BIN)
                    deleted_count += 1

                    success_msg = f"️ {PkTexts.OLD_LOG_FILE_DELETED}: {log_file.name}"
                    logging.info(f"{success_msg}")
                    logging.debug(success_msg)
                else:
                    kept_count += 1
                    logging.debug(f"보관 대상 파일: {log_file.name} (수정: {file_modified_str})")

            except OSError as e:
                error_msg = f"️ {PkTexts.LOG_FILE_DELETE_FAILED}: {log_file} - {e}"
                logging.error(f"{error_msg}")
                logging.debug(error_msg)

        # 최종 결과 로깅
        logging.debug(f"처리 완료 - 삭제: {deleted_count}, 보관: {kept_count}")

        if deleted_count > 0:
            result_msg = f" {PkTexts.LOG_CLEANUP_COMPLETE}: {deleted_count}{PkTexts.FILES_DELETED}, {kept_count}{PkTexts.FILES_KEPT}"
            logging.info(f"{result_msg}")
            logging.debug(result_msg)
        elif kept_count > 0:
            result_msg = f"ℹ️ {PkTexts.NO_OLD_FILES_TO_DELETE}, {kept_count}{PkTexts.FILES_KEPT}"
            logging.info(f"{result_msg}")
            logging.debug(result_msg)
        else:
            logging.info(f"처리할 .log 파일이 없습니다")

    except Exception as e:
        error_msg = f" {PkTexts.LOG_CLEANUP_ERROR}: {e}"
        logging.error(f"예외 발생: {error_msg}")
        logging.debug(error_msg)

    # 함수 종료 로깅
    logging.debug(f"함수 종료")
