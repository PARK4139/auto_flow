import logging
import os
import re
import shutil  # For renaming directories/files
import textwrap
import traceback
from pathlib import Path
from typing import Optional, Tuple

from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_find_and_replace_target_file_texts import find_and_replace_target_file_texts
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE_HALF, PK_UNDERLINE_SHORT, PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_file_extensions import ALL_CODE_EXTENSIONS
from pk_internal_tools.pk_objects.pk_modes import PkModesForPnxReplacement, PkModesForPnxTextTransformation, PkModesForPnxTargetScope
from pk_internal_tools.pk_objects.pk_modes import PkModesForPnxSearchDepth
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


@ensure_seconds_measured
def ensure_pnx_names_and_target_file_texts_replaced(
        old_text: Optional[str] = None,
        new_text: Optional[str] = None,
        replacement_option: Optional[PkModesForPnxReplacement] = None,
        text_transformation: Optional[PkModesForPnxTextTransformation] = None,
        scope: Optional[PkModesForPnxTargetScope] = None,
        search_depth: Optional[PkModesForPnxSearchDepth] = None,
        file_extensions: Optional[Tuple[str, ...]] = None,
        case_sensitive: Optional[str] = None,
        d_working_root: Optional[Path] = None
):
    """
        TODO: Write docstring for ensure_pnx_names_and_target_file_texts_replaced.
    """
    try:
        """
        PNX 프로젝트 내의 파일/디렉토리 이름 및 파일 콘텐츠 텍스트를 교체합니다.
        """

        ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
        func_n = get_caller_name()

        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}PNX 이름 및 파일 콘텐츠 교체 스크립트 시작{PkColors.RESET}")
        logging.info(PK_UNDERLINE)

        if not d_working_root:
            d_working_root = ensure_value_completed(
                key_name="d_working_root",
                func_n=func_n,
                guide_text="교체 작업을 수행할 범위를 선택하세요:",
                options=[str(D_PK_ROOT)]
            )
            d_working_root = Path(d_working_root)
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

        logging.info(f"{PK_UNDERLINE_SHORT} 교체 작업 범위 선택 {PK_UNDERLINE_HALF}")

        if replacement_option is None:
            options = [member.value.lower() for member in PkModesForPnxReplacement]
            replacement_option = ensure_value_completed(
                key_name="replacement_option",
                func_n=func_n,
                guide_text="교체 작업을 수행할 범위를 선택하세요:",
                options=options
            )
            selected_scope = PkModesForPnxReplacement(replacement_option.upper())
        else:
            selected_scope = replacement_option
        logging.info(f"선택된 교체 범위: {selected_scope.value}")

        # Original and Replacement Text ---
        if old_text is None:
            original_text = ensure_value_completed(
                key_name="old_text",
                func_n=func_n,
                guide_text="교체할 기존 텍스트를 입력하세요:",
                history_reset=True,
            )
        else:
            original_text = old_text
        if new_text is None:
            replacement_text = ensure_value_completed(
                key_name="new_text",
                func_n=func_n,
                guide_text="새로운 텍스트를 입력하세요:",
                history_reset=True
            )
        else:
            replacement_text = new_text

        if not original_text or not replacement_text:
            logging.error("기존 텍스트와 새로운 텍스트는 필수 입력값입니다. 작업을 종료합니다.")
            return

        # --- 3. Text Transformation ---
        if text_transformation is None:
            transformation_options = [member.value.lower() for member in PkModesForPnxTextTransformation]
            selected_transformation_name = ensure_value_completed(
                key_name="select_text_transformation",
                func_n=func_n,
                guide_text="원본/교체 텍스트에 적용할 변환을 선택하세요:",
                options=transformation_options,
            )
            selected_transformation = PkModesForPnxTextTransformation(selected_transformation_name.upper())
        else:
            selected_transformation = text_transformation
        logging.info(f"선택된 텍스트 변환: {selected_transformation.value}")

        # Apply transformation
        transformed_original_text = original_text
        transformed_replacement_text = replacement_text

        if selected_transformation == PkModesForPnxTextTransformation.TO_UPPER:
            transformed_original_text = original_text.upper()
            transformed_replacement_text = replacement_text.upper()
        elif selected_transformation == PkModesForPnxTextTransformation.TO_LOWER:
            transformed_original_text = original_text.lower()
            transformed_replacement_text = replacement_text.lower()

        logging.info(f"변환된 원본 텍스트: '{transformed_original_text}'")
        logging.info(f"변환된 교체 텍스트: '{transformed_replacement_text}'")

        # --- 4. Target Scope (Full Project, Custom Dirs, Specific Files) ---
        if scope is None:
            scope_options = [member.value.lower() for member in PkModesForPnxTargetScope]
            scope_to_replacement = ensure_value_completed(
                key_name="scope_to_replacement",
                func_n=func_n,
                guide_text="교체 작업을 수행할 대상 범위를 선택하세요:",
                options=scope_options,
            )
            selected_target_scope = PkModesForPnxTargetScope(scope_to_replacement.upper())
        else:
            selected_target_scope = scope
        logging.info(f"선택된 대상 범위: {selected_target_scope.value}")

        target_paths_to_process = []
        if selected_target_scope == PkModesForPnxTargetScope.FULL_PROJECT:
            target_paths_to_process = [d_working_root]
        elif selected_target_scope == PkModesForPnxTargetScope.CUSTOM_DIRECTORIES:
            custom_dirs_str = ensure_value_completed(
                key_name=f"custom_directories",
                func_n=func_n,
                guide_text="처리할 사용자 지정 디렉토리 경로(콤마로 구분)를 입력하세요:"
            )
            if custom_dirs_str:
                target_paths_to_process = [Path(d.strip()) for d in custom_dirs_str.split(',') if d.strip()]
            else:
                logging.error("사용자 지정 디렉토리 경로가 입력되지 않았습니다. 작업을 종료합니다.")
                return
        elif selected_target_scope == PkModesForPnxTargetScope.SPECIFIC_FILES:
            specific_files_str = ensure_value_completed(
                key_name=f"specific_files",
                func_n=func_n,
                guide_text="처리할 특정 파일 경로(콤마로 구분)를 입력하세요:"
            )
            if specific_files_str:
                target_paths_to_process = [Path(f.strip()) for f in specific_files_str.split(',') if f.strip()]
            else:
                logging.error("특정 파일 경로가 입력되지 않았습니다. 작업을 종료합니다.")
                return

        # --- 5. File Extensions ---
        if file_extensions is None:
            file_extensions_guide = f"대상 파일 확장자(콤마로 구분, 예: .py,.txt). 비워두면 모든 코드 확장자를 대상으로 합니다."
            selected_extensions_names = ensure_values_completed(
                key_name="file_extensions",
                func_n=func_n,
                guide_text=file_extensions_guide,
                options=[f".{ext}" for ext in ALL_CODE_EXTENSIONS],
                history_reset=True
            )

            if selected_extensions_names:
                # Clean the selected extension names from the multi-select fzf which may have extra dots
                cleaned_extensions = [ext.strip().lstrip('.') for ext in selected_extensions_names]
                file_extensions = tuple(f".{ext}" for ext in cleaned_extensions if ext)
            else:
                file_extensions = tuple(f".{ext}" for ext in ALL_CODE_EXTENSIONS)  # 기본값: ALL_CODE_EXTENSIONS
        else:
            file_extensions = file_extensions
        logging.info(f"선택된 파일 확장자: {file_extensions if file_extensions else '모든 파일'}")

        # --- 6. Case Sensitivity ---
        if case_sensitive is None:
            case_sensitive = ensure_value_completed(
                key_name="case_sensitive",
                func_n=func_n,
                guide_text="대소문자를 구분하여 교체하시겠습니까? (y/n):",
                options=["y", "n"]
            )
            case_sensitive = (case_sensitive.lower() == 'y')
        else:
            case_sensitive = case_sensitive
        logging.info(f"대소문자 구분: {case_sensitive}")

        # --- 7. Directories to ignore ---
        ignored_directory_names = [".venv", ".venv_matter", "__pycache__", ".git", "dist", "build", ".egg-info", "pk_web_server.egg-info", ".pytest_cache", ".mypy_cache", "htmlcov", ".idea", ".vscode"]
        logging.info(f"무시할 디렉토리: {ignored_directory_names}")

        # --- 8. Search Depth ---
        if search_depth is None:
            search_depth_options = [member.value.lower() for member in PkModesForPnxSearchDepth]
            selected_search_depth_name = ensure_value_completed(
                key_name="select_search_depth",
                func_n=func_n,
                guide_text="검색 깊이를 선택하세요:",
                options=search_depth_options,
            )
            selected_search_depth = PkModesForPnxSearchDepth(selected_search_depth_name.upper())
        else:
            selected_search_depth = search_depth
        logging.info(f"선택된 검색 깊이: {selected_search_depth.value}")

        

        # --- Perform the replacement operations ---
        if selected_target_scope == PkModesForPnxTargetScope.SPECIFIC_FILES:
            for file_path in target_paths_to_process:
                if not file_path.is_file():
                    logging.warning(f"지정된 파일이 존재하지 않거나 파일이 아닙니다: {file_path}")
                    continue

                if selected_scope in [PkModesForPnxReplacement.FILE_NAMES_ONLY, PkModesForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                    # File renaming for specific files
                    old_file_path = file_path
                    current_name = file_path.name

                    if case_sensitive:
                        if transformed_original_text in current_name:
                            new_name = current_name.replace(transformed_original_text, transformed_replacement_text)
                            new_file_path = old_file_path.parent / new_name
                            try:
                                shutil.move(old_file_path, new_file_path)
                                logging.info(f"파일 이름 변경: {old_file_path} -> {new_file_path}")
                                file_path = new_file_path  # Update file_path for content replacement
                            except OSError as e:
                                logging.error(f"파일 이름 변경 실패 {old_file_path}: {e}")
                    else:  # Case-insensitive
                        if transformed_original_text.lower() in current_name.lower():
                            new_name = current_name.replace(transformed_original_text, transformed_replacement_text, -1)  # All occurrences
                            new_file_path = old_file_path.parent / new_name
                            try:
                                shutil.move(old_file_path, new_file_path)
                                logging.info(f"파일 이름 변경: {old_file_path} -> {new_file_path}")
                                file_path = new_file_path  # Update file_path for content replacement
                            except OSError as e:
                                logging.error(f"파일 이름 변경 실패 {old_file_path}: {e}")

                if selected_scope in [PkModesForPnxReplacement.FILE_CONTENTS_ONLY, PkModesForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                    # File content replacement for specific files
                    if (not file_extensions or file_path.suffix in file_extensions) and file_path.is_file():
                        try:
                            find_and_replace_target_file_texts(str(file_path), transformed_original_text, transformed_replacement_text, case_sensitive=case_sensitive)
                            logging.info(f"파일 콘텐츠 텍스트 교체: {file_path}")
                        except Exception as e:
                            logging.error(f"파일 콘텐츠 텍스트 교체 실패 {file_path}: {e}")

        else:  # FULL_PROJECT or CUSTOM_DIRECTORIES
            if QC_MODE: logging.debug(f"DEBUG_TARGET_PATHS: target_paths_to_process='{target_paths_to_process}'")
            for d_target in target_paths_to_process:
                if QC_MODE: logging.debug(f"DEBUG_TARGET_PATHS: Checking d_target='{d_target}', is_dir()={d_target.is_dir()}")
                if not d_target.is_dir():
                    logging.warning(f"지정된 디렉토리가 존재하지 않거나 디렉토리가 아닙니다: {d_target}")
                    continue

                for root, dirs, files in os.walk(d_target, topdown=True):
                    if QC_MODE: logging.debug(f"PNX_DEBUG: Walking through root: {root}")
                    if QC_MODE: logging.debug(f"PNX_DEBUG: Dirs before filter: {dirs}")
                    # Filter ignored directories
                    dirs[:] = [d for d in dirs if d not in ignored_directory_names]
                    if QC_MODE: logging.debug(f"PNX_DEBUG: Dirs after filter: {dirs}")

                    # Apply search depth logic
                    if selected_search_depth == PkModesForPnxSearchDepth.SHALLOW:
                        dirs[:] = []  # Prevent os.walk from descending into subdirectories
                        if QC_MODE: logging.debug(f"PNX_DEBUG: Shallow search activated. Dirs cleared.")

                    # Map to store renamed files within this 'root' iteration
                    renamed_files_map = {}

                    # 1. Directory renaming
                    if selected_scope in [PkModesForPnxReplacement.DIRECTORY_NAMES_ONLY, PkModesForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                        if QC_MODE: logging.debug(f"PNX_DEBUG: Attempting directory renaming. Selected scope: {selected_scope.value}")
                        for name in dirs:
                            if QC_MODE: logging.debug(f"PNX_DEBUG: Checking dir for rename: {Path(root) / name}")
                            if case_sensitive:
                                if QC_MODE: logging.debug(f"PNX_DEBUG: Case-sensitive check. '{transformed_original_text}' in '{name}'? {transformed_original_text in name}")
                                if transformed_original_text in name:
                                    new_name = name.replace(transformed_original_text, transformed_replacement_text)
                                    new_dir_path = Path(root) / new_name
                                    try:
                                        shutil.move(old_dir_path, new_dir_path)
                                        logging.info(f"디렉토리 이름 변경: {old_dir_path} -> {new_dir_path}")
                                    except OSError as e:
                                        logging.error(f"디렉토리 이름 변경 실패 {old_dir_path}: {e}")
                            else:  # Case-insensitive
                                if QC_MODE: logging.debug(f"PNX_DEBUG: Case-insensitive check. '{transformed_original_text.lower()}' in '{name.lower()}'? {transformed_original_text.lower() in name.lower()}")
                                if transformed_original_text.lower() in name.lower():
                                    new_name = name.replace(transformed_original_text, transformed_replacement_text, -1)  # All occurrences
                                    new_dir_path = Path(root) / new_name
                                    try:
                                        shutil.move(old_dir_path, new_dir_path)
                                        logging.info(f"디렉토리 이름 변경: {old_dir_path} -> {new_dir_path}")
                                    except OSError as e:
                                        logging.error(f"디렉토리 이름 변경 실패 {old_dir_path}: {e}")

                    # List of (current_file_path, original_name) for content replacement
                    processed_files_for_content_replacement = []

                    # 2. File renaming and preparing files for content replacement
                    if selected_scope in [PkModesForPnxReplacement.FILE_NAMES_ONLY, PkModesForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                        if QC_MODE: logging.debug(f"PNX_DEBUG: Attempting file renaming. Selected scope: {selected_scope.value}")
                        for name in list(files):  # Iterate over a copy of files to allow modification if needed
                            if QC_MODE: logging.debug(f"PNX_DEBUG: Checking file for rename: {Path(root) / name}. Suffix: {Path(name).suffix}. In file_extensions: {file_extensions}?")
                            if not file_extensions or Path(name).suffix in file_extensions:
                                old_file_path = Path(root) / name
                                current_name_in_iteration = name  # The name as seen by os.walk for this iteration

                                new_name_for_rename = current_name_in_iteration
                                if case_sensitive:
                                    if QC_MODE: logging.debug(f"PNX_DEBUG: Case-sensitive file rename check. '{transformed_original_text}' in '{current_name_in_iteration}'? {transformed_original_text in current_name_in_iteration}")
                                    if transformed_original_text in current_name_in_iteration:
                                        new_name_for_rename = current_name_in_iteration.replace(transformed_original_text, transformed_replacement_text)
                                else:  # Case-insensitive
                                    if QC_MODE: logging.debug(f"PNX_DEBUG: Case-insensitive file rename check. '{transformed_original_text.lower()}' in '{current_name_in_iteration.lower()}'? {transformed_original_text.lower() in current_name_in_iteration.lower()}")
                                    # Use regex for case-insensitive replacement to avoid replacing parts of the name incorrectly
                                    pattern = re.compile(re.escape(transformed_original_text), re.IGNORECASE)
                                    new_name_for_rename = pattern.sub(transformed_replacement_text, current_name_in_iteration)

                                if new_name_for_rename != current_name_in_iteration:
                                    if QC_MODE: logging.debug(f"PNX_DEBUG: File '{current_name_in_iteration}' will be renamed to '{new_name_for_rename}'.")
                                    new_file_path = Path(root) / new_name_for_rename
                                    try:
                                        shutil.move(old_file_path, new_file_path)
                                        logging.info(f"파일 이름 변경: {old_file_path} -> {new_file_path}")
                                        renamed_files_map[old_file_path] = new_file_path  # Store mapping
                                        processed_files_for_content_replacement.append((new_file_path, current_name_in_iteration))  # Use new path for content
                                    except OSError as e:
                                        logging.error(f"파일 이름 변경 실패 {old_file_path}: {e}")
                                        processed_files_for_content_replacement.append((old_file_path, current_name_in_iteration))  # If rename fails, use old path
                                else:
                                    if QC_MODE: logging.debug(f"PNX_DEBUG: No rename needed for file '{current_name_in_iteration}'.")
                                    # No rename, but still eligible for content replacement
                                    processed_files_for_content_replacement.append((old_file_path, current_name_in_iteration))
                            else:
                                if QC_MODE: logging.debug(f"PNX_DEBUG: File '{name}' skipped for rename due to extension filter.")
                                # Not eligible for rename, but might be for content replacement
                                processed_files_for_content_replacement.append((Path(root) / name, name))
                    else:
                        if QC_MODE: logging.debug(f"PNX_DEBUG: File renaming skipped. Selected scope: {selected_scope.value}")
                        # If no file renaming, all files are initially eligible for content replacement (if they match extensions)
                        processed_files_for_content_replacement = [(Path(root) / name, name) for name in files if not file_extensions or Path(name).suffix in file_extensions]
                        for file_path_obj, original_name_for_logging in processed_files_for_content_replacement:
                            if QC_MODE: logging.debug(f"PNX_DEBUG: File '{file_path_obj}' added for content replacement (no rename).")

                    # 3. File content replacement
                    if selected_scope in [PkModesForPnxReplacement.FILE_CONTENTS_ONLY, PkModesForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                        if QC_MODE: logging.debug(f"PNX_DEBUG: Attempting file content replacement. Selected scope: {selected_scope.value}")
                        for file_path_obj, original_name_for_logging in processed_files_for_content_replacement:  # Iterate over the potentially updated paths
                            if QC_MODE: logging.debug(f"PNX_DEBUG: Checking file for content replace: {file_path_obj}. Suffix: {file_path_obj.suffix}. In file_extensions: {file_extensions}?")
                            if not file_extensions or file_path_obj.suffix in file_extensions:
                                if file_path_obj.is_file():
                                    if QC_MODE: logging.debug(f"PNX_DEBUG: Replacing content in file: {file_path_obj}")
                                    try:
                                        find_and_replace_target_file_texts(str(file_path_obj), transformed_original_text, transformed_replacement_text, case_sensitive=case_sensitive)
                                        logging.info(f"파일 콘텐츠 텍스트 교체: {file_path_obj}")
                                    except Exception as e:
                                        logging.error(f"파일 콘텐츠 텍스트 교체 실패 {file_path_obj}: {e}")
                                else:
                                    logging.warning(f"콘텐츠 교체를 위해 파일을 찾을 수 없습니다 (이동되었거나 삭제되었을 수 있음): {file_path_obj}")
                            else:
                                if QC_MODE: logging.debug(f"PNX_DEBUG: File '{file_path_obj}' skipped for content replacement due to extension filter.")
        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
