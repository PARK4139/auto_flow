from pk_internal_tools.pk_objects.pk_texts import PkTexts


def should_i_crawl_youtube_video_title_and_url():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    while 1:

        # 테스트용
        keyword = 'blahblah'
        url = f'https://www.youtube.com/results?search_query={keyword}'

        dialog = PkGui.PkQdialog(prompt="해당 페이지의 video title, video url을 크롤링할까요", buttons=[YES, NO],
                                     input_box_mode=True, input_box_text_default=url)
        dialog.exec()
        btn_txt_clicked = dialog.btn_txt_clicked

        if btn_txt_clicked == PkTexts.YES:
            crawl_youtube_video_title_and_url(url=dialog.input_box.text())
            break
        else:
            break
