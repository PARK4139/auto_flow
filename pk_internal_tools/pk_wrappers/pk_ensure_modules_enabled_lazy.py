import logging
import os
import os.path
import re
import traceback

from pk_internal_tools.pk_functions.backup_workspace import backup_workspace
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.restore_workspace_from_latest_archive import restore_workspace_from_latest_archive
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools


def move_import_to_function_start(body_lines, indent_level):
    """본문 중간에 있는 import 문을 함수 시작 부분으로 이동"""
    imports = []
    non_import_lines = []

    # 임포트 문을 함수 본문에서 분리
    for line in body_lines:
        if re.match(r'^\s*(import|from\s+\w+\s+import)\b', line.strip()):
            imports.append(line.strip())
        else:
            non_import_lines.append(line)

    # 적절한 들여쓰기를 적용한 import 문 생성
    formatted_imports = [f"{' ' * indent_level}{imp}\n" for imp in imports]
    return formatted_imports + non_import_lines


def pk_ensure_modules_enabled_lazy_once(f_working, D_PKG_ARCHIVED, preview=False):
    """모듈 임포트를 lazy하게 업데이트하고 백업 및 복원 기능 추가"""
    # 백업
    func_n = get_caller_name()
    archive_path = backup_workspace(D_PKG_ARCHIVED, f_working, func_n)

    with open(file=f_working, mode='r', encoding=PkEncoding.UTF8.value) as f_obj:
        lines = f_obj.readlines()

    updated_lines = []
    inside_function = False
    function_body = []
    function_indent = 0

    # n. 사용자 임포트 블록 가져오기
    f_module_template = os.path.join(d_pk_external_tools, "refactor", "pk_template_modules.py")
    cleaned_import_block = clean_import_block(f_module_template)

    # 파일의 각 라인 처리
    for line in lines:
        stripped_line = line.strip()
        indent_level = len(line) - len(stripped_line)

        if stripped_line.startswith("def ") and stripped_line.endswith(":"):
            if inside_function:
                # 함수 종료 시점 처리: import 정리
                cleaned_body = move_import_to_function_start(function_body, function_indent + 4)
                updated_lines.extend(cleaned_body)
                function_body = []

            # 새로운 함수 시작
            inside_function = True
            function_indent = indent_level
            updated_lines.append(line)
        elif inside_function:
            if indent_level <= function_indent and stripped_line:
                # 함수 종료 시점 처리
                cleaned_body = move_import_to_function_start(function_body, function_indent + 4)
                updated_lines.extend(cleaned_body)
                function_body = []

                # 새로운 블록이 시작된 경우
                inside_function = False
                updated_lines.append(line)
            else:
                function_body.append(line)
        else:
            updated_lines.append(line)

    # 마지막 함수 처리
    if inside_function:
        cleaned_body = move_import_to_function_start(function_body, function_indent + 4)
        updated_lines.extend(cleaned_body)

    # 미리보기 모드에서는 실제 파일 수정 없이 출력만
    if preview:
        logging.info(f"[{PkTexts.PREVIEW}] 수정된 파일 내용 미리보기: '{f_working}'")
        logging.info(f"[{PkTexts.PREVIEW}] 추가될 임포트 블록: \n{cleaned_import_block}")
        for line in updated_lines:
            logging.info(line.strip())
    else:
        # 실제 수정이 실행 모드에서만 수행됨
        with open(file=f_working, mode='w', encoding=PkEncoding.UTF8.value) as f_out:
            f_out.writelines(updated_lines)

        logging.info(f"[{PkTexts.INSERTED}] 수정된 파일이 '{f_working}'에 저장되었습니다.")

    # REVERT 기능
    decision = ensure_value_completed_2025_10_12_0000(key_name=f"{PkTexts.AFTER_SERVICE}", options=[rf"{PkTexts.ORIGIN} {PkTexts.DELETE}", PkTexts.REVERT], )
    if decision == PkTexts.REVERT:
        restore_workspace_from_latest_archive(D_PKG_ARCHIVED, f_working)
    else:
        logging.info(f"백업이 '{archive_path}'에 저장되었습니다.")


def pk_ensure_modules_enabled_lazy():
    from enum import Enum
    encoding: Enum

    # apply to files
    # d_working = rf"{os.environ['USERPROFILE']}\Downloads\pk_system\pk_external_tools\workspace"
    # D_PKG_ARCHIVED = rf"{os.environ['USERPROFILE']}\Downloads\pk_system\pkg_archived"
    # 
    # # 실행 모드 설정 (프리뷰 또는 실제 실행 모드)
    # exec_mode = ensure_value_completed_2025_10_12_0000(
    #     key_hint=f"{PkTexts.MODE}=",
    #     values=[PkTexts.PREVIEW, f"{PkTexts.DEFAULT} {PkTexts.EXECUTION}"]
    # ).strip()
    # 
    # preview = exec_mode == PkTexts.PREVIEW
    # 
    # # .py 파일을 하나씩 처리
    # for f_working in get_pnxs_from_d_working(d_working=d_working):
    #     if is_f(f_working):
    #         if get_nx(f_working) != "__init__.py" and get_nx(f_working) != "pk_working.py":
    #             pk_ensure_modules_enabled_lazy_once(f_working, D_PKG_ARCHIVED, preview)

    # apply to file
    f_working = rf"{os.environ['USERPROFILE']}\Downloads\pk_system\pk_external_tools\workspace\pk_working.py"
    D_PKG_ARCHIVED = rf"{os.environ['USERPROFILE']}\Downloads\pk_system\pkg_archived"
    if is_f(f_working):
        exec_mode = ensure_value_completed_2025_10_12_0000(key_name=f"{PkTexts.MODE}", options=[PkTexts.PREVIEW, f"{PkTexts.DEFAULT} {PkTexts.EXECUTION}"]).strip()
        preview = exec_mode == PkTexts.PREVIEW
        pk_ensure_modules_enabled_lazy_once(f_working, D_PKG_ARCHIVED, preview)


if __name__ == "__main__":
    try:
        ensure_pk_log_initialized(__file__)
        pk_ensure_modules_enabled_lazy()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
