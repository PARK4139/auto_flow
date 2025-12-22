def run_console_blurred():
    import sys

    import pyautogui
    from PySide6.QtWidgets import QApplication
    while 1:
        pyautogui.FAILSAFE = False

        q_application = QApplication(sys.argv)

        # 프로그램 코어진입 with 프로그램exec 동의요청
        # dialog=PkGui.CustomDialog(q_application=q_application, q_wiget=PkGui.PkQdialog(ment=f"다음의 프로젝트 d에서 자동화 프로그램이 시작됩니다\n{PROJECT_D}", btns=["exec 동의", "exec 하지 않기"], auto_click_positive_btn_after_milliseconds=10), is_app_instance_mode=True)
        # if dialog.btn_txt_clicked == "exec 동의":
        #     print(PROJECT_D)
        #     chdir(PROJECT_D)
        #     run_console_blurred_core_as_scheduler(q_application)
        # if dialog.btn_txt_clicked == "exec 하지 않기":
        #     raise

        # 프로그램 코어진입 without 프로그램exec 동의요청
        window = PkGui.RpaProgramMainWindow(q_application)
        q_application.exec()

        break
