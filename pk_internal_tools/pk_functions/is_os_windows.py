def is_os_windows():
    import platform

    if platform.system() == 'Windows':
        # if QC_MODE:
        #     ensure_printed_once(f'''windows is detected ''')
        return 1
    else:
        # if QC_MODE:
        #     ensure_printed_once(f'''windows is not detected ''')
        return 0
