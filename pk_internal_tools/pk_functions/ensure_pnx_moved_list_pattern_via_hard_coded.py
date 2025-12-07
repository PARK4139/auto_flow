import colorama

from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from os.path import dirname
from functools import lru_cache
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_pnx_moved_list_pattern_via_hard_coded():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # pnx=rf"D:\#기타\pkg_dirs"
    # pnx=rf"D:\#기타\pkg_files"
    pnx = rf"D:\#기타"
    pnx = rf"D:\#기타\pkg_files\pk_video"

    txt_to_exclude_list = [
        F_DB_YAML,
        F_SUCCESS_LOG,
        F_LOCAL_PKG_CACHE_PRIVATE,
    ]

    # d_list, f_list=get_sub_pnxs_without_walking(pnx=item_pnx, txt_to_exclude_list=txt_to_exclude_list)
    d_list, f_list = get_sub_pnx_list(pnx=pnx, txt_to_exclude_list=txt_to_exclude_list)

    # pnxs=d_list
    pnxs = f_list

    # pattern 대체 timestamp 를 붙이기
    # pnxs_and_pnxs_new=[]
    # for item in pnxs:
    #     pattern_new=''
    #     item_without_reg=re.sub(pattern, pattern_new, item[0]) # 날짜/시간 패턴을 모두 remove
    #     item_pn=get_pn(item_without_reg)
    #     item_x=get_x(item_without_reg)
    #     timestamp=get_pk_time_2025_10_20_1159("now")
    #     item_new=""
    #     if is_file(item[0]):
    #         item_new=f"{item_pn}_{timestamp}.{item_x}"
    #     else:
    #         item_new=f"{item_pn}_{timestamp}{item_x}"
    #     pnxs_and_pnxs_new.append([item[0], item_new])

    # [문자열] 패턴은 f명의 맨앞이나 뒤로 이동
    pnxs_and_pnxs_new = []
    for item in pnxs:
        item_pnx = item[0]
        pattern = r'(\[.*?\])'
        # item_pnx_new=get_str_moved_pattern_to_front(pattern=pattern, item_pnx=item_pnx)
        item_pnx_new = get_f_n_moved_pattern(pattern=pattern, pnx_working=item_pnx, mode_front=0)
        if item_pnx != item_pnx_new:  # item_pnx item_pnx_new가 다르면 추가
            pnxs_and_pnxs_new.append([item_pnx, item_pnx_new])

    # 확인
    ensure_iterable_log_as_vertical(item_iterable=pnxs_and_pnxs_new, item_iterable_n="바꿀 대상")
    logging.debug(rf'''len(pnxs_and_pnxs_new)="{len(pnxs_and_pnxs_new)}"  ''')

    # 적용
    ensure_pnxs_renamed_2025_10_29(pnx_list=pnxs_and_pnxs_new)
