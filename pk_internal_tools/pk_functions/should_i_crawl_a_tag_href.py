from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from PIL import Image


def should_i_crawl_a_tag_href():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    while 1:

        url = ""

        dialog = PkGui.PkQdialog(prompt="해당 페이지의 href 를 크롤링할까요", buttons=[YES, NO], input_box_mode=True, input_box_text_default=url)
        dialog.exec()
        btn_txt_clicked = dialog.btn_txt_clicked

        if btn_txt_clicked == PkTexts.YES:
            crawl_html_href(url=dialog.input_box.text())
            break
        else:
            break
