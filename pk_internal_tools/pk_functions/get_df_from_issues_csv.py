from pk_internal_tools.pk_functions.ensure_pnx_moved import ensure_pnx_moved
from pk_internal_tools.pk_objects.pk_directories import D_USERPROFILE


def get_df_from_issues_csv():
    # 경로
    Downloads = rf"{D_USERPROFILE}/Downloads"
    issues_list_csv = rf"{D_USERPROFILE}/Downloads/Issues_list.csv"
    issues_list_csv_alternative = rf"{D_USERPROFILE}/Downloads/deprecated/Issues_list.csv"

    import pandas as pd
    from pathlib import Path
    df = None
    pnx = issues_list_csv
    if Path(pnx).exists():
        df = pd.read_csv(filepath_or_buffer=pnx)
    else:
        pnx = issues_list_csv_alternative
        if Path(pnx).exists():
            df = pd.read_csv(filepath_or_buffer=pnx)
    ensure_pnx_moved(pnx=pnx, d_dst=Downloads, with_overwrite=1)
    return df
