import logging


def print_user_input_organized_duplicated_hashed():
    import sys

    import pyautogui
    from PySide6.QtWidgets import QApplication
    import clipboard
    pyautogui.FAILSAFE = False
    q_application = QApplication(sys.argv)
    while 1:
        # input_box_txt_default=""
        input_box_txt_default = "##2025 #2024 #2024 #2024 #2024 #2027 #2025 #hacks#2024 #hacks#2024 #hacks#2024 #hacks#2024 #hacks#2024 #hacks#2024 #hacks #스프레이부스 RC making #압축봉활용 #ORGANIZER #과탄산소다 #커스텀 #diy #DIY #청소 #2027 10 42 스프레이부스 #가구커스텀 #2024 Drawing #2025 건축 #건축커스텀"
        texts = input_box_txt_default.split("#")
        texts_removed_duplication: [str] = []
        dialog = PkGui.PkQdialog(prompt="정리정돈하고 싶은 텍스트를 입력해주세요", buttons=["진행", "종료"], input_box_mode=True,
                                     input_box_text_default=input_box_txt_default)
        dialog.exec()
        btn_txt_clicked = dialog.btn_txt_clicked
        logging.debug(btn_txt_clicked)
        if btn_txt_clicked == "진행":
            user_input = dialog.input_box.text()
            texts = user_input.split("#")
            hashtag_as_year = f'{get_pk_time_2025_10_20_1159("%Y")} '
            texts = [item.replace("##", "#") for item in texts]  # mkr_replace_list_element_each
            texts = [hashtag_as_year] + texts  # mkr_add_element_to_list_as_front_element
            texts = [x for x in texts if x is not None]
            texts = get_list_striped_element(working_list=texts)  # mkr_strip_list_element_each
            texts = [item for item in texts if item and item.strip()]  # mkr_remove_list_element_as_""
            for text in texts:
                if text not in texts_removed_duplication:
                    if text is not None:
                        texts_removed_duplication.append(text)
            texts = texts_removed_duplication
            texts_contained_no = [text for text in texts if any(char.isdigit() for char in text)]
            # texts_contained_no=sorted(texts_contained_no, reverse=False)  # mkr_sort_list_element_by_accend_order
            texts_contained_no = sorted(texts_contained_no, reverse=True)  # mkr_sort_list_element_by_decent_order
            texts_not_contained_no = [text for text in texts if text not in texts_contained_no]
            texts = texts_contained_no + texts_not_contained_no  # 숫자있는 요소를 앞쪽에 배열
            texts = ["#" + item for item in texts]  # mkr_add_prefix_to_list_element_each
            texts = " ".join(texts)  # mkr_convert_from_list_to_str
            print_magenta(f'''texts={texts}''')

            clipboard.copy(texts)
            dialog = PkGui.PkQdialog(prompt=f"클립보드로 붙여넣기 되었습니다", buttons=["닫기"],
                                         auto_click_positive_btn_after_seconds=0)
            dialog.exec()
            raise
        elif btn_txt_clicked == "종료":
            raise
