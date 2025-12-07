import logging


def get_os_n():
    import platform
    if platform.system() == 'Windows':
        return 'Windows'.lower()
    elif platform.system() == 'Linux':
        return 'Linux'.lower()
    else:
        return 'Unknown'.lower()
