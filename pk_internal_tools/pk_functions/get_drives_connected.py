def get_drives_connected():
    import os
    import string

    import logging

    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    logging.debug(f"연결된 드라이브: {drives}")
    return drives
