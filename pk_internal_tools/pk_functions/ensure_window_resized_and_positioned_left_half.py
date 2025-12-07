from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_window_resized_and_positioned_left_half():
    # TODO : 이거 불명확한 동작. 업데이트 필요.
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    ensure_pressed("win", "left")
    # ensure_slept(milliseconds=500)  # 간헐적 실패 예방
