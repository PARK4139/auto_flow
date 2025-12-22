def get_windows_opened():
    from pk_internal_tools.pk_functions.get_windows_opened_2025_12_12 import get_windows_opened_2025_12_12
    from pk_internal_tools.pk_functions.get_windows_opened_2025_10_03 import get_windows_opened_2025_10_03
    from pk_internal_tools.pk_functions.get_windows_opened_2025_10_02 import get_windows_opened_2025_10_02
    try:
        return get_windows_opened_2025_12_12()
    except Exception as e:
        try:
            return get_windows_opened_2025_10_03()  # fallback function
        except Exception as e:
            return get_windows_opened_2025_10_02()  # fallback function
