from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_target_file_system_scanned():
    """
        TODO: Write docstring for ensure_target_file_system_scanned.
    """
    try:

        import os
        import logging
        from datetime import datetime

        from pk_internal_tools.pk_functions.get_drives_connected import get_drives_connected
        from pk_internal_tools.pk_functions._pk_target_db_utils import backup_existing_dbs, get_db_path, get_windows_os_system_path_sql_like_patterns, handle_walk_error, init_db
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
        from pk_internal_tools.pk_functions.get_sqlite3_connection import get_sqlite3_connection

        db_paths = {tt: get_db_path(tt) for tt in ["파일", "디렉토리", "모두"]}
        backup_existing_dbs(db_paths)
        for db_path in db_paths.values(): init_db(db_path)
        scan_roots = get_drives_connected()
        logging.info(f"전체 스캔을 시작합니다. 대상 드라이브: {scan_roots}")
        files_to_insert, dirs_to_insert = [], []
        scan_time = datetime.now().timestamp()
        for scan_root in scan_roots:
            logging.info(f"드라이브 스캔 중: {scan_root}")
            walk_path = f"\\\\?\\{scan_root}" if os.name == 'nt' else scan_root
            try:
                for root, dirs, files in os.walk(walk_path, onerror=handle_walk_error):
                    system_filters = get_windows_os_system_path_sql_like_patterns()
                    excluded_dir_names = [f.replace('%', '').lower() for f in system_filters]
                    dirs[:] = [d for d in dirs if d.lower() not in excluded_dir_names]
                    for d in dirs:
                        dirs_to_insert.append((os.path.join(root, d), "directory", scan_time))
                    for f in files:
                        files_to_insert.append((os.path.join(root, f), "file", scan_time))
            except Exception as e:
                logging.error(f"드라이브 스캔 중 예외 발생: {scan_root} - {e}")

        logging.info(f"총 {len(files_to_insert)}개의 파일과 {len(dirs_to_insert)}개의 디렉토리를 찾았습니다. DB에 저장합니다...")
        with get_sqlite3_connection(db_paths["파일"]) as conn:
            conn.execute("DELETE FROM targets")
            conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert)
            conn.commit()
        with get_sqlite3_connection(db_paths["디렉토리"]) as conn:
            conn.execute("DELETE FROM targets")
            conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", dirs_to_insert)
            conn.commit()
        with get_sqlite3_connection(db_paths["모두"]) as conn:
            conn.execute("DELETE FROM targets")
            conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert + dirs_to_insert)
            conn.commit()
        logging.info("전체 스캔 및 DB 저장이 완료되었습니다.")
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
