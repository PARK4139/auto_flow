def get_windows_opened():
    try:
        from pk_internal_tools.pk_functions.get_windows_opened_raw import get_windows_opened_raw
        return get_windows_opened_raw()
    except:
        try:
            from pk_internal_tools.pk_functions.get_windows_opened_v_2025_10_03 import get_windows_opened_v_2025_10_03
            return get_windows_opened_v_2025_10_03()  # fallback function
        except:
            from pk_internal_tools.pk_functions.get_windows_opened_v_2025_10_02 import get_windows_opened_v_2025_10_02
            return get_windows_opened_v_2025_10_02()  # fallback function
