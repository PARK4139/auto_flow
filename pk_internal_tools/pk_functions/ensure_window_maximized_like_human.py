from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_window_maximized_like_human():
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    ensure_pressed("alt", "space")
    # ensure_slept(milliseconds=40) # -> 간헐적 실패
    # ensure_slept(milliseconds=77) # -> succeeded -> 느림
    ensure_slept(milliseconds=44)  # pk_checkpoint
    ensure_pressed("x")
    # ensure_slept(milliseconds=77)
    # ensure_slept(milliseconds=40)
