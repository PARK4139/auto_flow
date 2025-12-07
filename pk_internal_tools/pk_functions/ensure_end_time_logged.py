

def ensure_end_time_logged():
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    import time
    end_time = time.time()
    GREEN = PK_ANSI_COLOR_MAP['CYAN']
    RESET = PK_ANSI_COLOR_MAP['RESET']
    print(f"ENDED AT : {GREEN}{time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    return end_time


