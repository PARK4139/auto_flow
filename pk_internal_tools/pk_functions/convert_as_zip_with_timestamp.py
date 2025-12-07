def convert_as_zip_with_timestamp(f):
    import os
    import traceback
    import logging

    from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
    from pk_internal_tools.pk_functions.ensure_command_executed_like_human_as_admin import ensure_command_executed_like_human_as_admin
    from pk_internal_tools.pk_functions.get_d_working import get_d_working

    starting_d = get_d_working()
    try:
        target_dirname = os.path.dirname(f)
        target_dirname_dirname = os.path.dirname(target_dirname)
        target_basename = os.path.basename(f).split(".")[0]
        target_zip = rf'$zip_{target_basename}.zip'
        target_yyyy_mm_dd_HH_MM_SS_zip = rf'{target_basename} - {get_pk_time_2025_10_20_1159("%Y %m %d %H %M %S")}.zip'
        # logging.debug(rf'# target_dirname_dirname 로 이동')
        os.chdir(target_dirname_dirname)
        # logging.debug(rf'부모d로 백업')
        cmd = f'bandizip.exe c "{target_zip}" "{f}"'
        ensure_command_executed_like_human_as_admin(cmd)
        # logging.debug(rf'이름변경')
        cmd = f'ren "{target_zip}" "$deleted_{target_yyyy_mm_dd_HH_MM_SS_zip}"'
        ensure_command_executed_like_human_as_admin(cmd)
        # logging.debug(rf'부모d에서 백업될 d로 이동')
        cmd = f'move "$deleted_{target_yyyy_mm_dd_HH_MM_SS_zip}" "{target_dirname}"'
        ensure_command_executed_like_human_as_admin(cmd)
        # logging.debug(rf'백업될 d로 이동')
        os.chdir(target_dirname)
        # logging.debug("os.getcwd()")
        # logging.debug(os.getcwd())
        # logging.debug("원본f삭제")
        os.remove(f)
    except:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
    finally:
        logging.debug(rf'프로젝트 d로 이동')
        os.chdir(starting_d)
