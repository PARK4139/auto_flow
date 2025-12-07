from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_cursor_worked_done():
    import logging
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_objects.pk_gui import ask_user
    text = "CURSOR 작업 완료"
    if QC_MODE:
        try:
            ask_user(
                text=text,
                title="작업 완료",
                buttons=["확인"],
                auto_click_positive_btn_after_milliseconds=1500,
                # auto_click_positive_btn_after_milliseconds=2000,
                sync_mode=True,
            )
        except Exception as e:
            logging.error(f"GUI 팝업 표시 실패: {e}")
            ensure_spoken(text)