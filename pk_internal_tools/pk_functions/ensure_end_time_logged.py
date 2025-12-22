

def ensure_end_time_logged():
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    import time
    end_time = time.time()
    GREEN = PkColors.CYAN
    RESET = PkColors.RESET
    print(f"ENDED AT : {GREEN}{time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    return end_time


