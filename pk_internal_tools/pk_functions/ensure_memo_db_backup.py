def ensure_memo_db_backup():
    from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    import time
    from pathlib import Path

    try:
        db_dir = d_pk_root_hidden
        from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
        main_db_path = F_PK_MEMO_SQLITE

        if not main_db_path.exists():
            logging.debug("메모 DB 파일이 존재하지 않습니다.")
            return False

        # 기존 백업 파일들 확인
        backup_files = list(db_dir.glob("pk_memo_*.sqlite"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        logging.debug("메모 DB 백업 상태:")

        if backup_files:
            logging.debug(f"백업 파일 수: {len(backup_files)}")

            # 최신 백업 파일 정보
            latest_backup = backup_files[0]
            backup_size = latest_backup.stat().st_size / (1024 * 1024)
            backup_time = time.ctime(latest_backup.stat().st_mtime)

            logging.debug(f"최신 백업: {latest_backup.nick_name}")
            logging.debug(f"백업 크기: {backup_size:.2f} MB")
            logging.debug(f"백업 시간: {backup_time}")

            # 백업 파일 유효성 검사
            try:
                test_conn = sqlite3.connect(str(latest_backup))
                test_cursor = test_conn.cursor()
                test_cursor.execute("SELECT COUNT(*) FROM pk_memos")
                memo_count = test_cursor.fetchone()[0]
                test_cursor.close()
                test_conn.close()

                logging.debug(f"백업 파일 유효성: 정상 (메모 {memo_count}개)")

            except Exception as e:
                logging.debug(f"백업 파일 유효성: 손상됨 ({str(e)})")

        else:
            logging.debug("  백업 파일이 없습니다.")

        # 백업 정책 확인
        logging.debug("  백업 정책:")
        logging.debug("   - 프로그램 시작 시 자동 백업")
        logging.debug("   - 백업 형식: pk_memo_YYYY_MM_DD_HHMMSS.sqlite")
        logging.debug("   - 백업 위치: .pk_system/")

        return True

    except Exception as e:
        logging.debug(f"메모 DB 백업 상태 확인 실패: {str(e)}")
        return False



