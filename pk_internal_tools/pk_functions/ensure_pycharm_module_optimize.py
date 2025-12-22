def ensure_pycharm_module_import_script_optimize():
    from pk_internal_tools.pk_functions.ensure_window_to_front_of_pycharm import ensure_pycharm_window_to_front
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_directories import D_PK_WRAPPERS, D_PK_FUNCTIONS

    import os
    import logging
    import sys
    import pyautogui
    from pk_internal_tools.pk_functions.close_pycharm_tab import close_pycharm_tab_like_human
    from pk_internal_tools.pk_functions.ensure_pk_exit_silent import ensure_pk_exit_silent
    from pk_internal_tools.pk_functions.extend_pycharm_code import extend_pycharm_code_like_human
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
    from pk_internal_tools.pk_functions.get_value_by_file_id import get_value_by_file_id
    from pk_internal_tools.pk_functions.ensure_cursor_moved_to_text_location import ensure_cursor_moved_to_text_location
    from pk_internal_tools.pk_functions.move_cursor_to_top_of_pycarm_code import move_cursor_to_top_of_pycarm_code_like_human
    from pk_internal_tools.pk_functions.move_pycharm_cursor_to_file import move_pycharm_cursor_to_file
    from pk_internal_tools.pk_functions.open_pycharm_parrete import open_pycharm_parrete_like_human
    from pk_internal_tools.pk_functions.paste_and_enter import paste_and_enter_like_human
    from pk_internal_tools.pk_functions.press_ctrl_alt_l_nth import press_ctrl_alt_l_nth_like_human
    from pk_internal_tools.pk_functions.ensure_loop_delayed_at_loop_foot import ensure_loop_delayed_at_loop_foot
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    EXCLUDED_PREFIXES = ["TODO_", "prefix_to_exclude_"]
    ALLOWED_EXTENSIONS = [".py"]

    key_name = 'DIRECTORY_TO_DO_MACRO_ROUTINE'
    options = [D_PK_FUNCTIONS, D_PK_WRAPPERS]
    selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
    DIRECTORY_TO_DO_MACRO_ROUTINE = selected

    if not Path(DIRECTORY_TO_DO_MACRO_ROUTINE).exists():
        ensure_pk_exit_silent()

    file_names = os.listdir(DIRECTORY_TO_DO_MACRO_ROUTINE)
    file_names_filtered = [
        f for f in file_names
        if os.path.isfile(os.path.join(DIRECTORY_TO_DO_MACRO_ROUTINE, f))
           and not any(f.startswith(prefix) for prefix in EXCLUDED_PREFIXES)
           and os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS
    ]
    total_file_cnt = len(file_names_filtered)
    logging.debug(f'len(file_names_filtered)={len(file_names_filtered)}')

    if not file_names_filtered:
        logging.debug(f'pk_?_pk')  # 이 프로젝트에서 pk_?_pk 유일하다.
        ensure_pk_exit_silent()

    # saved_file_index 먼저 불러오고 file_cnt를 그 다음에 초기화해야 함
    key_name = 'saved_file_index'
    options = [0, 1]
    selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
    saved_file_index = selected

    saved_file_index = int(saved_file_index)
    loop_cnt = 1
    file_cnt = saved_file_index + 1  # Save point 이후부터 시작

    mouse_x, mouse_y = pyautogui.position()
    logging.debug(f"total_file_cnt={total_file_cnt}, saved_file_index={saved_file_index}")
    ensure_pycharm_window_to_front()
    try:
        for file_name in file_names_filtered:
            target_file = Path(DIRECTORY_TO_DO_MACRO_ROUTINE) / file_name
            new_x, new_y = pyautogui.position()
            if (new_x, new_y) != (mouse_x, mouse_y):
                logging.warning(f"{PkTexts.DETECTED} Mouse moved: start=({mouse_x},{mouse_y}) → now=({new_x},{new_y})")
                sys.exit(0)

            if file_cnt <= saved_file_index:
                logging.debug(f"{PkTexts.SKIPPED} {file_cnt}/{total_file_cnt} (reason: file_cnt <= saved_file_index)")
            elif get_str_from_f(str(target_file)).strip().startswith("def"):  # lazy import 완료간주.
                logging.debug(f"{PkTexts.SKIPPED} {file_cnt} / {total_file_cnt} (reason: content starts with 'def')")
            else:
                logging.debug(f"{PkTexts.STARTED} {file_cnt}/{total_file_cnt} {file_name}")

                file_base = os.path.splitext(file_name)[0]
                ensure_text_saved_to_clipboard(file_base)
                open_pycharm_parrete_like_human()
                paste_and_enter_like_human()
                move_cursor_to_top_of_pycarm_code_like_human()
                extend_pycharm_code_like_human()
                press_ctrl_alt_l_nth_like_human()
                close_pycharm_tab_like_human()

                ensure_loop_delayed_at_loop_foot(loop_cnt, mode_level=2, milliseconds_limit=50)
                loop_cnt += 1

            file_cnt += 1

    except Exception as e:
        logging.exception(f"예외 발생: {e}")
    finally:
        move_pycharm_cursor_to_file(__file__)
        move_pycharm_cursor_to_file(__file__)

        key_name = 'saved_file_index'
        options = [file_cnt - 1]
        selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
        saved_file_index = selected

        key_name = "cursor_location" # 현재 매크로 파일로 되돌하 오기 위함.
        text_to_move_cursor = get_value_by_file_id(file_id=get_file_id(key_name, func_n))
        logging.debug(f"{PkTexts.STOPPED} {file_cnt - 1}/{total_file_cnt}")
