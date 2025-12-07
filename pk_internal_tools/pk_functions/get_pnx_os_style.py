from pathlib import Path
from typing import Union

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_pnx_os_style(pnx: Union[str, Path]):
    from pathlib import Path
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
    from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
    from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

    # 입력을 Path 객체로 변환
    if isinstance(pnx, str):
        pnx = Path(pnx)
    
    # OS별 스타일 적용 후 Path 객체로 반환
    if is_os_wsl_linux():
        result = get_pnx_wsl_unix_style(str(pnx))
        return Path(result)
    elif is_os_windows():
        result = get_pnx_windows_style(str(pnx))
        return Path(result)
    else:
        result = get_pnx_unix_style(str(pnx))
        return Path(result)
