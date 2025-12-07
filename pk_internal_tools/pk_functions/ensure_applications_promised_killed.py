

def ensure_applications_promised_killed(pk_application_killing_mode = True):
    from pk_internal_tools.pk_functions.ensure_gemini_cli_killed import ensure_gemini_cli_killed
    from pk_internal_tools.pk_functions.ensure_losslescut_killed import ensure_losslescut_killed
    from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_functions.ensure_cmd_exe_killed import ensure_cmd_exe_killed
    from pk_internal_tools.pk_functions.ensure_pk_wrappers_killed import ensure_pk_wrappers_killed
    from pk_internal_tools.pk_functions.ensure_potplayer_killed import ensure_potplayer_killed
    from pk_internal_tools.pk_functions.ensure_windows_deduplicated_by_title import ensure_windows_deduplicated_by_title
    from pk_internal_tools.pk_functions.ensure_process_killed_by_image_name import ensure_process_killed_by_image_name
    from pk_internal_tools.pk_functions.ensure_window_titles_printed import ensure_window_titles_printed

    if QC_MODE:
        ensure_window_titles_printed()
        # ensure_slept(minutes=1)

    ensure_potplayer_killed()
    ensure_losslescut_killed()
    ensure_process_killed_by_image_name('chrome.exe')
    ensure_process_killed_by_image_name('code.exe')
    ensure_process_killed_by_image_name('cursor.exe')
    ensure_gemini_cli_killed()
    ensure_cmd_exe_killed()
    ensure_windows_deduplicated_by_title()

    if pk_application_killing_mode:
        ensure_process_killed_by_image_name('pycharm64.exe') # pk_optioni
        # ensure_pk_wrappers_killed()  # execute last # 프로세스 자기 자신 죽여서 수행불가 상태로 만듬.
