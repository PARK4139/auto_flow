from typing import List

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def get_historical_list(f) -> List[str]:
    import os

    
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made

    from pathlib import Path
    f = str(Path(f).resolve())
    if not Path(f).exists():
        ensure_pnx_made(pnx=f, mode="f")
    if not os.path.isfile(f):
        return []

    delimiter = f"\n{PK_UNDERLINE}\n"
    with open(f, 'r', encoding='utf-8') as f_obj:
        content = f_obj.read()
        # Split the content by the delimiter and filter out empty strings that may result from the split.
        items = [item.strip() for item in content.split(delimiter) if item.strip()]
    return items
