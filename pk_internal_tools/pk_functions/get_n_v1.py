






from pk_internal_tools.pk_functions.is_f import is_f


def get_n_v1(pnx):
    import os
    if is_f(pnx=pnx):
        return rf"{os.path.splitext(os.path.basename(pnx))[0]}"
    else:
        return os.path.basename(pnx)
