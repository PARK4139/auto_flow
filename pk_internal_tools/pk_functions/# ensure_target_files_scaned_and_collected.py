import logging

from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS


def ensure_target_files_scaned_and_collected():
    """메인 흐름: 스캔 후 이동"""
    import os
    import sys

    tab_completer = [D_PK_WORKING, d_pk_root, D_DOWNLOADS, rf"{D_DOWNLOADS}\[]\pk_ani"]

    # 명령 인자 우선
    if len(sys.argv) == 2:
        working_dir = sys.argv[1]
    else:
        working_dir = None

    while True:
        if not working_dir:
            working_dir = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=tab_completer)
            tab_completer.append(working_dir)

        if not os.path.isdir(working_dir):
            print_red(f"Error: '{working_dir}' 는 유효한 디렉토리가 아닙니다.")
            sys.exit(1)

        f_list = collect_f_list_recursive(working_dir)
        total_before = len(f_list)
        if total_before == 0:
            logging.debug("수집 대상이 없습니다.")
            logging.debug(f'''"수집 대상이 없습니다." ''')

            break

        print_f_list_preview(f_list)

        choice = ensure_value_completed_2025_10_12_0000(key_name='choice (o/x)', options=['o', 'x'])
        if choice.strip().lower() != 'o':
            print("수집 취소됨.")
            return

        # 이동 전 파일 수 확인
        print(f"이동 전 파일 개수: {total_before}개")
        collect_and_move(f_list, working_dir)
        # 이동 후 파일 수 확인
        dst_dir = f"{working_dir.rstrip(os.sep)}_merged"
        moved_count = len([name for name in os.listdir(dst_dir) if os.path.isfile(os.path.join(dst_dir, name))])
        print(f"이동 후 파일 개수: {moved_count}개")

        print(f"모든 항목을 '{working_dir}_merged'로 이동했습니다. (이동됨: {moved_count}/{total_before})")
        continue

        choice = ensure_value_completed_2025_10_12_0000(key_name='choice (o/x)', options=['o', 'x'])
        if choice.strip().lower() != 'o':
            print("수집 취소됨.")
            continue

        collect_and_move(f_list, working_dir)
        print(f"모든 항목을 '{working_dir}_merged'로 이동했습니다.")
        continue
