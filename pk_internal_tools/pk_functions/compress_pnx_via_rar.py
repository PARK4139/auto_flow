def compress_pnx_via_rar(src, dst, with_timestamp=1):
    import logging
    import os.path
    import traceback
    from datetime import datetime

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.copy_pnx_with_overwrite import copy_pnx_with_overwrite
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_pnxs_move_to_recycle_bin import ensure_pnxs_move_to_recycle_bin
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_n import get_n
    from pk_internal_tools.pk_functions.get_p import get_p
    from pk_internal_tools.pk_functions.get_x import get_x
    from pk_internal_tools.pk_functions.rename_pnx import rename_pnx
    from pk_internal_tools.pk_objects.pk_etc import PK_BLANK
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_d_working import get_d_working
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
    from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    try:

        # todo ensure wsl

        func_n = get_caller_name()

        # 전처리
        # src = get_pnx_windows_style(pnx=src)
        src = get_pnx_unix_style(pnx=src)
        dst = get_pnx_unix_style(pnx=dst)

        # 정의
        d_working = get_d_working()

        pnx = src
        p = get_p(pnx)
        n = get_n(pnx)
        nx = get_nx(pnx)
        x = get_x(pnx)
        x = x.lstrip('.')  # 확장자에서 점 remove

        rar = "rar"  # via rar
        timestamp = ""
        if with_timestamp:
            timestamp = rf"{PK_BLANK}{datetime.now().strftime('%Y %m %d %H %M %S')}"
        pn_rar = rf"{p}/{n}.{rar}"
        dst_nx_rar = rf"{dst}/{n}.{rar}"
        dst_nx_timestamp_rar = rf"{dst}/{n}{timestamp}.{rar}"

        # 로깅
        # logging.debug(rf'''dst="{dst}"  ''')
        # logging.debug(rf'''pnx="{pnx}"  ''')
        # logging.debug(rf'''p="{p}"  ''')
        # logging.debug(rf'''n="{n}"  ''')
        # logging.debug(rf'''nx="{nx}"  ''')
        # logging.debug(rf'''x="{x}"  ''')
        # logging.debug(rf'''dst_nx_rar="{dst_nx_rar}"  ''')
        # logging.debug(rf'''dst_nx_timestamp_rar="{dst_nx_timestamp_rar}"  ''')
        # logging.debug(string = rf'''dst_nx_timestamp_rar="{dst_nx_timestamp_rar}"  ''')

        # 삭제
        ensure_pnxs_move_to_recycle_bin(pnxs=[pn_rar])

        # 생성
        ensure_pnx_made(pnx=dst, mode='d')

        # 이동
        os.chdir(p)

        # 압축
        wsl_pn_rar = get_pnx_wsl_unix_style(pnx=pn_rar)
        cmd = f'wsl rar a "{wsl_pn_rar}" "{nx}"'
        ensure_command_executed(cmd, encoding=PkEncoding.CP949)

        # copy
        copy_pnx_with_overwrite(pnx=pn_rar, dst=dst)

        # rename
        rename_pnx(src=dst_nx_rar, pnx_new=dst_nx_timestamp_rar)

        logging.debug(rf'''wsl_pn_rar="{wsl_pn_rar}"  ''')
        dst_nx = rf"{dst}/{nx}"
        logging.debug(rf'''desktop_nx="{dst_nx}"  ''')

        # remove
        ensure_pnxs_move_to_recycle_bin(pnxs=[dst_nx])
        ensure_pnxs_move_to_recycle_bin(pnxs=[dst_nx_rar])

        # chdir
        os.chdir(d_working)

        # logging
        logging.debug(rf'''dst_nx_rar="{dst_nx_rar}"  ''')
        logging.debug(rf'''[{func_n}] dst_nx_timestamp_rar="{dst_nx_timestamp_rar}"  ''')

        return dst_nx_timestamp_rar
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        ensure_spoken(wait=True)
