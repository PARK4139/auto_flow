import logging
import traceback


def ensure_target_file_names_and_target_file_texts_replaced_advanced(d_target, old_text, new_text, target_extensions=None, ignored_directory_names=None, operation_mode=None):
    import os
    from pathlib import Path

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureTargetFilenameAndFileContentTextReplaced
    from pk_internal_tools.pk_functions.ensure_target_file_name_and_file_texts_replaced import ensure_target_file_name_and_file_texts_replaced

    if operation_mode is None:
        operation_mode = PkModesForEnsureTargetFilenameAndFileContentTextReplaced.FILENAME_AND_FILECONTENT

    if target_extensions is None:
        target_extensions = []
    if ignored_directory_names is None:
        ignored_directory_names = []

    d_target_path = Path(d_target).resolve()
    logging.debug(f'd_target={d_target_path} {"%%%FOO%%%" if QC_MODE else ""}')

    if not d_target_path.is_dir():
        logging.error(f" 디렉토리 없음: {d_target_path}")
        return

    dirs_to_rename = []

    # Step 1: Walk the directory tree from the bottom up, process files, and collect directory rename tasks.
    for root, dirs, files in os.walk(str(d_target_path), topdown=False):
        # Process files (rename and content replacement)
        for file_name in files:
            file_path_old = Path(root) / file_name

            if target_extensions and not any(str(file_path_old).lower().endswith(ext) for ext in target_extensions):
                continue

            if ignored_directory_names and any(ignored_dir in str(file_path_old) for ignored_dir in ignored_directory_names):
                # logging.debug()(f"[SKIP] Ignored directory name found in path: {file_path_old}")
                continue

            ensure_target_file_name_and_file_texts_replaced(f_target=str(file_path_old), old_text=old_text, new_text=new_text, operation_mode=operation_mode)

        # Collect directories to rename
        if operation_mode in [PkModesForEnsureTargetFilenameAndFileContentTextReplaced.ONLY_FILENAME, PkModesForEnsureTargetFilenameAndFileContentTextReplaced.FILENAME_AND_FILECONTENT]:
            for dir_name in dirs:
                dir_path_old = Path(root) / dir_name

                if ignored_directory_names and any(ignored_dir in str(dir_path_old) for ignored_dir in ignored_directory_names):
                    continue

                if old_text in dir_name:
                    new_dir_name = dir_name.replace(old_text, new_text)
                    dir_path_new = Path(root) / new_dir_name
                    dirs_to_rename.append((str(dir_path_old), str(dir_path_new)))

    # Step 2: Rename the collected directories after the walk is complete.
    # Sort by path length (depth) in descending order to rename deepest directories first.
    dirs_to_rename.sort(key=lambda x: len(x[0]), reverse=True)

    for dir_path_old, dir_path_new in dirs_to_rename:
        try:
            if os.path.isdir(dir_path_old):  # Check if source dir still exists
                os.rename(dir_path_old, dir_path_new)
                logging.debug(f"[RENAMED DIR] {dir_path_old} -> {dir_path_new}")
        except OSError as e:
            logging.error(f" 디렉토리 이름 변경 실패: {dir_path_old} -> {dir_path_new}")
            logging.debug(e)
            traceback.print_exc()
