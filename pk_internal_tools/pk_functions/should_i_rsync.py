from pk_internal_tools.pk_objects.pk_texts import PkTexts


def should_i_rsync():  # todo : chore : wsl rsync 로 교체
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # text_promised=get_text_from_clipboard()
    text_promised = D_PK_PARENT
    while 1:
        dialog = PkGui.PkQdialog(prompt="해당위치의 타겟을 싱크할까요", buttons=[YES, NO], input_box_mode=True,
                                     input_box_text_default=text_promised)
        dialog.exec()
        btn_txt_clicked = dialog.btn_txt_clicked

        # txt_written 에 데이터 저장
        txt_written = dialog.input_box.text()

        # txt_written 데이터 전처리
        # "  C:\projects\services  " ->> "C:\projects\services"
        txt_written = txt_written.strip()
        # "C:\projects\services" ->> C:\projects\services
        if txt_written.startswith("\""):
            if txt_written.endswith("\""):
                txt_written = txt_written.replace("\"", "", 1)
                # txt_written=txt_written[:-(len("\""))] + "${add suffix test}" # 이코드는 add suffix 만들 때 활용하자
                txt_written = txt_written[:-(len("\""))] + ""

        pnx = txt_written
        pnx_todo_sync = rf"{pnx}_sync"
        pnx_todo_sync_zip = rf"{pnx}_sync.zip"

        if btn_txt_clicked == PkTexts.YES:
            copy_pnx_from_local_os_to_remote_os_via_rsync(d_pnx=pnx)
            break
        else:
            break
