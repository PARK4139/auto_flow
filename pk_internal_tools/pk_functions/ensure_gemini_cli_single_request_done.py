from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_single_request_done():
    import logging

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title

    from pk_internal_tools.pk_functions import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_text_clicked_via_ocr_without_timelimit import \
        ensure_text_clicked_via_ocr_without_timelimit

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    msg = rf"프롬프트 수행시작"
    if not QC_MODE:
        ensure_spoken(msg)
    logging.debug(rf"msg={msg}")

    gemini_cli_window_title = get_gemini_cli_window_title()
    try:
        text = 'Type your message'  # gemini_prompt_done_signature_text
        if ensure_text_clicked_via_ocr_without_timelimit(text=text):
            ensure_spoken(rf"단일 프롬프트 수행완료.")
            ensure_window_to_front(gemini_cli_window_title)
            ensure_slept(milliseconds=77)
            # ensure_slept(milliseconds=500)
        else:
            ensure_window_to_front(gemini_cli_window_title)
            ensure_slept(milliseconds=77)
    except:
        msg = rf"프롬프트 수행완료 되었습니까?"
        ensure_spoken(msg)
        answer = input(
            "y/n=")  # TODO : GUI 로 ensure_answer_input_via_window_popup(options=[yes, no]) fallback 으로 input() 사용
        if answer.strip().lower() == 'y':
            ensure_spoken(rf"단일 프롬프트 수행완료.")
            ensure_window_to_front(gemini_cli_window_title)
            ensure_slept(milliseconds=77)
