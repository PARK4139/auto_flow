




import logging


def empty_recycle_bin():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # logging
    ensure_command_executed_like_human_as_admin(rf'echo y | del {D_HOME}\AppData\Roaming\Microsoft\Windows\Recent')
    ensure_command_executed_like_human_as_admin('PowerShell.exe -NoProfile -cmd Clear-RecycleBin -Confirm:$false')
    # 휴지통 삭제 (외장하드까지)
    # for %%a in (cdefghijk L mnopqrstuvwxyz) do (
    # 존재하는 경우 %%a:\$RECYCLE.BIN for /f "tokens=* usebackq" %%b in (`"dir /a:d/b %%a:\$RECYCLE.BIN\"`) do rd / q/s "%%a:\$RECYCLE.BIN\%%~b"
    # 존재하는 경우 %%a:\RECYCLER for /f "tokens=* usebackq" %%b in (`"dir /a:d/b %%a:\RECYCLER\"`) do rd /q/s "%% a:\RECYCLER\%%~b"
    # )

    # 가끔 휴지통을 열어볼까요?
    # logging.debug("숨김 휴지통 열기")
    # cmd='explorer c:\$RECYCLE.BIN'
    # run_via_cmd_exe(cmd=cmd)
    # 외장하드 숨김 휴지통 을 보여드릴까요
    # explorer c:\$RECYCLE.BIN
    # explorer d:\$RECYCLE.BIN
    # explorer e:\$RECYCLE.BIN
    # explorer f:\$RECYCLE.BIN

    # speak_ment_experimental(f'휴지통을 비웠습니다', thread_join_mode=True)
    logging.debug(f'''휴지통을 비웠습니다"''')
