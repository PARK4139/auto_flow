from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def should_i_explorer():
    while 1:
        dialog = PkGui.PkQdialog(prompt="해당위치의 타겟을 exec 할까요", buttons=[YES, NO], input_box_mode=True,
                                     input_box_text_default=get_text_from_clipboard())
        dialog.exec()
        btn_txt_clicked = dialog.btn_txt_clicked
        input_box_text = dialog.input_box.text()
        if btn_txt_clicked == PkTexts.YES:
            pnx = input_box_text
            cmd = rf"explorer {pnx}"
            ensure_command_executed(cmd=cmd, mode="a")
            break
        else:
            break
