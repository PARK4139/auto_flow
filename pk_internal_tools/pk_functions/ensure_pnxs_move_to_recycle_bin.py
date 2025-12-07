from pathlib import Path
from typing import List, Optional, Union

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pnxs_move_to_recycle_bin(pnxs: Optional[List[Union[str, Path]]]):
    import logging
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_pnx_moved import ensure_pnx_moved
    from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    try:
        for pnx in pnxs:
            pnx = Path(pnx)
            if pnx.exists():
                logging.debug(f'''이동할 {pnx} is exist. ''')
                D_PK_RECYCLE_BIN.mkdir(parents=True, exist_ok=True)
                ensure_pnx_moved(pnx=pnx, d_dst=D_PK_RECYCLE_BIN)
            else:
                logging.debug(f'''이동할 {pnx} is not existing. ''')
    except:
        logging.debug("❌ An unexpected error occurred")
