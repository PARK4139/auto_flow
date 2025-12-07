from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing


def get_df_from_issues_list_csv_deprecated():
    # 경로
    Downloads = rf"{D_HOME}/Downloads"
    issues_list_csv = rf"{D_HOME}/Downloads/Issues_list.csv"
    issues_list_csv_alternative = rf"{D_HOME}/Downloads/deprecated/Issues_list.csv"

    import pandas as pd
    df = None
    pnx = issues_list_csv
    if is_pnx_existing(pnx):
        df = pd.read_csv(filepath_or_buffer=pnx)
    else:
        pnx = issues_list_csv_alternative
        if is_pnx_existing(pnx):
            df = pd.read_csv(filepath_or_buffer=pnx)
    ensure_pnx_moved(pnx=pnx, d_dst=Downloads, with_overwrite=1)
    return df
