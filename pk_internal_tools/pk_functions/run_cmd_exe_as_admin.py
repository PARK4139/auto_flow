def ensure_cmd_exe_as_executed_admin():
    from pk_internal_tools.pk_functions.ensure_command_executed_like_human_as_admin import ensure_command_executed_like_human_as_admin
    import sys
    import traceback
    try:
        while 1:
            # run.exe 관리자모드로 exec
            ensure_command_executed_like_human_as_admin('PowerShell -cmd "Start-Process cmd -Verb RunAs"')

            # 네 클릭
            # f_png=rf"{PROJECT_D}\pk_external_tools\run cmd exe.png"
            # click_center_of_img_recognized_by_mouse_left(img_abspath=f_png)

            # 루프 종료
            break
    except:
        traceback.print_exc(file=sys.stdout)
