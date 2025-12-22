from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
from pk_internal_tools.pk_objects.pk_files import F_PK_LOG


@ensure_seconds_measured
def ensure_pk_log_error_log_sent_to_cursor():
    import logging

    error_log_file = F_PK_LOG

    if not error_log_file.exists():
        logging.debug(f"에러 로그 파일이 존재하지 않습니다: {error_log_file}")
        return

    # 에러로그를 클립보드로 저장
    error_log_content_lines = []
    with open(error_log_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if "[ERROR]" in line:
                # if PkTexts.ERROR in line:
                error_log_content_lines.append(line.strip())
    error_log_content = "\n".join(error_log_content_lines)
    if not error_log_content or not error_log_content.strip():
        logging.debug("에러 로그 파일이 비어있습니다.")
        return
    ensure_text_saved_to_clipboard(text=error_log_content)

    # CURSOR로 로그 전송
    logging.debug(f"에러 로그를 Cursor로 전송합니다. 파일: {error_log_file}")
    while 1:
        for window_title in get_window_titles():
            if window_title.strip().endswith("- Cursor"):
                ensure_window_to_front(window_title_seg=window_title)
                ensure_pressed("ctrl", "v")  # paste
