from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
from pk_internal_tools.pk_functions.get_x import get_x
from pathlib import Path
from pk_internal_tools.pk_functions.get_p import get_p
from pk_internal_tools.pk_functions.ensure_func_info_saved import ensure_func_info_saved


def ensure_dummy_file_exists(file_pnx):
    import inspect
    file_pnx = Path(file_pnx)
    ensure_pnx_made(get_p(file_pnx), mode="d")
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if not file_pnx.exists():
        x = get_x(file_pnx)
        with open(file_pnx, 'wb') as f:
            f.write(b'\x00')  # 1바이트 더미
        func_data = {
            "n": func_n,
            "state": PkTexts.SUCCEEDED,
            "file_pnx": file_pnx,
        }
        ensure_func_info_saved(func_n, func_data)
        # return func_data
        # 이제 return 안하고 db 에서 가져와도 됨.
