from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_tree_copied_except_blacklist_and_including_whitelist(d_working: Path, dst_dir: Path, blacklist: list[Path], whitelist: list[Path]):  # Changed parameter name and type hint
    # blacklist, whitelist 모두 등록이 되면, 복사하지 않음. (blacklist 가 우선됨)
    import logging
    import os
    import shutil
    import traceback
    from pathlib import Path

    from pk_internal_tools.pk_functions.is_path_covered_by_list import is_path_covered_by_list
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    try:
        if whitelist is None:
            whitelist = []
        if blacklist is None:
            blacklist = []

        logging.debug(f"d_working={d_working}")
        logging.debug(f"dst_dir={dst_dir}")

        # pk_*
        logging.debug(f'len(blacklist)={len(blacklist)}')
        for idx, black_file in enumerate(blacklist):
            logging.debug(f'idx={idx} black_file={black_file}')

        logging.debug(f'len(whitelist)={len(whitelist)}')
        for idx, white_file in enumerate(whitelist):
            logging.debug(f'idx={idx} white_file={white_file}')

        # 경로 객체로 변환 (이미 Path 객체로 받도록 변경되었으므로 .resolve()만 호출)
        d_working = d_working.resolve()
        dst_dir = dst_dir.resolve()
        logging.debug(f"Resolved Paths: d_working={d_working}, dst_dir={dst_dir}")

        # 자기 자신 복사 방지
        if d_working == dst_dir or d_working in dst_dir.parents:
            logging.debug(f"잘못된 경로: 복사 대상이 원본과 같거나 하위 디렉토리입니다. d_working={d_working}, dst_dir={dst_dir})")
            return dst_dir

        # 기본적인 시스템 무시 디렉토리 (Path 객체로 변환)
        auto_exclude_dirs = {
            Path('.git'),
            Path('__pycache__'),
            Path('.venv'),
            Path('.venv'),
            Path('.venv'),
            Path('node_modules')
        }
        logging.debug(f"Auto exclude directories: {auto_exclude_dirs}")

        # black_list를 리터럴 경로와 glob 패턴으로 분리
        literal_excluded_paths = set()
        grouped_glob_patterns_blacklist = {}  # {base_path_resolved: [pattern_string, ...]}

        # auto_exclude_dirs는 항상 리터럴 경로로 처리
        # Ensure blacklist is always a list of Path objects
        if isinstance(blacklist, Path):
            all_initial_excluded_paths = [blacklist] + list(auto_exclude_dirs)
        else:
            all_initial_excluded_paths = (blacklist or []) + list(auto_exclude_dirs)

        for p in all_initial_excluded_paths:
            # Glob 패턴 포함 여부 확인 (Path.name 또는 Path.stem에 *나 ?가 있는지)
            if '*' in p.name or '?' in p.name or '*' in p.stem or '?' in p.stem:
                # Glob 패턴인 경우, 패턴 부분과 베이스 경로 분리
                pattern_string = p.name
                base_path_resolved = (d_working / p.parent).resolve()
                if base_path_resolved not in grouped_glob_patterns_blacklist:
                    grouped_glob_patterns_blacklist[base_path_resolved] = []
                grouped_glob_patterns_blacklist[base_path_resolved].append(pattern_string)
            else:
                # 리터럴 경로인 경우, 절대 경로로 변환하여 추가
                # Check if p is already an absolute path
                if p.is_absolute():
                    literal_excluded_paths.add(str(p.resolve()).casefold())
                else:
                    literal_excluded_paths.add(str((d_working / p).resolve()).casefold())

        logging.debug(f'len(literal_excluded_paths)={len(literal_excluded_paths)}')
        for idx, literal_excluded_path in enumerate(literal_excluded_paths):
            logging.debug(f'idx={idx} literal_excluded_path={literal_excluded_path}')

        logging.debug(f'len(grouped_glob_patterns_blacklist)={len(grouped_glob_patterns_blacklist)}')
        for idx, (base_path, patterns) in enumerate(grouped_glob_patterns_blacklist.items()):
            logging.debug(f'idx={idx} base_path={base_path} patterns={patterns}')

        # whitelist를 리터럴 경로와 glob 패턴으로 분리
        literal_whitelisted_paths = set()
        grouped_glob_patterns_whitelist = {}

        for p in (whitelist or []):
            if '*' in p.name or '?' in p.name or '*' in p.stem or '?' in p.stem:
                pattern_string = p.name
                base_path_resolved = (d_working / p.parent).resolve()
                if base_path_resolved not in grouped_glob_patterns_whitelist:
                    grouped_glob_patterns_whitelist[base_path_resolved] = []
                grouped_glob_patterns_whitelist[base_path_resolved].append(pattern_string)
            else:
                if p.is_absolute():
                    literal_whitelisted_paths.add(str(p.resolve()).casefold())
                else:
                    literal_whitelisted_paths.add(str((d_working / p).resolve()).casefold())

        logging.debug(f'len(literal_whitelisted_paths)={len(literal_whitelisted_paths)}')
        for idx, literal_whitelisted_path in enumerate(literal_whitelisted_paths):
            logging.debug(f'idx={idx} literal_whitelisted_path={literal_whitelisted_path}')

        logging.debug(f'len(grouped_glob_patterns_whitelist)={len(grouped_glob_patterns_whitelist)}')
        for idx, (base_path, patterns) in enumerate(grouped_glob_patterns_whitelist.items()):
            logging.debug(f'idx={idx} base_path={base_path} patterns={patterns}')

        if not dst_dir.exists():
            logging.debug(f"Destination directory does not exist, creating: {dst_dir}")
            dst_dir.mkdir(parents=True, exist_ok=True)

        copied_count = 0
        reserved_names = {'nul', 'con', 'prn', 'aux', 'lpt1', 'com1'}

        final_items_to_copy = []
        final_dirs_to_create = set()  # Use set to avoid duplicates, will convert to list later

        logging.debug(f"Traversing {d_working} for items to copy...")
        for root, dirs, files in os.walk(d_working):
            root_path = Path(root).resolve()

            # Check if the current root directory is blacklisted
            is_root_blacklisted = is_path_covered_by_list(root_path, literal_excluded_paths, grouped_glob_patterns_blacklist)
            if is_root_blacklisted:
                logging.debug(f"Skipping blacklisted directory and its contents: {root_path}")
                dirs[:] = []  # Don't recurse into this directory
                continue

            # Process files in the current directory
            for file_name in files:
                file_path = (root_path / file_name).resolve()
                is_blacklisted = is_path_covered_by_list(file_path, literal_excluded_paths, grouped_glob_patterns_blacklist)
                is_whitelisted = is_path_covered_by_list(file_path, literal_whitelisted_paths, grouped_glob_patterns_whitelist)

                # New logic: Only copy if whitelisted AND NOT blacklisted
                if is_whitelisted and not is_blacklisted:
                    final_items_to_copy.append(file_path)
                    logging.debug(f"APPROVED FILE (WHITELISTED & NOT BLACKLISTED): {file_path}")
                else:
                    logging.debug(f"REJECTED FILE (NOT WHITELISTED OR BLACKLISTED): {file_path}")

            # Process directories for creation (only if whitelisted AND NOT blacklisted)
            # We add directories to a set to ensure uniqueness and handle parent directories
            # The sorting by depth later will ensure correct creation order
            for dir_name in dirs:
                dir_path = (root_path / dir_name).resolve()
                is_blacklisted = is_path_covered_by_list(dir_path, literal_excluded_paths, grouped_glob_patterns_blacklist)
                is_whitelisted = is_path_covered_by_list(dir_path, literal_whitelisted_paths, grouped_glob_patterns_whitelist)

                # New logic: Only create if whitelisted AND NOT blacklisted
                if is_whitelisted and not is_blacklisted:
                    final_dirs_to_create.add(dir_path)
                    logging.debug(f"APPROVED DIR (WHITELISTED & NOT BLACKLISTED): {dir_path}")
                elif is_blacklisted:
                    logging.debug(f"REJECTED DIR (BLACKLISTED): {dir_path}")
                    dirs.remove(dir_name)  # Prevent os.walk from entering this blacklisted directory
                else:
                    logging.debug(f"REJECTED DIR (NOT WHITELISTED OR BLACKLISTED): {dir_path}")

        logging.debug(f"Traversing {d_working} for items to copy...")
        for root, dirs, files in os.walk(d_working):
            root_path = Path(root).resolve()

            # Check if the current root directory is blacklisted
            if is_path_covered_by_list(root_path, literal_excluded_paths, grouped_glob_patterns_blacklist):
                logging.debug(f"Skipping blacklisted directory and its contents: {root_path}")
                dirs[:] = []  # Don't recurse into this directory
                continue

            # Process files in the current directory
            for file_name in files:
                file_path = (root_path / file_name).resolve()
                is_blacklisted = is_path_covered_by_list(file_path, literal_excluded_paths, grouped_glob_patterns_blacklist)
                is_whitelisted = is_path_covered_by_list(file_path, literal_whitelisted_paths, grouped_glob_patterns_whitelist)

                if is_whitelisted:
                    final_items_to_copy.append(file_path)
                    logging.debug(f"APPROVED FILE (WHITELISTED): {file_path}")
                elif is_blacklisted:
                    logging.debug(f"REJECTED FILE (BLACKLISTED): {file_path}")
                else:
                    final_items_to_copy.append(file_path)
                    logging.debug(f"APPROVED FILE (DEFAULT): {file_path}")

            # Process directories for creation (only if not blacklisted)
            # We add directories to a set to ensure uniqueness and handle parent directories
            # The sorting by depth later will ensure correct creation order
            for dir_name in dirs:
                dir_path = (root_path / dir_name).resolve()
                is_blacklisted = is_path_covered_by_list(dir_path, literal_excluded_paths, grouped_glob_patterns_blacklist)
                is_whitelisted = is_path_covered_by_list(dir_path, literal_whitelisted_paths, grouped_glob_patterns_whitelist)

                if is_whitelisted:
                    final_dirs_to_create.add(dir_path)
                    logging.debug(f"APPROVED DIR (WHITELISTED): {dir_path}")
                elif is_blacklisted:
                    logging.debug(f"REJECTED DIR (BLACKLISTED): {dir_path}")
                    dirs.remove(dir_name)  # Prevent os.walk from entering this blacklisted directory
                else:
                    final_dirs_to_create.add(dir_path)
                    logging.debug(f"APPROVED DIR (DEFAULT): {dir_path}")

        # Convert set to list for sorting
        final_dirs_to_create = list(final_dirs_to_create)

        # Sort directories by depth to ensure parents are created before children
        final_dirs_to_create.sort(key=lambda p: len(p.parts))

        logging.debug(f"TOTAL FILES TO COPY: {len(final_items_to_copy)}")
        logging.debug(f"TOTAL DIRECTORIES TO CREATE: {len(final_dirs_to_create)}")

        # First, create all necessary directories
        for d_working_path in final_dirs_to_create:
            rel_path = d_working_path.relative_to(d_working)
            d_dst_path = dst_dir / rel_path
            try:
                if not d_dst_path.exists():
                    d_dst_path.mkdir(parents=True, exist_ok=True)
                    logging.debug(f"[CREATED DIR] {rel_path}")
                    copied_count += 1
                else:
                    logging.debug(f"[SKIPPED DIR - ALREADY EXISTS] {rel_path}")
            except Exception as e:
                logging.debug(f"[SKIP] Directory creation failed: {d_working_path} -> {d_dst_path} ({e})")
                continue

        # Then, copy all files
        for src_file_path in final_items_to_copy:
            rel_path = src_file_path.relative_to(d_working)
            dst_file_path = dst_dir / rel_path
            try:
                # Ensure parent directory exists (redundant if dirs are created first, but safe)
                dst_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file_path, dst_file_path)
                logging.debug(f"[COPIED FILE] {rel_path}")
                copied_count += 1
            except Exception as e:
                logging.debug(f"[SKIP] FILE COPY FAILED: {src_file_path} -> {dst_file_path} ({e})")
                continue

        logging.debug(f"[{PkTexts.DONE}] {copied_count} ITEM(S) COPIED TO '{dst_dir}'.")
        return dst_dir
    except Exception as e:
        ensure_debug_loged_verbose(traceback)
        return None  # Return None on error
