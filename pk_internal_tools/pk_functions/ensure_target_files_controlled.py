from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE, F_POTPLAYER_EXE


@ensure_seconds_measured
def ensure_target_files_controlled(d_working=None):
    from pk_internal_tools.pk_functions.ensure_target_files_controlled_2025_12_13 import ensure_target_files_controlled_2025_12_13

    import logging
    import shutil
    import traceback
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_p import get_p
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_target_files_controlled_2025_12_13 import ensure_target_files_controlled_2025_12_13
    

    """
    여러 대상을 fzf로 선택하여 열기, 부모열기, 경로복사, 이동 등의 작업을 수행합니다.
    """
    try:
        target_files = ensure_target_files_controlled_2025_12_13()
        if not target_files:
            logging.info("대상이 선택되지 않았습니다.")
            return False
        logging.info(f"{len(target_files)}개의 대상이 선택되었습니다:")
        for target in target_files:
            logging.info(f"{target}")

        func_n = get_caller_name()

        key_name = '작업옵션'
        options = ["열기", "부모열기", "경로복사", "이동", "play with Losslesscut", "Potplayer로 재생", "종료"]
        guide_text = f"{len(target_files)}개의 대상에 대한 작업을 선택하세요."
        work_option = ensure_value_completed(
            key_name=key_name,
            func_n=func_n,
            options=options,
            guide_text=guide_text
        )

        if not work_option:
            return False

        if work_option == "열기":
            for target in target_files:
                ensure_command_executed(f'start "" "{target}"')
            logging.info(f"{len(target_files)}개의 대상을 열었습니다.")

        elif work_option == "스캔":
            ensure_target_files_controlled_2025_12_13(operation_option="스캔")

        elif work_option == "부모열기":
            parent_dirs = sorted(list({get_p(target) for target in target_files}))
            for parent_dir in parent_dirs:
                ensure_command_executed(f'start "" "{parent_dir}"')
            logging.info(f"{len(parent_dirs)}개의 고유한 부모 폴더를 열었습니다.")

        elif work_option == "경로복사":
            paths_to_copy = "\n".join(target_files)
            PATH_COUNT_THRESHOLD = 20

            if len(target_files) > PATH_COUNT_THRESHOLD:
                save_option_key = "저장 방식"
                save_option_guide = f"선택한 경로가 {PATH_COUNT_THRESHOLD}개를 초과합니다. 어떻게 처리할까요"
                save_options = ["클립보드에 복사", "파일로 저장"]
                save_option = ensure_value_completed(
                    key_name=save_option_key,
                    func_n=func_n,
                    options=save_options,
                    guide_text=save_option_guide
                )

                if save_option == "파일로 저장":
                    from datetime import datetime
                    from pk_internal_tools.pk_objects.pk_directories import D_PK_CACHE

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file_name = f"selected_paths_{timestamp}.txt"
                    output_path = Path(D_PK_CACHE) / output_file_name

                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(paths_to_copy)

                    logging.info(f"{len(target_files)}개의 경로를 다음 파일에 저장했습니다: {output_path}")
                    ensure_command_executed(f'start "" "{output_path.parent}"')

                else:  # "클립보드에 복사" or user cancelled
                    ensure_text_saved_to_clipboard(paths_to_copy)
                    logging.info(f"{len(target_files)}개의 경로를 클립보드에 복사했습니다.")

            else:  # Less than or equal to threshold
                ensure_text_saved_to_clipboard(paths_to_copy)
                logging.info(f"{len(target_files)}개의 경로를 클립보드에 복사했습니다.")

        elif work_option == "부모열기":  # Renamed from 부모열기
            parent_dirs = sorted(list({get_p(target) for target in target_files}))
            for parent_dir in parent_dirs:
                ensure_command_executed(f'start "" "{parent_dir}"')
            logging.info(f"{len(parent_dirs)}개의 고유한 부모 폴더를 열었습니다.")

        elif work_option == "경로복사":  # Renamed from 경로복사
            paths_to_copy = "\n".join(target_files)
            PATH_COUNT_THRESHOLD = 20

            if len(target_files) > PATH_COUNT_THRESHOLD:
                save_option_key = "저장 방식"
                save_option_guide = f"선택한 경로가 {PATH_COUNT_THRESHOLD}개를 초과합니다. 어떻게 처리할까요"
                save_options = ["클립보드에 복사", "파일로 저장"]
                save_option = ensure_value_completed(
                    key_name=save_option_key,
                    func_n=func_n,
                    options=save_options,
                    guide_text=save_option_guide
                )

                if save_option == "파일로 저장":
                    from datetime import datetime
                    from pk_internal_tools.pk_objects.pk_directories import D_PK_CACHE

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file_name = f"selected_paths_{timestamp}.txt"
                    output_path = Path(D_PK_CACHE) / output_file_name

                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(paths_to_copy)

                    logging.info(f"{len(target_files)}개의 경로를 다음 파일에 저장했습니다: {output_path}")
                    ensure_command_executed(f'start "" "{output_path.parent}"')

                else:  # "클립보드에 복사" or user cancelled
                    ensure_text_saved_to_clipboard(paths_to_copy)
                    logging.info(f"{len(target_files)}개의 경로를 클립보드에 복사했습니다.")

            else:  # Less than or equal to threshold
                ensure_text_saved_to_clipboard(paths_to_copy)
                logging.info(f"{len(target_files)}개의 경로를 클립보드에 복사했습니다.")

        elif work_option == "이동":
            dest_path_key = "이동할 경로"
            dest_path_guide = f"{len(target_files)}개 파일을 어디로 이동하시겠습니까?"
            dest_path = ensure_value_completed(
                key_name=dest_path_key,
                func_n=func_n,
                guide_text=dest_path_guide
            )
            if dest_path and Path(dest_path).is_dir():
                moved_count = 0
                for target in target_files:
                    try:
                        shutil.move(target, dest_path)
                        moved_count += 1
                    except Exception as e:
                        logging.error(f"'{target}' 이동 실패: {e}")
                logging.info(f"{moved_count}개의 파일을 '{dest_path}'(으)로 이동했습니다.")
            elif dest_path:
                logging.warning("유효한 폴더 경로를 입력해야 합니다.")

        elif work_option == "play with Losslesscut":
            for target in target_files:
                if Path(target).is_file():
                    ensure_command_executed(f'start "{get_window_title_temp()}" "{F_LOSSLESSCUT_EXE}" "{target}"')
                    logging.info(f"'{target}'을 play with Losslesscut했습니다.")
                else:
                    logging.warning(f"'{target}'은(는) 파일이 아니므로 play with Losslesscut할 수 없습니다.")

        elif work_option == "Potplayer로 재생":
            for target in target_files:
                if Path(target).is_file():
                    ensure_command_executed(f'start "" "{F_POTPLAYER_EXE}" "{target}"')
                    logging.info(f"'{target}'을 Potplayer로 재생했습니다.")
                else:
                    logging.warning(f"'{target}'은(는) 파일이 아니므로 Potplayer로 재생할 수 없습니다.")

        elif work_option == "종료":
            logging.info("작업을 종료합니다.")
            return False  # Exit the function

        return True

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return False
