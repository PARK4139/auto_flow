from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.is_f import is_f
import logging


def classify_pnx_list_to_pkg_compressed(src, without_walking=True):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # d 유효성 확인
    if is_f(pnx=src):
        logging.debug(f"{src}  ")
        return

    # f과 d get
    txt_to_exclude_list = [
        F_DB_YAML,
        F_SUCCESS_LOG,
        F_LOCAL_PKG_CACHE_PRIVATE,
    ]

    if without_walking == False:
        d_list, f_list = get_sub_pnx_list(pnx=src, txt_to_exclude_list=txt_to_exclude_list)
    else:
        d_list, f_list = get_sub_pnx_list(pnx=src, txt_to_exclude_list=txt_to_exclude_list, without_walking=0)

    # f 처리
    x_allowed = [".zip", '.tar']
    x_allowed = x_allowed + get_list_replaced_element_from_str_to_upper_case(working_list=x_allowed)
    src = get_pn(src)
    dst = rf"{src}\pkg_compressed"
    for f in f_list:
        f = f[0]
        file_p = get_p(f)
        file_x = get_x(f).replace(".", "")  # 확장자에서 점(.) remove
        if file_x in [ext.replace(".", "") for ext in x_allowed]:  # x_allowed의 확장자와 비교
            ensure_pnx_made(dst, mode="d")
            ensure_pnx_moved(pnx=f, d_dst=dst)
            logging.debug(rf'''file_new="{f}"  ''')
    logging.debug(rf'''dst="{dst}"  ''')
