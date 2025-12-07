import inspect
import logging
import logging
import os
import re
import shutil
import traceback
from datetime import datetime
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
from pk_internal_tools.pk_functions.ensure_modules_imported_proper import ensure_modules_imported_proper
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_objects.pk_directories import D_ARCHIVED, d_pk_external_tools
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_texts import PkTexts



def collect_import_lines_from_dir(d_working: str, encoding_list=('utf-8', 'cp949')):
    imports = set()

    for pyfile in Path(d_working).rglob("*.py"):
        try:
            for encoding in encoding_list:
                try:
                    text = pyfile.read_text(encoding=encoding)
                    break
                except Exception:
                    continue
            else:
                continue  # 모든 인코딩 실패

            lines = text.splitlines()
            in_multiline_import = False
            import_block = []

            for line in lines:
                stripped = line.strip()
                if in_multiline_import:
                    import_block.append(stripped)
                    if ')' in stripped:
                        imports.add(" ".join(import_block))
                        in_multiline_import = False
                        import_block = []
                elif stripped.startswith("import ") or stripped.startswith("from "):
                    if stripped.endswith("("):
                        in_multiline_import = True
                        import_block = [stripped]
                    else:
                        imports.add(stripped)

        except Exception as e:
            print(f"[SKIP] {pyfile} - {e}")

    return sorted(imports)


def save_imports_to_txt(func_n, d_working: str):
    imports = collect_import_lines_from_dir(d_working)
    output_path = Path(d_working) / f"{func_n}.txt"
    output_path.write_text("\n".join(imports), encoding="utf-8")
    print(f"[STEP1] import lines saved to: {output_path}")
    return output_path


def open_txt_file_for_editing(f_txt: Path):
    print(f"[STEP2] opening {f_txt} for editing...")
    ensure_pnx_opened_by_ext(str(f_txt))


def confirm_editing_done() -> bool:
    response = ensure_value_completed_2025_10_12_0000(
        key_name="편집을 완료하셨습니까? (y/n)=",
        options=["y", "n"]
    ).lower()
    return response == "y"


def announce_start_applying():
    print("" + "=" * 60)
    print("📌 편집된 import 내용을 기반으로 적용을 시작합니다.")
    print("=" * 60 + "\n")


def backup_f_working(f_working: str, d_backup_target: str) -> str:
    if not os.path.exists(f_working):
        raise FileNotFoundError(f"[ERROR] 파일이 존재하지 않습니다: {f_working}")
    if not os.path.isfile(f_working):
        raise IsADirectoryError(f"[ERROR] 디렉토리가 아닌 파일만 지원합니다: {f_working}")

    # 파일 이름 및 타임스탬프 설정
    base_name = os.path.splitext(os.path.basename(f_working))[0]
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M")
    archive_basename = os.path.join(d_backup_target, f"{base_name}_{timestamp}")
    archive_output = archive_basename + ".tar.bz2"

    # 임시 디렉토리 생성 및 파일 복사
    temp_dir = os.path.join(d_backup_target, f"__temp_for_backup__{timestamp}")
    os.makedirs(temp_dir, exist_ok=True)
    shutil.copy2(f_working, os.path.join(temp_dir, os.path.basename(f_working)))

    # 압축 수행
    os.makedirs(d_backup_target, exist_ok=True)
    shutil.make_archive(
        base_name=archive_basename,
        format='bztar',
        root_dir=temp_dir,
        base_dir="."
    )

    # 임시 디렉토리 삭제
    shutil.rmtree(temp_dir)

    logging.info(f"[{PkTexts.COMPRESSED}] {archive_output}")
    print(f"[STEP5] 📦 백업 완료: {archive_output}")
    return archive_output


def preview_lazy_import_applied_code(code: str, lazy_imports: list[str]) -> str:
    def insert_lazy_imports(code: str, lazy_imports: list[str]) -> str:
        pattern = re.compile(r'(def\s+\w+\s*\(.*?\)\s*:)')

        def replacer(match):
            return f"{match.group(1)}\n    " + "\n    ".join(sorted(lazy_imports))

        return pattern.sub(replacer, code)

    preview_code = insert_lazy_imports(code, lazy_imports)
    return preview_code


if __name__ == "__main__":
    try:
        # ensure_modules_imported_proper()
        # TODO
        ensure_not_prepared_yet_guided()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
