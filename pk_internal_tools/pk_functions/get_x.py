def get_x(pnx):
    from pathlib import Path

    from pk_internal_tools.pk_functions.is_f import is_f

    if is_f(pnx=pnx):
        pnx = Path(pnx)
        ext = "".join(pnx.suffixes)
        return ext
    else:
        return ""
