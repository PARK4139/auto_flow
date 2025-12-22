from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed


def print_sub_pnx_list(src):
    txt_to_exclude_list = [
        F_DB_YAML,
        F_SUCCESS_LOG,
        F_LOCAL_PKG_CACHE_PRIVATE,
    ]

    # dir_pnxs, file_pnxs = get_sub_pnxs_without_walking(pnx=item_pnx, txt_to_exclude_list=txt_to_exclude_list)
    d_list, f_list = get_sub_pnx_list(pnx=src, txt_to_exclude_list=txt_to_exclude_list)

    pnx_list = d_list + f_list

    # 확인
    ensure_iterable_data_printed(iterable_data=pnx_list, iterable_data_n="바꿀 대상")
    logging.debug(rf'''len(pnxs)="{len(pnx_list)}"  ''')
