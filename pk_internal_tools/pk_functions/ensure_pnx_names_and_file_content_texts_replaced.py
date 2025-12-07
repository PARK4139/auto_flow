from pathlib import Path
from typing import Optional, Tuple

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE_HALF, PK_UNDERLINE_SHORT, PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForPnxReplacement, SetupOpsForPnxTextTransformation, SetupOpsForPnxTargetScope, SetupOpsForPnxSearchDepth


@ensure_seconds_measured
def ensure_pnx_names_and_file_content_texts_replaced(
        old_text: Optional[str] = None,
        new_text: Optional[str] = None,
        operation_scope: Optional[SetupOpsForPnxReplacement] = None,
        text_transformation: Optional[SetupOpsForPnxTextTransformation] = None,
        scope: Optional[SetupOpsForPnxTargetScope] = None,
        search_depth: Optional[SetupOpsForPnxSearchDepth] = None,
        file_extensions: Optional[Tuple[str, ...]] = None,
        case_sensitive: Optional[bool] = None,
        root_dir: Optional[Path] = None
):
    """
        TODO: Write docstring for ensure_pnx_names_and_file_content_texts_replaced.
    """
    try:

        """
        PNX 프로젝트 내의 파일/디렉토리 이름 및 파일 콘텐츠 텍스트를 교체합니다.
        """
        import traceback
        import logging
        import textwrap
        import re
        import os
        import shutil  # For renaming directories/files
        from pathlib import Path
        from enum import Enum

        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.ensure_find_and_replace_text_in_file import find_and_replace_text_in_file
        from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForPnxReplacement, SetupOpsForPnxTextTransformation, SetupOpsForPnxTargetScope
        from pk_internal_tools.pk_objects.pk_file_extensions import ALL_CODE_EXTENSIONS

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        func_n = get_caller_name()

        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}PNX 이름 및 파일 콘텐츠 교체 스크립트 시작{PK_ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)

        # Calculate D_PNX_PROJECT directly
        # pk_wrappers/pk_ensure_pnx_names_and_file_content_texts_replaced.py
        # -> src/pk_system
        # Path(__file__).parent is pk_wrappers
        # Path(__file__).parent.parent is pk_internal_tools
        # Path(__file__).parent.parent.parent is pk_system (the directory that contains pk_internal_tools)
        if root_dir:
            D_PNX_PROJECT = root_dir
        else:
            D_PNX_PROJECT = Path(__file__).parent.parent.parent  # This is src/pk_system

        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

        logging.info(f"{PK_UNDERLINE_SHORT} 교체 작업 범위 선택 {PK_UNDERLINE_HALF}")

        if operation_scope is None:
            options_list = [member.value.lower() for member in SetupOpsForPnxReplacement]
            selected_scope_name = ensure_value_completed(
                key_name="select_operation_scope",
                func_n=func_n,
                guide_text="교체 작업을 수행할 범위를 선택하세요:",
                options=options_list
            )
            selected_scope = SetupOpsForPnxReplacement(selected_scope_name.upper())
        else:
            selected_scope = operation_scope
        logging.info(f"선택된 교체 범위: {selected_scope.value}")

        # --- 2. Original and Replacement Text ---
        if old_text is None:
            original_text = ensure_value_completed(
                key_name="original_text",
                func_n=func_n,
                guide_text="교체할 기존 텍스트를 입력하세요:"
            )
        else:
            original_text = old_text
        if new_text is None:
            replacement_text = ensure_value_completed(
                key_name="replacement_text",
                func_n=func_n,
                guide_text="새로운 텍스트를 입력하세요:"
            )
        else:
            replacement_text = new_text

        if not original_text or not replacement_text:
            logging.error("기존 텍스트와 새로운 텍스트는 필수 입력값입니다. 작업을 종료합니다.")
            return

        # --- 3. Text Transformation ---
        if text_transformation is None:
            transformation_options = [member.value.lower() for member in SetupOpsForPnxTextTransformation]
            selected_transformation_name = ensure_value_completed(
                key_name="select_text_transformation",
                func_n=func_n,
                guide_text="원본/교체 텍스트에 적용할 변환을 선택하세요:",
                options=transformation_options,
            )
            selected_transformation = SetupOpsForPnxTextTransformation(selected_transformation_name.upper())
        else:
            selected_transformation = text_transformation
        logging.info(f"선택된 텍스트 변환: {selected_transformation.value}")

        # Apply transformation
        transformed_original_text = original_text
        transformed_replacement_text = replacement_text

        if selected_transformation == SetupOpsForPnxTextTransformation.TO_UPPER:
            transformed_original_text = original_text.upper()
            transformed_replacement_text = replacement_text.upper()
        elif selected_transformation == SetupOpsForPnxTextTransformation.TO_LOWER:
            transformed_original_text = original_text.lower()
            transformed_replacement_text = replacement_text.lower()

        logging.info(f"변환된 원본 텍스트: '{transformed_original_text}'")
        logging.info(f"변환된 교체 텍스트: '{transformed_replacement_text}'")

        # --- 4. Target Scope (Full Project, Custom Dirs, Specific Files) ---
        if scope is None:
            target_scope_options = [member.value.lower() for member in SetupOpsForPnxTargetScope]
            selected_target_scope_name = ensure_value_completed(
                key_name="scope_to_replacement",
                func_n=func_n,
                guide_text="교체 작업을 수행할 대상 범위를 선택하세요:",
                options=target_scope_options,
            )
            selected_target_scope = SetupOpsForPnxTargetScope(selected_target_scope_name.upper())
        else:
            selected_target_scope = scope
        logging.info(f"선택된 대상 범위: {selected_target_scope.value}")

        target_paths_to_process = []
        if selected_target_scope == SetupOpsForPnxTargetScope.FULL_PROJECT:
            target_paths_to_process = [D_PNX_PROJECT]
        elif selected_target_scope == SetupOpsForPnxTargetScope.CUSTOM_DIRECTORIES:
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
        elif selected_target_scope == SetupOpsForPnxTargetScope.SPECIFIC_FILES:
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
                multi_select=True
            )

            if selected_extensions_names:
                file_extensions = tuple(f".{ext.strip()}" for ext in selected_extensions_names if ext.strip())
            else:
                file_extensions = tuple(f".{ext}" for ext in ALL_CODE_EXTENSIONS)  # 기본값: ALL_CODE_EXTENSIONS
        else:
            file_extensions = file_extensions
        logging.info(f"선택된 파일 확장자: {file_extensions if file_extensions else '모든 파일'}")

        # --- 6. Case Sensitivity ---
        if case_sensitive is None:
            case_sensitive_option = ensure_value_completed(
                key_name="case_sensitive",
                func_n=func_n,
                guide_text="대소문자를 구분하여 교체하시겠습니까? (y/n):",
                options=["y", "n"]
            )
            case_sensitive = (case_sensitive_option.lower() == 'y')
        else:
            case_sensitive = case_sensitive
        logging.info(f"대소문자 구분: {case_sensitive}")

        # --- 7. Directories to ignore ---
        ignored_directory_names = [".venv", ".venv_matter", "__pycache__", ".git"]
        logging.info(f"무시할 디렉토리: {ignored_directory_names}")

        # --- 8. Search Depth ---
        if search_depth is None:
            search_depth_options = [member.value.lower() for member in SetupOpsForPnxSearchDepth]
            selected_search_depth_name = ensure_value_completed(
                key_name="select_search_depth",
                func_n=func_n,
                guide_text="검색 깊이를 선택하세요:",
                options=search_depth_options,
            )
            selected_search_depth = SetupOpsForPnxSearchDepth(selected_search_depth_name.upper())
        else:
            selected_search_depth = search_depth
        logging.info(f"선택된 검색 깊이: {selected_search_depth.value}")

        # --- Perform the replacement operations ---
        if selected_target_scope == SetupOpsForPnxTargetScope.SPECIFIC_FILES:
            for file_path in target_paths_to_process:
                if not file_path.is_file():
                    logging.warning(f"지정된 파일이 존재하지 않거나 파일이 아닙니다: {file_path}")
                    continue

                if selected_scope in [SetupOpsForPnxReplacement.FILE_NAMES_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
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

                if selected_scope in [SetupOpsForPnxReplacement.FILE_CONTENTS_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                    # File content replacement for specific files
                    if (not file_extensions or file_path.suffix in file_extensions) and file_path.is_file():
                        try:
                            find_and_replace_text_in_file(str(file_path), transformed_original_text, transformed_replacement_text, case_sensitive=case_sensitive)
                            logging.info(f"파일 콘텐츠 텍스트 교체: {file_path}")
                        except Exception as e:
                            logging.error(f"파일 콘텐츠 텍스트 교체 실패 {file_path}: {e}")

        else:  # FULL_PROJECT or CUSTOM_DIRECTORIES
            logging.debug(f"DEBUG_TARGET_PATHS: target_paths_to_process='{target_paths_to_process}'")
            for d_target in target_paths_to_process:
                logging.debug(f"DEBUG_TARGET_PATHS: Checking d_target='{d_target}', is_dir()={d_target.is_dir()}")
                if not d_target.is_dir():
                    logging.warning(f"지정된 디렉토리가 존재하지 않거나 디렉토리가 아닙니다: {d_target}")
                    continue

                for root, dirs, files in os.walk(d_target, topdown=True):
                    # Filter ignored directories
                    dirs[:] = [d for d in dirs if d not in ignored_directory_names]

                    # Apply search depth logic
                    if selected_search_depth == SetupOpsForPnxSearchDepth.SHALLOW:
                        dirs[:] = []  # Prevent os.walk from descending into subdirectories

                    # Map to store renamed files within this 'root' iteration
                    renamed_files_map = {}

                    # 1. Directory renaming
                    if selected_scope in [SetupOpsForPnxReplacement.DIRECTORY_NAMES_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                        for name in dirs:
                            old_dir_path = Path(root) / name
                            if case_sensitive:
                                if transformed_original_text in name:
                                    new_name = name.replace(transformed_original_text, transformed_replacement_text)
                                    new_dir_path = Path(root) / new_name
                                    try:
                                        shutil.move(old_dir_path, new_dir_path)
                                        logging.info(f"디렉토리 이름 변경: {old_dir_path} -> {new_dir_path}")
                                    except OSError as e:
                                        logging.error(f"디렉토리 이름 변경 실패 {old_dir_path}: {e}")
                            else:  # Case-insensitive
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
                    if selected_scope in [SetupOpsForPnxReplacement.FILE_NAMES_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                        for name in list(files):  # Iterate over a copy of files to allow modification if needed
                            if not file_extensions or Path(name).suffix in file_extensions:
                                old_file_path = Path(root) / name
                                current_name_in_iteration = name  # The name as seen by os.walk for this iteration

                                new_name_for_rename = current_name_in_iteration
                                if case_sensitive:
                                    if transformed_original_text in current_name_in_iteration:
                                        new_name_for_rename = current_name_in_iteration.replace(transformed_original_text, transformed_replacement_text)
                                else:  # Case-insensitive
                                    # Use regex for case-insensitive replacement to avoid replacing parts of the name incorrectly
                                    pattern = re.compile(re.escape(transformed_original_text), re.IGNORECASE)
                                    new_name_for_rename = pattern.sub(transformed_replacement_text, current_name_in_iteration)

                                if new_name_for_rename != current_name_in_iteration:
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
                                    # No rename, but still eligible for content replacement
                                    processed_files_for_content_replacement.append((old_file_path, current_name_in_iteration))
                            else:
                                # Not eligible for rename, but might be for content replacement
                                processed_files_for_content_replacement.append((Path(root) / name, name))
                    else:
                        # If no file renaming, all files are initially eligible for content replacement (if they match extensions)
                        processed_files_for_content_replacement = [(Path(root) / name, name) for name in files if not file_extensions or Path(name).suffix in file_extensions]

                    # 3. File content replacement
                    if selected_scope in [SetupOpsForPnxReplacement.FILE_CONTENTS_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
                        for file_path_obj, original_name_for_logging in processed_files_for_content_replacement:  # Iterate over the potentially updated paths
                            if not file_extensions or file_path_obj.suffix in file_extensions:
                                if file_path_obj.is_file():
                                    try:
                                        find_and_replace_text_in_file(str(file_path_obj), transformed_original_text, transformed_replacement_text, case_sensitive=case_sensitive)
                                        logging.info(f"파일 콘텐츠 텍스트 교체: {file_path_obj}")
                                    except Exception as e:
                                        logging.error(f"파일 콘텐츠 텍스트 교체 실패 {file_path_obj}: {e}")
                                else:
                                    logging.warning(f"콘텐츠 교체를 위해 파일을 찾을 수 없습니다 (이동되었거나 삭제되었을 수 있음): {file_path_obj}")
        return True
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
