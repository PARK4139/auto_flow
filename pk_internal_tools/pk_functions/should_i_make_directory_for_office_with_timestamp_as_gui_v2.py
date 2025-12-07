def should_i_make_directory_for_office_with_timestamp_as_gui_v2():
    from pk_internal_tools.pk_functions import ensure_pnx_made, get_pk_time_2025_10_20_1159
    from pk_internal_tools.pk_functions.is_pnx_required import is_pnx_required
    from pk_internal_tools.pk_objects.pk_gui import ask_user

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    import logging
    from pathlib import Path
    import traceback

    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    try:
        work_n = None
        pnx = None
        txt_clicked = None
        function = None
        txt_written = None
        txt_clicked, function, txt_written = ask_user(
            prompt="업무명을 입력해주세요",
            buttons=["입력", "n"],
            function=None,
            auto_click_negative_btn_after_seconds=30,
            title=f"{func_n}()",
            input_box_mode=True,
        )
        if txt_clicked != "입력":
            return
        work_n = txt_written
        work_n = work_n.strip()
        work_n = work_n.replace("\"", "")
        logging.debug(f'''[ {get_pk_time_2025_10_20_1159('now')} ] work_ns={work_n}  ''')
        if work_n == "":
            logging.debug(    f'''[ {get_pk_time_2025_10_20_1159('now')} ] work_n가 입력되지 않았습니다  ''')
            return

        txt_clicked, function, txt_written = ask_user(
            prompt="어느 경로에 만들까요?",
            buttons=["입력", "n"],
            function=None,
            auto_click_negative_btn_after_seconds=30,
            title=f"{func_n}()",
            input_box_mode=True,
        )
        if txt_clicked != "입력":
            return
        pnx = txt_written
        pnx = Path(pnx)
        if is_pnx_required(pnx):
            return
        logging.debug(rf'''pnx="{pnx}"  ''')
        logging.debug(rf'''work_n="{work_n}"  ''')
        timestamp = get_pk_time_2025_10_20_1159("yyyy MM dd (weekday) HH mm")
        pnx_new = rf"{pnx}\{timestamp} {work_n}"
        logging.debug(rf'''pnx_new="{pnx_new}"  ''')
        ensure_pnx_made(pnx=pnx_new, mode="d")
        pnx = pnx_new
        cmd = rf'explorer "{pnx}"'
        ensure_command_executed(cmd=cmd, mode="a")
        return
    except:
        logging.debug(f"{traceback.format_exc()}")
