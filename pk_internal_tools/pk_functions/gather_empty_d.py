from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.is_d import is_d
import logging


def gather_empty_d(d_working: str, d_dst=None):
    import os

    """
    d_src에서 빈 d를 찾아 d_dst 로 이동하는 함수.
    """
    if d_dst is None:
        d_dst = r"G:\Downloads\[empty]"

    ensure_pnx_made(pnx=d_dst, mode="d")  # 대상 d 생성

    if not is_d(d_working):
        logging.debug(f"'{d_working}' is not a valid d.")
        return

    #  1. 빈 d를 찾아 이동 (한 번만 exec )
    for root, d_nx_list, file_nxs in os.walk(d_working, topdown=False):
        if not d_nx_list and not file_nxs and is_empty_d(root):
            ensure_pnx_moved(pnx=root, d_dst=d_dst)

    #  2. 빈 트리(리프 d)를 이동 후 remove
    logging.debug(f"d_working={d_working}  ")

    if is_empty_tree(d_working):  # d_src 전체를 검사
        for root, d_nx_list, _ in os.walk(d_working, topdown=True):
            for d_nx in d_nx_list:
                d_working = os.path.abspath(os.path.join(root, d_nx))
                if is_leaf_d(d_working):
                    ensure_pnx_moved(pnx=d_working, d_dst=d_dst)
