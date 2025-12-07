import logging
import os
import os.path
import re
import traceback

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.backup_workspace import backup_workspace
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.get_file_id import get_file_id
from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
from pk_internal_tools.pk_functions.restore_workspace_from_latest_archive import restore_workspace_from_latest_archive
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_PK_FUNCTIONS, D_PKG_ARCHIVED
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools


def replace_in_file(file_path, old_text, new_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_text not in content:
        logging.info(f"[{PkTexts.SKIPPED}] {file_path} (No target string found)")
        return False
    new_content = content.replace(old_text, new_text)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    logging.info(f"[{PkTexts.INSERTED}] Replaced '{old_text}' with '{new_text}' in: {file_path}")
    return True


def walk_and_replace(target_dir, old_text, new_text, exts=None):
    changed_files = []
    for root, _, files in os.walk(target_dir):
        for fname in files:
            if exts and not any(fname.endswith(ext) for ext in exts):
                continue
            file_path = os.path.join(root, fname)
            try:
                if replace_in_file(file_path, old_text, new_text):
                    changed_files.append(file_path)
            except Exception as e:
                logging.error(f"{file_path} - {e}")
    logging.info(f"Total files changed: {len(changed_files)}")


def walk_and_regex_replace(target_dir, pattern, repl, exts=None, dry_run=True):
    changed_files = []
    # n. 대상 파일 전체 목록 수집
    all_files = []
    for root, _, files in os.walk(target_dir):
        for fname in files:
            if exts and not any(fname.endswith(ext) for ext in exts):
                continue
            file_path = os.path.join(root, fname)
            all_files.append(file_path)
    total_files = len(all_files)

    # n. 진행률과 함께 파일 처리
    for idx, file_path in enumerate(all_files, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if not re.search(pattern, content):
                # logging.info(f"[{idx}/{total_files}] [{mkr..}] [{PkTexts.SKIPPED}] {file_path} (Pattern not found)")
                continue
            new_content = re.sub(pattern, repl, content)
            if dry_run:
                if content != new_content:
                    logging.info(f"[{idx}/{total_files}] [{PkTexts.DRY_RUN}] Would replace pattern '{pattern}' with '{repl}' in: {file_path}")
                    changed_files.append(file_path)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logging.info(f"[{idx}/{total_files}] [{PkTexts.INSERTED}] Replaced pattern '{pattern}' with '{repl}' in: {file_path}")
                changed_files.append(file_path)
        except Exception as e:
            logging.error(f"[{idx}/{total_files}] [ERROR] {file_path} - {e}")
    logging.info(f"{len(changed_files)}/{total_files} files {'to be changed' if dry_run else 'changed'}")
    return changed_files


if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done

    ensure_pk_log_initialized(__file__=__file__)
    try:
        while True:
            func_n = get_caller_name()

            key_name = "d_working"
            d_working = get_values_from_historical_file_routine(
                file_id=get_file_id(key_name, func_n),
                key_hint=f'{key_name}=',
                options=[D_PK_FUNCTIONS, d_pk_external_tools]
            )[0]

            key_name = "old_text"
            old_text = get_values_from_historical_file_routine(
                file_id=get_file_id(key_name, func_n),
                key_hint=f'{key_name}=',
                options=["old_text"]
            )[0]

            key_name = "new_text"
            new_text = get_values_from_historical_file_routine(
                file_id=get_file_id(key_name, func_n),
                key_hint=f'{key_name}=',
                options=["new_text"]
            )[0]

            key_name = "exts"
            exts = get_values_from_historical_file_routine(
                file_id=get_file_id(key_name, func_n),
                key_hint=f'{key_name}= (예: .py,.txt)',
                options=[".py", ".txt"],
            )[0]

            if not os.path.isdir(d_working):
                logging.info(f"[{PkTexts.PATH_NOT_FOUND}] {d_working}")
                break

            python_filenames = [f for f in os.listdir(d_working) if f.endswith('.py')]
            python_files = [os.path.join(d_working, f) for f in python_filenames]
            if not python_files:
                logging.info(f"[{PkTexts.LISTED}] No .py files found.")
                break

            exec_mode = ensure_value_completed_2025_10_12_0000(
                key_name=f"{PkTexts.MODE}=",
                options=[PkTexts.DRY_RUN, PkTexts.EXECUTION]
            ).strip()

            dry_run = None
            if exec_mode == PkTexts.DRY_RUN:
                dry_run = True
                logging.info(f"[{PkTexts.MODE}] {f'{PkTexts.DRY_RUN}' if dry_run else PkTexts.EXECUTION}")
            elif exec_mode == PkTexts.EXECUTION:
                dry_run = False
                logging.info(f"[{PkTexts.MODE}] {f'{PkTexts.DRY_RUN}' if dry_run else PkTexts.EXECUTION}")

            if exec_mode == PkTexts.DRY_RUN:
                walk_and_regex_replace(d_working, old_text, new_text, exts=exts, dry_run=dry_run)
            elif exec_mode == PkTexts.EXECUTION:

                # n. backup
                logging.info(f"[{PkTexts.STARTED}] {PkTexts.BACKUP}")
                archive_path = backup_workspace(D_PKG_ARCHIVED, d_working, func_n)
                logging.info(f"[{PkTexts.FINISHED}] {PkTexts.BACKUP}")

                # n. work
                walk_and_regex_replace(d_working, old_text, new_text, exts=exts, dry_run=dry_run)

                # n. after service
                decision = ensure_value_completed_2025_10_12_0000(
                    key_name=f"{PkTexts.AFTER_SERVICE}=",
                    options=[rf"{PkTexts.ORIGIN} {PkTexts.DELETE}", PkTexts.REVERT],
                )
                if decision == rf"{PkTexts.ORIGIN} {PkTexts.DELETE}":
                    for path in python_files:
                        try:
                            os.remove(path)  # TODO   move to 휴지통    as  origiin   or tar.bz2
                            logging.info(f"[{PkTexts.REMOVED}] {os.path.basename(path)}")
                        except Exception as e:
                            logging.info(f"[{PkTexts.ERROR}] Failed to remove {path}: {e}")
                else:
                    try:
                        logging.info(f"[{PkTexts.STARTED}] {PkTexts.REVERTED}")
                        restore_workspace_from_latest_archive(D_PKG_ARCHIVED, d_working)
                        logging.info(f"[{PkTexts.DONE}] {PkTexts.REVERTED}")
                    except Exception as e:
                        logging.error(f"[{PkTexts.ERROR}] {PkTexts.AUTO} {PkTexts.REVERTED}")
                        logging.error(f"[{PkTexts.RETRY}] {PkTexts.AUTO} {PkTexts.REVERTED}")
                        if archive_path:
                            restore_workspace_from_latest_archive(D_PKG_ARCHIVED, d_working)
                            logging.info(f"[{PkTexts.DONE}] {PkTexts.AUTO} {PkTexts.REVERTED}")
                        raise
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
