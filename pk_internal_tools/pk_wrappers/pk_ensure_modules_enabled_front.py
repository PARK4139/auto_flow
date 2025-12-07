import inspect
import logging
import logging
import os
import os.path
import os.path
import traceback

from pk_internal_tools.pk_functions.backup_workspace import backup_workspace
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
from pk_internal_tools.pk_functions.restore_workspace_from_latest_archive import restore_workspace_from_latest_archive
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import D_PKG_ARCHIVED
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root



def clean_import_block(block: str) -> str:
    result_lines = []
    for line in block.strip().splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            stripped = stripped[1:].strip()  # Remove comment characters
        result_lines.append(stripped)
    return "\n".join(result_lines)


def pk_ensure_modules_import_to_python_files():
    func_name = inspect.currentframe().f_code.co_name
    d_working = rf"{os.environ['USERPROFILE']}\Downloads\pk_system\pk_internal_tools\pk_wrappers\pk_functions"
    d_backup_root = os.path.join(d_pk_external_tools, "..", "pkg_archived")
    f_module_template = os.path.join(d_pk_external_tools, "refactor", "pk_template_modules.py")
    # 6. 파일 처리 (프리뷰 모드에서는 실제 파일 수정 없이 출력만)
    loop_cnt = 1
    while True:
        # n. 파일 경로 확인
        if not os.path.isdir(d_working):
            logging.warning(f"[{PkTexts.PATH_NOT_FOUND}] {d_working}")
            return

        # n. 사용자가 작성한 임포트 블록 가져오기
        raw_import_block = get_str_from_f(f=f_module_template)
        cleaned_import_block = clean_import_block(raw_import_block)

        # n. 사용자 입력으로 preview 모드 선택
        preview_mode = ensure_value_completed_2025_10_12_0000(
            key_name=f"{PkTexts.MODE}=",
            options=[PkTexts.PREVIEW, f"{PkTexts.DEFAULT} {PkTexts.EXECUTION}"]
        ) == PkTexts.PREVIEW

        # n. .py 파일 경로 가져오기
        py_files = [f for f in os.listdir(d_working) if f.endswith('.py')]
        full_paths = [os.path.join(d_working, f) for f in py_files]

        if not full_paths:
            logging.info(f"[{PkTexts.LISTED}] No .py files found.")
            return

        # n. 백업 수행 (실제 실행 모드에서만)
        archive_path = None
        if not preview_mode:
            archive_path = backup_workspace(d_working, d_backup_root, func_name)

        for root, _, files in os.walk(d_working):
            for file in files:
                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 임포트 블록이 이미 존재하는지 확인
                if all(line in content for line in cleaned_import_block.splitlines()):
                    logging.info(f"[{PkTexts.SKIPPED}] already contains imports: {file_path}")
                    continue

                # 프리뷰 모드일 경우 수정 예시만 출력
                if preview_mode:
                    logging.info(f"[{PkTexts.PREVIEW}] will insert imports into: {file_path}")
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_import_block + "\n\n" + content)
                    logging.info(f"[{PkTexts.INSERTED}] imports added to: {file_path}")
                loop_cnt += 1

        # 7. 후속 서비스 (삭제 또는 복원)
        if not preview_mode:
            decision = ensure_value_completed_2025_10_12_0000(
                key_name=f"{PkTexts.AFTER_SERVICE}=",
                options=[PkTexts.SATISFIED, PkTexts.REVERT],
            )
            if decision == PkTexts.SATISFIED:
                logging.info(f"[{PkTexts.SATISFIED}]")
                logging.info(f"[{PkTexts.DONE}] import injection {'(preview)' if preview_mode else '(executed)'}")
                # pk_ensure_pk_exit_silent() # pk_option
                continue
            elif decision == PkTexts.REVERT:
                restore_workspace_from_latest_archive(D_PKG_ARCHIVED, d_working)  # REVERT 실행
                logging.info(f"[{PkTexts.DONE}] {PkTexts.REVERT}")


def main():
    try:
        ensure_pk_log_initialized(__file__)
        pk_ensure_modules_import_to_python_files()
    except Exception as e:
        ensure_exception_routine_done(traceback=traceback, exception=e)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)


if __name__ == "__main__":
    main()
