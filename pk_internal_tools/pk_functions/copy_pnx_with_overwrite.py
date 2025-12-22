def copy_pnx_with_overwrite(pnx, dst):
    import os

    from pk_internal_tools.pk_functions.compress_pnx_via_bz_exe import compress_pnx_via_bz_exe
    from pk_internal_tools.pk_functions.decompress_f_via_zip import decompress_f_via_zip
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_pnxs_move_to_recycle_bin import ensure_pnxs_move_to_recycle_bin
    from pk_internal_tools.pk_functions.get_n import get_n
    from pk_internal_tools.pk_functions.get_p import get_p

    import logging
    from pathlib import Path

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT

    import shutil
    import traceback

    try:
        # shutil.copy2(pnx, dst)  # shutil.copy2 copies the file and metadata, overwrites if exists # 사용중인 f에 대해서는 권한문제있어서 복사불가한 방식
        # cmd=f'copy "{pnx}" "{dst}"' # d 복사안됨
        # cmd=f'xcopy /E /H /K /Y "{pnx}" "{dst}"'
        # cmd=f'robocopy "{pnx}" "{dst}" /E /Z /R:3 /W:5 /COPYALL /DCOPY:T'
        # cmd=f'robocopy "{pnx}" "{dst}" /E /Z /R:3 /W:5 /COPY:DATSOU /DCOPY:T'
        # cmd=f'runas /user:Administrator robocopy "{pnx}" "{dst}" /E /Z /R:3 /W:5 /COPY:DATSOU /DCOPY:T'
        # cmd=rf'powershell -cmd "Start-Process cmd -ArgumentList \'/c robocopy \"{pnx}\" \"{dst}\" /E /Z /R:3 /W:5 /COPY:DATSOU /DCOPY:T\' -Verb runAs"'
        # cmd=rf'powershell -cmd "Start-Process cmd -ArgumentList \'/c xcopy \\"{pnx}\\" \\"{dst}\\" "'
        # cmd=rf'powershell -cmd "Start-Process cmd -ArgumentList \'/c xcopy \\"{pnx}\\" \\"{dst}\\" /E /H /K /Y\' -Verb runAs"'
        # subprocess.run(cmd, shell=True, check=True)
        # press("enter", interval=0.6)

        if not Path(dst).exists():
            Path(dst).mkdir(parents=True, exist_ok=True)

        pnx = Path(pnx)

        if not pnx.exists():
            logging.debug(f'pnx does not exist: {pnx}')
            return None

        pnx_p = get_p(pnx)  # 원본
        f_zip = pnx_p / f'{get_n(pnx)}.zip'  # 부산물
        f_zip_new = Path(dst) / f"{get_nx(pnx=f_zip)}"  # 부산물
        pnx_new = Path(dst) / get_n(pnx=pnx) # 산출물

        # remove (useless files) (에방차원)
        useless_files = [
            f_zip_new,
            f_zip,
        ]
        for useless_file in useless_files:
            if useless_file.exists():
                ensure_pnxs_move_to_recycle_bin(pnxs=[useless_file])
        if not f_zip_new.exists():
            logging.debug(f'f_zip_new removed {f_zip_new}')

        # compress
        compress_pnx_via_bz_exe(pnx=pnx, f_zip=f_zip)
        if not f_zip.exists():
            logging.debug(f'f_zip does compress failed {f_zip}')
            return None

        # move
        shutil.move(src=f_zip, dst=dst)
        if not f_zip_new.exists():
            logging.debug(f'f_zip_new move failed: {f_zip_new}')
            return None

        # decompress
        decompress_f_via_zip(f_decompressed=f_zip_new)
        if not pnx_new.exists():
            logging.debug(f'pnx_new does compress failed {pnx_new}')
            return None
        if pnx_new.exists():
            logging.debug(f'pnx_new move successfully {pnx_new}')

        # remove (useless files) (부산물 제거)
        useless_files = [
            f_zip,
            f_zip_new,
        ]
        for useless_file in useless_files:
            if useless_file.exists():
                ensure_pnxs_move_to_recycle_bin(pnxs=[useless_file])

        return pnx_new

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
