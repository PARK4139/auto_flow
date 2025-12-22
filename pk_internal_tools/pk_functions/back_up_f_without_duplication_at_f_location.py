def back_up_f_without_duplication_at_f_location(f: str) -> str:
    import logging
    import os
    import shutil
    import re

    if not os.path.isfile(f):
        logging.error(f"[BACKUP] File not found: {f}")
        raise FileNotFoundError(f"File not found: {f}")
    base_p, f_nx = os.path.split(f)
    f_n, f_x = os.path.splitext(f_nx)
    pattern = re.compile(rf"^{re.escape(f_n)} \((\d+)\)\.bak$")
    existing_nums = []
    try:
        for name in os.listdir(base_p):
            m = pattern.fullmatch(name)
            if m:
                existing_nums.append(int(m.group(1)))
    except Exception as e:
        logging.warning(f"Failed to scan directory: {e}")
    try:
        next_num = max(existing_nums, default=0) + 1
        candidate = os.path.join(base_p, f"{f_n} ({next_num}).bak")
        shutil.copy2(f, candidate)
        logging.debug(f"[BACKUP] {candidate}")
        return candidate
    except Exception as e:
        logging.error(f"[BACKUP] Failed to create backup: {e}")
        raise
