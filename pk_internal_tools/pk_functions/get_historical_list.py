from typing import List


def get_historical_list(f) -> List[str]:
    import os

    from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made

    from pathlib import Path
    f = str(Path(f).resolve())
    if not is_pnx_existing(f):
        ensure_pnx_made(pnx=f, mode="f")
    if not os.path.isfile(f):
        return []

    delimiter = "\n%%PK_DELIMITER%%\n"
    with open(f, 'r', encoding='utf-8') as f_obj:
        content = f_obj.read()
        # Split the content by the delimiter and filter out empty strings that may result from the split.
        items = [item.strip() for item in content.split(delimiter) if item.strip()]
    return items