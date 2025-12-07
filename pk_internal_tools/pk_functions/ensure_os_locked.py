from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_os_locked():
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_power_saved_as_s3 import ensure_power_saved_as_s3

    # TODO : 절전모드 진입 선공하면 아래 두줄 주석해재
    # ensure_screen_saved()
    # ensure_slept(seconds = 10)
    ensure_spoken('s3, 절전모드로 진입합니다')
    ensure_power_saved_as_s3()
