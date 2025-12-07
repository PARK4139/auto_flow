from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def backup_workspace(D_PKG_ARCHIVED, d_working, func_n):
    import traceback
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    import logging
    import logging
    import logging
    import os
    import tarfile
    from datetime import datetime
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    try:
        # 0. 경로 정규화
        from pathlib import Path
        d_working = Path(d_working).resolve()
        D_PKG_ARCHIVED = Path(D_PKG_ARCHIVED).resolve()

        # 대상 폴더 크기 계산
        def get_dir_size(path):
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.isfile(fp):
                        total += os.path.getsize(fp)
            return total

        target_size_mb = get_dir_size(d_working) / (1024 * 1024)
        if target_size_mb > 100:
            logging.debug(f"[ALERT] 백업 대상 폴더({d_working})의 크기가 100MB를 초과했습니다: {target_size_mb:.2f} MB"
                          )
            answer = input("continue:y/n").strip().lower()
            if answer not in ("y", "yes"):
                logging.debug("백업을 중단합니다.")
                return None

        logging.debug(f'''d_working={d_working} ''')
        logging.debug(f'''D_PKG_ARCHIVED={D_PKG_ARCHIVED} ''')
        os.makedirs(D_PKG_ARCHIVED, exist_ok=True)
        timestamp = datetime.now().strftime('%Y_%m%d_%H%M_%S')
        base_name = os.path.basename(d_working)
        archive_name = f"{base_name}_archived_before_work_{timestamp}_via_{func_n}.tar.bz2"
        archive_path = os.path.join(D_PKG_ARCHIVED, archive_name)
        with tarfile.open(archive_path, "w:bz2") as tar:
            tar.add(d_working, arcname=base_name)
        logging.debug(f"[{PkTexts.BACKUP_DONE}] {archive_path}\n")
        return archive_path
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
