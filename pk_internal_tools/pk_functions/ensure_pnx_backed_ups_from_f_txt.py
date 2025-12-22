from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT


def ensure_pnx_backed_ups_from_f_txt(dst):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    f_txt = rf'{D_PK_ROOT}\.pk_system\{func_n}.txt'
    ensure_pnx_made(pnx=D_PK_ROOT_HIDDEN, mode="d")
    ensure_pnx_made(pnx=f_txt, mode="f")
    # open_pnx(f_func_n_txt)
    texts = get_list_from_f(f=f_txt)
    texts = get_list_deduplicated(working_list=texts)
    texts = get_list_striped_element(working_list=texts)
    for text in texts:
        pk_ensure_pnx_backed_up(pnx_working=text, d_dst=dst)
