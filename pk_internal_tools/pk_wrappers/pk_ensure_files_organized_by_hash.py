import os
import logging
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_WORKING, d_pk_root
from pk_internal_tools.pk_functions.ensure_files_organized_by_hash import ensure_files_organized_by_hash
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done

if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # n. Get source directory from user
        source_dir_str = ensure_value_completed(
            key_name='source_directory',
            guide_text="해시 기반으로 정리할 대상 폴더를 선택하세요:",
            options=[str(D_PK_WORKING), os.getcwd(), str(D_DOWNLOADS), str(d_pk_root)]
        )
        source_dir = Path(source_dir_str)

        # n. Define and suggest destination directory
        suggested_dest_dir = Path(f"{source_dir_str}_hashed")
        dest_dir_str = ensure_value_completed(
            key_name='destination_directory',
            guide_text=f"결과물을 저장할 목적지 폴더를 선택하세요 (기본값: {suggested_dest_dir}):",
            options=[str(suggested_dest_dir)]
        )
        dest_dir = Path(dest_dir_str)

        logging.info(f"Source: {source_dir}")
        logging.info(f"Destination: {dest_dir}")

        # 3. Confirmation
        confirm_message = f"'{source_dir}'의 모든 파일을 '{dest_dir}'로 이동합니다. 이 작업은 되돌릴 수 없습니다. 계속하시겠습니까?"
        confirmation = ensure_value_completed_2025_10_12_0000(
            key_name='confirmation',
            guide_text=confirm_message,
            options=["yes", "no"]
        )

        if confirmation.lower() == 'yes':
            # 4. Execute the core function
            ensure_files_organized_by_hash(
                source_directory=source_dir,
                destination_directory=dest_dir
            )
        else:
            logging.warning("작업이 사용자에 의해 취소되었습니다.")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
