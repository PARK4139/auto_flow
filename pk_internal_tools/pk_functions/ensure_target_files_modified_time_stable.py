def ensure_target_files_modified_time_stable(files_to_monitor, monitoring_seconds, monitoring_interval_seconds=0.2):
    import traceback

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    try:
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        import time
        from pk_internal_tools.pk_functions.get_nx import get_nx

        import logging
        from pathlib import Path

        files_to_monitor = [Path(f) for f in files_to_monitor]

        from pathlib import Path

        def get_mtime_map(files_to_monitor):
            """
            주어진 파일 리스트의 최종 수정 시간을 맵 형태로 반환합니다.
            """
            mtime_map = {}
            for f in files_to_monitor:
                f_path = Path(f)
                f_clean = str(f_path.resolve())
                mtime_map[f_clean] = f_path.stat().st_mtime
            return mtime_map

        logging.debug(f"detect started for {monitoring_seconds} seconds")
        file_nxs = [get_nx(f) for f in files_to_monitor]
        logging.debug(f"len(file_nxs)={len(file_nxs)}")
        for file_nx in file_nxs:
            logging.debug(f"file_nx={file_nx}")

        baseline = get_mtime_map(files_to_monitor)

        pk_seconds_limit = monitoring_seconds
        pk_time_s = time.time()

        while True:
            current = get_mtime_map(files_to_monitor)
            for f in files_to_monitor:
                f = str(f)
                # logging.debug(f"f={f}")
                # logging.debug(f"current[f]={current[f]}")
                # logging.debug(f"baseline[f]={baseline[f]}")
                if f in baseline and f in current and baseline[f] != current[f]:
                    logging.debug(f"files_to_monitor is not stable")
                    return False

            elapsed = time.time() - pk_time_s
            if elapsed >= pk_seconds_limit:
                # logging.debug(f'''time is limited (pk_time_limit={pk_seconds_limit}) ''')
                logging.debug(f"files_to_monitor is stable (for {elapsed})")
                return True

            # ensure_slept(milliseconds = 80)
            time.sleep(00)  # 로깅 방지
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return None
