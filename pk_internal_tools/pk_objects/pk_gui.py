import os
import sys
import time
import traceback
from functools import partial
from typing import Callable, TypeVar

import clipboard
import pyautogui
import pynput
from BlurWindow.blurWindow import GlobalBlur
from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QEvent
from PySide6.QtCore import QThread
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QScreen
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QScrollArea, QTextBrowser
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

T = TypeVar('T')


class PkGui:
    class PkQdialog(QDialog):
        """순환참조 를 회피하기 위해서 객체를 복제했다."""

        def update_txt_clicked(self, text_of_clicked_button):
            import logging
            func_n = get_caller_name()
            logging.debug(rf'''%%%FOO%%%''')
            self.txt_clicked = text_of_clicked_button

        def update_txt_clicked_and_close(self, text_of_clicked_button):
            import logging
            from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
            from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV
            func_n = get_caller_name()
            logging.debug(rf'''%%%FOO%%%''')
            #  import play_wav_f
            play_wav_f(f=F_POP_SOUND_POP_SOUND_WAV)
            self.txt_clicked = text_of_clicked_button
            self.close()

        def set_shortcut(self, key_plus_key: str, function):
            import logging
            func_n = get_caller_name()
            logging.debug(rf'''%%%FOO%%%''')
            self.shortcut = QShortcut(QKeySequence(key_plus_key), self)
            self.shortcut.activated.connect(function)

        def __init__(self, prompt: str, buttons=None, parent=None, input_box_mode=False, input_box_text_default="", title="", auto_click_negative_btn_after_milliseconds: int = None, auto_click_positive_btn_after_milliseconds: int = None):
            from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV, F_ICON_PNG, F_GMARKETSANSTTFLIGHT_TTF
            import logging
            from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
            from pk_internal_tools.pk_functions.print_light_black import print_light_black
            from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
            func_n = get_caller_name()

            # log _________ class_name.function()
            class_name = self.__class__.__name__
            logging.debug(rf'''{PK_UNDERLINE}class_name="{class_name}/{func_n}()" %%%FOO%%%''')

            try:
                super().__init__(parent)
                f = F_POP_SOUND_POP_SOUND_WAV
                if os.path.exists(f):
                    #  import play_wav_f
                    play_wav_f(f=f)
                self.input_text_default = input_box_text_default
                self.context = prompt
                self.title = title
                if self.title == "":
                    self.setWindowTitle(".")
                else:
                    self.setWindowTitle(self.title)
                self.is_input_text_box = input_box_mode
                self.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")  # 메시지박스창 스타일시트 적용 설정
                self.setWindowIcon(QIcon(str(F_ICON_PNG)))  # 메시지박스창 아이콘 설정
                self.setAttribute(Qt.WA_TranslucentBackground)  # 메시지박스창 블러 설정
                # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 메시지박스창 최상단 프레임레스 설정
                GlobalBlur(self.winId(), hexColor=False, Acrylic=False, Dark=True, QWidget=self)
                # self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)  # 메시지박스창 최대화 최소화 버튼숨기기
                # self.setWindowFlag(Qt.WindowCloseButtonHint, False)  # 메시지박스창 닫기 버튼 disable
                # self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 모든 창들 중 가장 앞에 메시지박스창 위치하도록 설정
                # self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")  # 메시지박스창 스타일시트 적용 설정

                self.display_width = get_display_info()['width'],
                self.display_height = get_display_info()['height'],
                # self.pop_up_window_width_default = int(int(self.display_width[0]) * 0.4)
                # self.pop_up_window_height_default = int(int(self.display_height[0]) * 0.4)
                # self.resize(self.pop_up_window_width_default, self.pop_up_window_height_default)
                if len(prompt.split("\n")) < 20:
                    # self.resize(500, 250)
                    self.resize(int(self.display_width[0] * 0.3), int(self.display_height[0] * 0.2))
                else:
                    # self.resize(int(500 * 2.5), 250 * 2)
                    # self.resize(int(self.display_width[0] * 0.8), int(self.display_height[0] * 0.6))
                    self.resize(int(self.display_width[0] * 0.4), int(self.display_height[0] * 0.6))
                    # self.resize(int(self.display_width[0] * 0.9), int(self.display_height[0] * 0.6))

                # 창을 화면의 상단가운데로 이동
                screen = QGuiApplication.primaryScreen()
                screen_geometry = screen.availableGeometry()
                center_point = screen_geometry.center()
                self.move(center_point.x() - self.width() / 2, screen_geometry.top() + (center_point.y() * 0.1))

                # pyside6 표준버튼 설정
                # self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                # self.setButtonText(QMessageBox.StandardButton.Ok, "확인", )
                # self.setButton.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                # self.setButtonText(QMessageBox.StandardButton.Cancel, "취소")
                self.txt_clicked = None
                self.layout_horizontal = None
                self.btn_positive = None
                self.btn_negative = None
                self.btn_third = None

                # 스크롤지역 설정
                self.scroll_area = None

                # 버튼 설정
                btn_to_copy = QPushButton(prompt)
                btn_to_copy.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                btn_to_copy.setFocusPolicy(Qt.NoFocus)
                btn_to_copy.clicked.connect(self.copy_label_text_to_clipboard)
                # logging.debug(context=len(contents.strip()))
                if 30 < len(prompt.strip()):
                    # btn_to_copy.setStyleSheet("text-align: left; font-size: 8px")
                    btn_to_copy.setStyleSheet("text-align: left; font-size: 16px")
                else:
                    btn_to_copy.setStyleSheet("text-align: center; font-size: 20px")
                f = F_GMARKETSANSTTFLIGHT_TTF
                if os.path.exists(f):
                    btn_to_copy.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))

                self.set_shortcut(function=self.copy_label_text_to_clipboard, key_plus_key="alt+C")  # 단축키 설정

                self.scroll_area = QScrollArea()
                # self.scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.scroll_area.setWidget(btn_to_copy)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.scroll_area.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.scroll_area.setStyleSheet(" border: none;")
                # if 100 < len(contents):
                # self.scroll_area.setStyleSheet("text-align: center; border: none;")
                # else:
                # self.scroll_area.setStyleSheet("text-align: left; border: none; ")
                self.scroll_area.setFocusPolicy(Qt.NoFocus)  # focus 가 필요 없는 부분에는 이렇게 설정을 해두어야 원하는 곳으로 처음 창이 열렸을 때 focus 되도록 유도할 수 있었다
                # self.scroll_area.setMaximumSize(3000, 1000)

                # 입력 텍스트 박스 설정
                if self.is_input_text_box == True:
                    self.input_box = QLineEdit()
                    self.input_box.setText(self.input_text_default)
                    self.input_box.setFocusPolicy(Qt.StrongFocus)
                    self.input_box.setFocus()  # 창이 나타났을 때 focus 가 다른데 말고 입력 텍스트 박스에 있도록

                if buttons is not None:
                    self.buttons = buttons

                else:
                    self.buttons = [""]
                self.buttons_etc = [None] * (len(self.buttons) - 3)
                try:
                    # 버튼 설정 / 단축키 설정
                    # f = FONTS.RUBIKDOODLESHADOW_REGULAR_TTF
                    f = F_GMARKETSANSTTFLIGHT_TTF
                    # if self.btns[0]:
                    #     self.btn_positive = QPushButton(f'{self.btns[0]} (F1)')
                    #     self.btn_positive.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                    #     self.btn_positive.clicked.connect(partial(self.update_txt_clicked_and_close, self.btns[0]))
                    #     if os.path.exists(pnx=f):
                    #         self.btn_positive.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))
                    #     # self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.btns[0]), key_plus_key="alt+y")  # 단축키 설정
                    #     self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.btns[0]), key_plus_key="F1")  # 단축키 설정
                    # if self.btns[1]:
                    #     self.btn_negative = QPushButton(f'{self.btns[1]} (F2)')
                    #     self.btn_negative.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                    #     self.btn_negative.clicked.connect(partial(self.update_txt_clicked_and_close, self.btns[1]))
                    #     if os.path.exists(pnx=f):
                    #         self.btn_negative.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))
                    #     self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.btns[1]), key_plus_key="F2")  # 단축키 설정
                    # if self.btns[2]:
                    #     self.btn_third = QPushButton(f'{self.btns[2]} (F3)')
                    #     self.btn_third.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                    #     self.btn_third.clicked.connect(partial(self.update_txt_clicked_and_close, self.btns[2]))
                    #     if os.path.exists(pnx=f):
                    #         self.btn_third.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))
                    #     self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.btns[2]), key_plus_key="F3")  # 단축키 설정
                    #
                    # for n, item in enumerate(iterable=self.btns[3:]):
                    #     # 여기서 Unexpected type(s): (int, QPushButton | QPushButton) Possible type(s): (SupportsIndex, None) (slice, Iterable[None]) 이 메세지가
                    #     # self.btns_etc[n]  에서 나타났는데  결국 원인을 찾지 못하였고, n 에 대한 노란밑줄을 무시처리했다.
                    #     self.btns_etc[n] = QPushButton(f'{self.btns[3:][n]}')  # noqa
                    #     self.btns_etc[n].setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")  # noqa
                    #     self.btns_etc[n].clicked.connect(partial(self.update_txt_clicked_and_close, self.btns[3:][n]))  # noqa
                    #     self.btns_etc[n].setFont(Pyside6Util.get_font_for_pyside6(font_path=GMARKETSANSTTFLIGHT_TTF))  # noqa
                    if len(self.buttons) > 0 and self.buttons[0]:
                        self.btn_positive = QPushButton(f'{self.buttons[0]} (F1)')  # 첫번째 버튼은 Positive 버튼
                        self.btn_positive.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                        self.btn_positive.clicked.connect(partial(self.update_txt_clicked_and_close, self.buttons[0]))
                        if os.path.exists(f):
                            self.btn_positive.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))
                        self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.buttons[0]),
                                          key_plus_key="F1")  # 단축키 설정

                    if len(self.buttons) > 1 and self.buttons[1]:
                        self.btn_negative = QPushButton(f'{self.buttons[1]} (F2)')
                        self.btn_negative.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                        self.btn_negative.clicked.connect(partial(self.update_txt_clicked_and_close, self.buttons[1]))
                        if os.path.exists(f):
                            self.btn_negative.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))
                        self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.buttons[1]),
                                          key_plus_key="F2")  # 단축키 설정

                    if len(self.buttons) > 2 and self.buttons[2]:
                        self.btn_third = QPushButton(f'{self.buttons[2]} (F3)')
                        self.btn_third.setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                        self.btn_third.clicked.connect(partial(self.update_txt_clicked_and_close, self.buttons[2]))
                        if os.path.exists(f):
                            self.btn_third.setFont(Pyside6Util.get_font_for_pyside6(font_path=f))
                        self.set_shortcut(function=partial(self.update_txt_clicked_and_close, self.buttons[2]),
                                          key_plus_key="F3")  # 단축키 설정

                    for n, item in enumerate(self.buttons[3:]):
                        self.buttons_etc[n] = QPushButton(f'{item}')
                        self.buttons_etc[n].setStyleSheet("background-color: rgba(0, 0, 0, 0);  color: white;")
                        self.buttons_etc[n].clicked.connect(partial(self.update_txt_clicked_and_close, item))
                        self.buttons_etc[n].setFont(
                            Pyside6Util.get_font_for_pyside6(font_path=F_GMARKETSANSTTFLIGHT_TTF))

                except:

                    print_light_black(f"{traceback.format_exc()}")

                # except IndexError:
                #     # btns=[]의 index 를 초과하거나 부족한 경우
                #     pass
                # except TypeError:
                #     # btns=None 인 경우
                #     pass

                # 타이머에 의한 자동 버튼 클릭 설정
                # 밀리초를 초로 변환
                from pk_internal_tools.pk_functions.get_seconds_from_milliseconds import get_seconds_from_milliseconds

                if auto_click_negative_btn_after_milliseconds is not None:
                    self.seconds_remaining_until_auto_click = get_seconds_from_milliseconds(auto_click_negative_btn_after_milliseconds)
                    self.is_closing_timer = True
                else:
                    self.is_closing_timer = False
                if auto_click_positive_btn_after_milliseconds is not None:
                    self.seconds_remaining_until_auto_click = get_seconds_from_milliseconds(auto_click_positive_btn_after_milliseconds)
                    self.is_starting_timer = True
                else:
                    self.is_starting_timer = False
                # print(rf'self.is_closing_timer : {self.is_closing_timer}')
                # print(rf'auto_closing_milliseconds : {auto_click_negative_btn_after_milliseconds}')
                # print(rf'self.is_starting_timer : {self.is_starting_timer}')
                # print(rf'auto_starting_milliseconds : {auto_click_positive_btn_after_milliseconds}')
                if self.is_closing_timer == True and self.is_starting_timer == True:
                    ensure_printed_as_gui("closing_timer 와 starting_timer 는 동시에 설정 할 수 없습니다")
                    return

                if self.is_closing_timer == True or self.is_starting_timer == True:
                    self.auto_choice_timer = QTimer()
                    if auto_click_negative_btn_after_milliseconds is not None:
                        self.auto_choice_timer.timeout.connect(self.countdown_and_click_negative_btn)  # noqa
                    elif auto_click_positive_btn_after_milliseconds is not None:
                        self.auto_choice_timer.timeout.connect(self.countdown_and_click_positive_btn)  # noqa
                    self.auto_choice_timer.start(1000)

                # 레이아웃 설정
                self.layout_horizontal = QGridLayout()
                logging.debug(rf'''self.btns="{self.buttons}" %%%FOO%%%''')
                logging.debug(rf'''len(self.btns)="{len(self.buttons)}" %%%FOO%%%''')
                try:
                    if len(self.buttons) > 0 and self.buttons[0]:  # btns 리스트의 길이가 0보다 크고, 첫 번째 요소가 True인 경우
                        self.layout_horizontal.addWidget(self.btn_positive, 0, 0)
                    if len(self.buttons) > 1 and self.buttons[1]:  # btns 리스트의 길이가 1보다 크고, 두 번째 요소가 True인 경우
                        self.layout_horizontal.addWidget(self.btn_negative, 0, 1)
                    if len(self.buttons) > 2 and self.buttons[2]:  # btns 리스트의 길이가 2보다 크고, 세 번째 요소가 True인 경우
                        self.layout_horizontal.addWidget(self.btn_third, 0, 2)
                    try:
                        for n, item in enumerate(iterable=self.buttons_etc):
                            self.layout_horizontal.addWidget(self.buttons_etc[n], 0, n + 3)
                    except:
                        print_light_black(f"{traceback.format_exc()}")
                except:
                    print_light_black(f"{traceback.format_exc()}")

                layout_vertical = QVBoxLayout()
                # if len(contents.split("\n")) < 10:
                #     layout_vertical.addWidget(self.label)
                # else:
                layout_vertical.addWidget(self.scroll_area)
                if input_box_mode:
                    layout_vertical.addWidget(self.input_box)
                layout_vertical.addLayout(self.layout_horizontal)
                self.setLayout(layout_vertical)

                self.bring_this_window()
            except:
                print_light_black(f"{traceback.format_exc()}")

        # deprecating test
        # def centerOnScreen(self):
        #     # 현재 화면의 가운데 좌표를 계산
        #     screen_geometry = QScreen().geometry()
        #     x = (screen_geometry.width() - self.width()) // 2
        #     y = (screen_geometry.height() - self.height()) // 2
        #     self.move(x, y)

        def copy_label_text_to_clipboard(self):
            from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
            from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV
            clipboard.copy(self.context)
            f = F_POP_SOUND_POP_SOUND_WAV
            if os.path.exists(f):
                #  import play_wav_f
                play_wav_f(F_POP_SOUND_POP_SOUND_WAV)

        def countdown_and_click_positive_btn(self):
            from pk_internal_tools.pk_functions.get_minuites_and_remaining_secs import get_minuites_and_remaining_secs
            mins, secs_remaining = get_minuites_and_remaining_secs(seconds=self.seconds_remaining_until_auto_click)
            if secs_remaining != 0:
                secs_remaining_with_unit = f"{secs_remaining}초"
            else:
                secs_remaining_with_unit = ""
            if mins != 0:
                mins_with_unit = f"{mins}분"
            else:
                mins_with_unit = ""
            self.btn_positive.setText(f"{self.buttons[0]} ({mins_with_unit} {secs_remaining_with_unit} 뒤 자동클릭)")

            if self.seconds_remaining_until_auto_click == 0:
                if self.buttons[0]:
                    self.update_txt_clicked_and_close(self.buttons[0])
            self.seconds_remaining_until_auto_click = self.seconds_remaining_until_auto_click - 1

        def countdown_and_click_negative_btn(self):
            from pk_internal_tools.pk_functions.get_minuites_and_remaining_secs import get_minuites_and_remaining_secs
            #  import get_minuites_and_remaining_secs
            mins, secs_remaining = get_minuites_and_remaining_secs(seconds=self.seconds_remaining_until_auto_click)
            if secs_remaining != 0:
                secs_remaining_with_unit = f"{secs_remaining}초"
            else:
                secs_remaining_with_unit = ""
            if mins != 0:
                mins_with_unit = f"{mins}분"
            else:
                mins_with_unit = ""
            self.btn_negative.setText(f"{self.buttons[1]} ({mins_with_unit} {secs_remaining_with_unit} 뒤 자동클릭)")

            if self.seconds_remaining_until_auto_click == 0:
                if self.buttons[1]:
                    self.update_txt_clicked_and_close(self.buttons[1])
            self.seconds_remaining_until_auto_click = self.seconds_remaining_until_auto_click - 1

        def bring_this_window(self):
            # self.activateWindow() 와 self.show() 의 위치는 서로 바뀌면 의도된대로 동작을 하지 않는다
            self.show()
            self.activateWindow()
            # active_window = win32gui.GetForegroundWindow()
            # win32gui.SetForegroundWindow(active_window)

    class CustomDialog():
        def __init__(self, q_application: QApplication, q_wiget: QWidget, is_app_instance_mode=False, is_exec_mode=True):
            import logging
            from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
            from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV
            func_n = get_caller_name()
            logging.debug(rf'''%%%FOO%%%''')
            """
            이 함수는 특별한 사용요구사항이 있습니다
            pyside6 앱 내에서 해당 함수를 호출할때는 is_app_instance_mode 를 파라미터에 넣지 않고 쓰는 것을 default 로 디자인했습니다.
            pyside6 앱 밖에서 해당 함수를 호출할때는 is_app_instance_mode 를 True 로 설정하고 쓰십시오.

            해당 사용요구사항이 생기게 된 이유는 다음과 같습니다
            pyside6 는 app을 singletone으로 instance를 구현합니다. 즉, instance는 반드시 pyside6 app 내에서 하나여야 합니다.
            pyside6의 QApplication()이 앱 내/외에서도 호출이 될 수 있도록 디자인했습니다.
            앱 내에서 호출 시에는 is_app_instance_mode 파라미터를 따로 설정하지 않아도 되도록 디자인되어 있습니다.
            앱 외에서 호출 시에는 is_app_instance_mode 파라미터를 True 로 설정해야 동작하도록 디자인되어 있습니다.
            앱 외에서 호출 시에는 반드시 CustomDialog() 인스턴스로 close()를 호출해 pyside6 app instance 를 종료 해야 합니다.
            """
            # 테스트 해보니, QApplication가 먼저 생성된 뒤에 QDialog 는 instance 가 생성되어야 하는 것같다.
            # 그래서 QDialog instance 를 CustomDialog 생성자의 파라미터로 못받는 것 같다.
            # 다른 Qwiget 을 받을 생각 이었는데...
            # 갑자기 든 생각인데. QApplication 도 같이 넘겨주면 되지 않을까?
            # 된다! 내 생각이 맞은 것 같다. QApplicaion() QDialog() 인스턴스의 생성순서만 바꿨는데 동작하지 않는다. 아무튼 QDialog 를 instance 인자로 받을 수 있다.
            f = F_POP_SOUND_POP_SOUND_WAV
            if os.path.exists(f):
                #  import play_wav_f
                play_wav_f(f=F_POP_SOUND_POP_SOUND_WAV)

            self.is_app_instance_mode = is_app_instance_mode
            if is_app_instance_mode == True:
                self.app_instance = q_application
            # if is_exec_mode == False:
            #     global dialog
            dialog = q_wiget
            if is_exec_mode == True:
                dialog.exec()  # noqa
            self.txt_clicked = dialog.txt_clicked  # noqa

        def close(self):
            if self.is_app_instance_mode == True:
                if isinstance(self.app_instance, QApplication):
                    self.app_instance.exec()
            if self.is_app_instance_mode == True:
                # self.app_instance.quit()  # QApplication 인스턴스 quit 시도 : fail
                self.app_instance.shutdown()  # QApplication 인스턴스 shutdown 시도 : success  # 성공요인은 app.shutdown()이 호출이 되면서 메모리를 해제까지 수행해주기 때문
                # del self.app_instance  # QApplication 인스턴스 del 시도 : fail
                # self.app_instance.deleteLater()  # QApplication delete later 시도 : fail
                # self.app_instance = None  # QApplication 인스턴스 None 시도 : fail
                # sys.exit()

    class RpaProgramMainWindow(QWidget):
        # class RpaProgramMainWindow(QDialog):
        # class RpaProgramMainWindow(QMainWindow):
        # def __init__(self, shared_obj): # shared_obj 는 창간 통신용 공유객체 이다. pyside6 app 의 상태관리
        def __init__(self, q_application):
            import logging
            from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
            from pk_internal_tools.pk_objects.pk_directories import d_pk_root
            from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
            from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV
            func_n = get_caller_name()
            logging.debug(rf'''%%%FOO%%%''')

            f = F_POP_SOUND_POP_SOUND_WAV
            if os.path.exists(f):
                #  import play_wav_f
                play_wav_f(f=f)
            super().__init__()
            self.app = q_application

            # deprecated test started at 2023 12 23 01 28
            # self.prompt_window = None
            # self.sub_window = None
            # self.question = None

            #  앱 전역 변수 설정
            self.text = "text"
            self.pw = "`"
            self.id = "`"
            # self.is_window_maximized = False
            self.display_width = get_display_info()['width'],
            self.display_height = get_display_info()['height'],
            # self.display_width_default = int(int(self.display_width[0]) * 0.106)
            # self.display_width_default = int(int(self.display_width[0]) * 0.045)
            # self.display_width_default = int(int(self.display_width[0]) * 0.02)
            self.display_width_default = int(int(self.display_width[0]) * 0.01)
            self.display_height_default = int(int(self.display_height[0]) * 0.2)

            #  메인창 설정
            self.setWindowTitle('.')
            icon_png = rf"{d_pk_root}\pk_external_tools\icon.PNG"
            self.setWindowIcon(QIcon(icon_png))  # 메인창 아이콘 설정
            # self.setAttribute(Qt.WA_TranslucentBackground) # 메인창 블러 설정
            # self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 메인창 최상단 프레임레스 설정
            GlobalBlur(self.winId(), hexColor=False, Acrylic=False, Dark=True, QWidget=self)
            self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)  # 최대화 최소화 버튼 숨기기
            self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 모든 창 앞에 위치하도록 설정
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
            # self.setStyleSheet(pyqt6css.qss)
            # self.setAttribute(Qt.WA_TranslucentBackground)
            # blur(self.winId())
            # self.scale = 1/1
            # self.scale = 1/2
            # self.scale = 1/3
            # self.scale = 1 / 4
            # self.scale = 1 / 10
            # self.setGeometry(0, 0, int(self.display_width_default * self.scale), int(self.display_height_default * self.scale))
            # self.setGeometry(0, 0,self.display_width_default, self.display_height_default)
            # self.resize(self.display_width_default, self.display_height_default)

            # self.setGeometry(0, 0, int(self.display_width_default * self.scale), int(self.display_height[0]))
            self.windows_size_mode = 1  # 창크기 모드 설정  #0 ~ 3
            QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 고해상도 스케일링을 활성화합니다.
            self.screens = QGuiApplication.screens()  # 사용 가능한 모든 화면을 가져옵니다.

            # inputbox 설정
            # self.inputbox = QLineEdit(self)
            # self.inputbox.setStyleSheet("color: rgba(255,255,255, 0.9);")
            # self.inputbox.setText("0,0")
            # self.inputbox.setFixedWidth(120)
            # # self.inputbox.setStyleSheet("text-shadow: 1px 1px 7px rgba(1, 1, 1, 1);") #텍스트에 그림자 넣고 싶었는데 안된다.
            # self.inputbox.textChanged.connect(self.inputbox_changed)
            # self.inputbox.editingFinished.connect(self.inputbox_edit_finished)
            # self.inputbox.returnPressed.connect(self.inputbox_return_pressed)

            # 이벤트 가 많으면 프로그램이 늦어지는 것 같아보였다

            # monitor_mouse_position 이벤트 설정
            # self.listener = pynput.mouse.Listener(on_move=self.monitor_mouse_position) # 아주 빠르게 마우스 움직임 감지
            # self.listener.start()

            # monitor_mouse_position_per_second 이벤트 설정 (마우스 멈춤 감지 이벤트/ 5초간 마우스 중지 시 메인화면 자동 숨김 이벤트)
            self.mouse_positions = []
            self.previous_position = None
            self.current_position = None
            self.timer = QTimer()
            self.timer.timeout.connect(self.monitor_mouse_position_per_second)  # noqa
            self.timer.start(1000)

            # mkr_단축키 설정
            self.available_shortcut_list = {
                # 버튼있는 SHORCUT #단축키 설정 #CODE RELATIONAL AREA 1/5
                'HIDE': 'Esc',  # GHOST MODE?
                'EXIT': 'Q',
                'BACK UP TARGET': 'S',
                'ASK AI QUESTION': 'A',
                'SHOOT SCREENSHOT FULL': 'F',
                'SHOOT SCREENSHOT CUSTOM': 'C',
                'SHOOT SCREENSHOT FOR RPA': '4',
                'ANI': '5',  # nyaa.si
                'EXPLORER': 'O',
                'SYNC SERVICES': '`',
                'TEST': '1',
                'BACKUP SERVICES': '2',  # BACK UP TARGET 인데, 버튼 지우게 되면 이걸로
                'PROJECT DIRECTORY': 'P',
                "CLASSIFY SPECIAL FILES": "F2",
                "GATHER EMPTY DIRECTORY": "F3",
                "GATHER SPECIAL FILES": "F4",
                "GATHER USELESS FILES": "F5",
                "MERGE DIRECTORIES": "F6",
                "CONVERT MKV TO WAV": "F7",
                'DOWNLOAD YOUTUBE(webm)': 'F8',
                'DOWNLOAD YOUTUBE(webm)_': 'F9',
                'DOWNLOAD VIDEO FROM WEB1': 'Alt+F1',
                'DOWNLOAD VIDEO FROM WEB2': 'Alt+F2',
                'ROTATE WINDOW MODE': 'Alt+W',
                'SYSTEM REBOOT': 'Alt+9',
                'SYSTEM SHUTDOWN': 'Alt+]',
                'SYSTEM POWER SAVING MODE': 'Alt+[',
                # 'LOGIN': 'Alt+F7',
                'EMPTY RECYCLE BIN': 'Alt+E',
                # 'RUN CMD.EXE AS ADMIN': 'Alt+C',
                'NAVER MAP': 'Alt+N',
                # 'WEB CRAWL HREF': "`+F1", # fail
                'WEB CRAWL HREF': "Ctrl+F1",
                'WEB CRAWL YOUTUBE VIDEO TITLE AND URL': "Ctrl+F2",
                'WEB CRAWL YOUTUBE VIDEO PLAYLIST': "Ctrl+F3",
                'rdp-82106': 'R+1',
                # 'DOWNLOAD YOUTUBE(wav)': 'S',
                # 'DOWNLOAD YOUTUBE(webm) ONLY SOUND': 'Alt+S',

            }

            # 버튼없는 SHORCUT #단축키 설정 #shortcut #mkr2024
            self.set_shortcut('TEST', self.should_i_start_test)
            self.set_shortcut('BACK UP TARGET', self.should_i_back_up_target)

            # 버튼있는 버튼
            # self.btn_to_open_PROJECT_D = self.get_btn(self.get_btn_name_promised('PROJECT DIRECTORY'), self.open_PROJECT_D)

            # 버튼있는 단축키
            # self.btn_to_open_PROJECT_D_only_shortcut_name = self.get_btn(btn_text_align="right", btn_name=self.get_shortcut_name_promised('PROJECT DIRECTORY'), function=self.open_PROJECT_D)
            # self.btn_to_back_up_target_only_shortcut_name = self.get_btn(btn_text_align="right", btn_name=self.get_shortcut_name_promised('BACK UP TARGET'), function=self.should_i_back_up_target)

            print(f'{PK_UNDERLINE}단축키')
            temp = ''
            for key in self.available_shortcut_list:
                value = self.available_shortcut_list[key]
                print(f'{value}         {key}')
                temp = temp + '\n' + f'{value}         {key}'

            # 레이블로 설정
            html = f"<html><body><h1 style='color: white;'>{temp}</h1></body></html>"
            text_browser = QTextBrowser()
            text_browser.setHtml(html)
            text_browser.resize(800, 600)

            text_browser2 = QTextBrowser()
            text_browser2.setHtml(html)
            text_browser2.resize(800, 600)

            text_browser3 = QTextBrowser()
            text_browser3.setHtml(html)
            text_browser3.resize(800, 600)

            text_browser4 = QTextBrowser()
            text_browser4.setHtml(html)
            # text_browser4.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")  # 메시지박스창 스타일시트 적용 설정
            text_browser4.resize(800, 600)

            # btns 설정 5/5
            btns = [
                # [text_browser, text_browser2],  # BLANK #여백
                # [text_browser3, text_browser4], #BLANK #여백
                # [self.btn_to_should_i_exit_this_program, self.btn_to_should_i_exit_this_program_only_shortcut_name],
                # [self.btn_to_toogle_rpa_window, self.btn_to_toogle_rpa_window_only_shorcut_name],
                # [self.btn_to_rotate_window_size_mode, self.btn_to_rotate_window_size_mode_only_shortcut_name],
                # [self.btn_to_should_i_empty_trash_can, self.btn_to_should_i_empty_trash_can_only_shortcut_name],
                # [self.btn_to_should_i_enter_to_power_saving_mode, self.btn_to_should_i_enter_to_power_saving_mode_only_shortcut_name],
                # [self.btn_to_classify_special_files, self.btn_to_classify_special_files_only_shortcut_name],
                # [self.btn_to_gather_empty_directory, self.btn_to_gather_empty_directory_only_shortcut_name],
                # [self.btn_to_merge_directories, self.btn_to_merge_directories_only_shortcut_name],
            ]

            # GRID SETTING
            grid = QtWidgets.QGridLayout(self)

            # GRID COORDINATION REFERENCE (ROW, COLUMN)
            #        0,0  0,1  0,2
            #        1,0  1,1  1,2
            #        2,0  2,1  2,2

            # spaver

            # GRID_COLUMN 1 폭 조절용 policy
            # size_policy = QSizePolicy()
            # grid.setHorizontalPolicy(QSizePolicy.Minimum)  # 그리드의 열의 폭을 최소로 설정합니다.
            grid.setVerticalSpacing(9)
            grid.setHorizontalSpacing(5)
            grid.setColumnMinimumWidth(1, 125)
            grid.setColumnMinimumWidth(2, 45)

            btns_grid = btns
            line_no = 0
            for btn in btns_grid:
                grid.addWidget(btn[0], line_no, 0)  # GRID_COLUMN 0 설정
                grid.addWidget(btn[1], line_no, 2)  # GRID_COLUMN 1 설정
                line_no = line_no + 1

            # 화면exec
            def do_once():
                self.rotate_window_size_mode()
                self.timer2.stop()

            self.timer2 = QTimer()
            self.timer2.timeout.connect(do_once)  # noqa
            # self.timer2.start(500)
            self.timer2.start(50)

            # TEST
            # self.inputbox = QPlainTextEdit(self)
            # self.inputbox = QTextEdit(self)
            # self.ta1 = QTableWidget(self)
            # self.ta1.resize(500, 500)
            # self.ta1.setColumnCount(3)
            # self.ta1.setStyleSheet("color: rgba(255,255,255, 0.9);")
            # self.ta1.setStyleSheet("background-color: rgba(255,255,255, 0.9);")
            # table_column = ["첫번째 열", "두번째 열", "Third 열"]
            # self.ta1.setHorizontalHeaderLabels(table_column)

            # # 행 2개 추가
            # self.ta1.setRowCount(2)

            # # 추가된 행에 데이터 채워넣음
            # self.ta1.setItem(0, 0, QTableWidgetItem("(0,0)"))
            # self.ta1.setItem(0, 1, QTableWidgetItem("(0,1)"))
            # self.ta1.setItem(1, 0, QTableWidgetItem("(1,0)"))
            # self.ta1.setItem(1, 1, QTableWidgetItem("(1,1)"))

            # 마지막에 행 1개추가
            # self.ta1.insertRow(2)
            # self.ta1.setItem(2, 0, QTableWidgetItem("New Data"))

            # 셀의 텍스트 변경
            # self.ta1.item(1, 1).setText("데이터 변경")

            # 셀에 있는 텍스트 출력
            # print(self.ta1.item(0, 1).text())

            # 테이블 데이터 전부 삭제
            # self.ta1.clear()

            # 테이블 행전부 삭제
            # self.ta1.setRowCount(0)

            self.scroll_area = QScrollArea()
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.scroll_area.setStyleSheet(f" border: none; width: {self.display_width_default}px; height: {self.display_height_default}px")
            self.scroll_area.setLayout(grid)

            # 레이아웃 설정
            layout = QVBoxLayout(self)
            layout.addWidget(self.scroll_area)

            self.setMouseTracking(True)  # pyside6 창 밖에서도 마우스 추적 가능 설정 # 마우스 움직임 이벤트 감지 허용 설정
            # self.toogle_rpa_window()
            # press("alt", "w")

            self.move_pyside6_window_to_front()

            self.txt_clicked = "foo"

            # self.event_loop = QEventLoop()
            # self.event_loop.exec()

            # self.exec()

        def monitor_mouse_position_per_second(self):

            """마우스 움직임 감지 함수"""
            x, y = pyautogui.position()  # 현재 마우스 위치 ( 이게 내가 원하던 수치 )
            # print(x, y)
            self.current_position = QCursor.pos()  # 현재 마우스 커서 위치 ( 이건 내가 원하는 수치는 아닌데... 뭘 의미하는 거지? )
            # print(self.current_position)
            if self.previous_position is not None and self.previous_position == self.current_position:
                # print("마우스가 멈췄습니다")
                # print(f"self.mouse_positions : {self.mouse_positions}") # 마우스 위치 리스트
                if 10 <= len(self.mouse_positions):
                    # 10번 연속 mouse 중지 감지
                    # self.mouse_positions 에 등록된 모든 self.current_position 가 동일하면 10번 연속으로 움직이지 않은 것으로 판단
                    if len(self.mouse_positions) == 10:
                        # 동일한 10개 원소를 갖는 리스트 내에서 요소의 중복을 제거하면 중복이 제거된 리스트의 요소의 수는 1개가 나올 것을 기대
                        mouse_positions_removed_duplicatd_elements = list(set(self.mouse_positions))  # orderless way
                        if len(mouse_positions_removed_duplicatd_elements) == 1:
                            # print("10번 연속 중지 감지")
                            self.hide()
                            pass

                if 5 <= len(self.mouse_positions):
                    self.mouse_positions = []  # 감지값들이 5개 이상이면 감지값목록 초기화

                elif len(self.mouse_positions) < 5:
                    self.mouse_positions.append(self.current_position)
                pass
            else:
                pass
                # print("마우스가 움직였습니다")

                # mkr_우측하단 꼭지점 부근 네비게이션
                # if 3440 - 25 <= x and 1440 - 25 <= y:
                #     press("win", "d"5)

                # 우측 네비게이션
                # if 3440 - 50 <= x <= 3440 and 300 <= y <= 1440:
                #     try:
                #         open_pnx(PYCHARM64_EXE)
                #     except:
                #         print_light_black(f"{traceback.format_exc()}")
                #         pass

                # 좌측 네비게이션
                # elif 0 <= x <= 15 and 0 <= y <= 1440:
                #     self.toogle_rpa_window()
                #     pass

                # else:
                #     pass
            self.previous_position = self.current_position

        def monitor_mouse_position(self, x, y):
            # 상단 네비게이션
            if 0 <= x <= 3440 and 0 <= y <= 25:
                pass
            else:
                pass

        @staticmethod
        # def rpa_program_method_decorator(function):
        def rpa_program_method_decorator(function: Callable[[T], None]):
            def wrapper(self):
                from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
                from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV
                f = F_POP_SOUND_POP_SOUND_WAV
                if os.path.exists(f):
                    #  import play_wav_f
                    play_wav_f(f=f)
                self.hide()  # 비동기 전까지는 사용자가 다른 명령을 하지 못하도록 이 코드를 사용
                function(self)
                self.move_pyside6_window_to_front()

            return wrapper

        def eventFilter(self, obj, event):
            # if event.type() == QEvent.MouseMove:
            #     x = event.globalX()
            #     y = event.globalY()
            #     print(f"마우스 이동 - X: {x}, Y: {y}")
            # return super().eventFilter(obj, event)
            if event.type() == QEvent.MouseButtonPress and not self.rect().contains(event.pos()):
                print("pyside6 창 외부 클릭 되었습니다")
            return super().eventFilter(obj, event)

        def mousePressEvent(self, e):
            if e.button() == Qt.LeftButton:  # 왼쪽 버튼 클릭 시 동작
                # print(f"mouse press event monitor: LeftButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
                pass
            elif e.button() == Qt.RightButton:
                print(f"mouse press event monitor: RightButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.BackButton:
                print(f"mouse press event monitor: BackButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton1:
                print(f"mouse press event monitor: ExtraButton1 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton10:
                print(f"mouse press event monitor: ExtraButton10 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton11:
                print(f"mouse press event monitor: ExtraButton11 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton12:
                print(f"mouse press event monitor: ExtraButton12 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton13:
                print(f"mouse press event monitor: ExtraButton13 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton14:
                print(f"mouse press event monitor: ExtraButton14 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton15:
                print(f"mouse press event monitor: ExtraButton15 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton16:
                print(f"mouse press event monitor: ExtraButton16 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton17:
                print(f"mouse press event monitor: ExtraButton17 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton18:
                print(f"mouse press event monitor: ExtraButton18 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton19:
                print(f"mouse press event monitor: ExtraButton19 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton2:
                print(f"mouse press event monitor: ExtraButton2 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton20:
                print(f"mouse press event monitor: ExtraButton20 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton21:
                print(f"mouse press event monitor: ExtraButton21 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton22:
                print(f"mouse press event monitor: ExtraButton22 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton23:
                print(f"mouse press event monitor: ExtraButton23 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton24:
                print(f"mouse press event monitor: ExtraButton24 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton3:
                print(f"mouse press event monitor: ExtraButton3 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton4:
                print(f"mouse press event monitor: ExtraButton4 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton5:
                print(f"mouse press event monitor: ExtraButton5 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton6:
                print(f"mouse press event monitor: ExtraButton6 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton7:
                print(f"mouse press event monitor: ExtraButton7 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton8:
                print(f"mouse press event monitor: ExtraButton8 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ExtraButton9:
                print(f"mouse press event monitor: ExtraButton9 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.ForwardButton:
                print(f"mouse press event monitor: ForwardButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.LeftButton:
                print(f"mouse press event monitor: LeftButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.MiddleButton:
                print(f"mouse press event monitor: MiddleButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.NoButton:
                print(f"mouse press event monitor: NoButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.TaskButton:
                print(f"mouse press event monitor: TaskButton pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.XButton1:
                print(f"mouse press event monitor: XButton1 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")
            elif e.button() == Qt.XButton2:
                print(f"mouse press event monitor: XButton2 pressed at {str(e.pos().x())} ,{str(e.pos().y())} ")

        # def mouseReleaseEvent(self, e):
        #     self.label10.setText(f"event monitor:\nmouseReleaseEvent : {str(e.pos().x())} ,{str(e.pos().y())} ")
        #
        # def mouseDoubleClickEvent(self, e):
        #     self.label10.setText(f"event monitor:\nmouseDoubleClickEvent : {str(e.pos().x())} ,{str(e.pos().y())} ")

        def keyPressEvent(self, e):
            self.mouse_positions = []  # 키보드가 눌리면 사용자가 사용중인 것으로 간주하고 마우스 위치 값 목록 초기화

        # def keyPressEvent(self, e):
        #     # these keys refered from https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html
        #     # 테스트 결과 한/영, 한자 인식안됨.
        #     if e.key() == Qt.Key_Return:
        #         self.label11.setText(f"keyboard event monitor:\nKey_Return : Key_Return ")
        #         self.showMinimized()
        #         press("space")
        #         self.showMaximized()
        #     elif e.key() == Qt.Key_0:
        #         self.label11.setText(f"keyboard event monitor:\nKey_0 : Key_0 ")
        # deprecated test
        # def inputbox_changed(self):
        #     logging.debug("inputbox 텍스트 change event 감지 되었습니다")
        #     print(self.inputbox.ment())
        #
        # def inputbox_edit_finished(self):
        #     logging.debug("inputbox edit finish event 감지 되었습니다")
        #
        # def inputbox_return_pressed(self):
        #     logging.debug("inputbox return pressed event 감지 되었습니다")

        def get_btn_name_with_shortcut_name(self, button_name_without_shortcut):
            # 버튼명과 shourtcut 명을 을 적당한 간격으로 띄워서 string 으로 반환하는 코드, 폰트 가 고정폭폰트 가 아니면 무용지물인 함수
            numbers = []
            for key, value in self.available_shortcut_list.items():
                numbers.append(len(value) + len(key))
            max_len_value = max(numbers)
            button_name_with_short_cut = ""
            for key, value in self.available_shortcut_list.items():
                if key == button_name_without_shortcut:
                    space_between = " " * (max_len_value - len(key) - len(value) + 1)
                    # space_between = "\t"
                    # button_name_with_short_cut = button_name_with_short_cut + f"{key}{space_between}{value}".strip()
                    # button_name_with_short_cut = button_name_with_short_cut + f"{key}{space_between}( {value} )".strip()
                    button_name_with_short_cut = button_name_with_short_cut + f"{value}{space_between}( {key} )".strip()
            print(button_name_with_short_cut)
            return button_name_with_short_cut

        def get_btn_name_promised(self, button_name_without_shortcut):
            button_name_with_short_cut = ""
            for key, value in self.available_shortcut_list.items():
                if key == button_name_without_shortcut:
                    button_name_with_short_cut = button_name_with_short_cut + f"{key}".strip()
            return button_name_with_short_cut

        def get_shortcut_name_promised(self, button_name_without_shortcut):
            button_name_with_short_cut = ""
            for key, value in self.available_shortcut_list.items():
                if key == button_name_without_shortcut:
                    button_name_with_short_cut = button_name_with_short_cut + f"{value}".strip()
            return button_name_with_short_cut

        # def show_available_shortcut_list(self):
        #     # global max
        #     # global 을 설정하면, 이 변수는 함수의 exec 이 끝난 다음에도 없어지지 않는다.
        #     # 이 값을 나중에 함수 끝나고도 또 쓸려면 이렇게 쓰면 되겠다. @staticmethod 의 경우에는 변수 간의 값에 간섭이 되지 않도록 굳이 쓰지 않는 것이 좋겠다.
        #     # global 많이 쓰면 이는 변수가 전역화 되니까 메모리의 성능이 저하되는 것이 아닐까?
        #     # 그렇다면 함수 내에서만 전역적으로 변수를 쓰는 경우에, global 을 쓰지 않는 것이 성능을 위해서는 좋은 선택이겠다. 굳이 함수가 끝난 뒤에 밖에서 써야한다면 global 을 써야 겠지만, 나는 무척이나 이게 헷갈릴 것 같다
        #     # 그동안의 경험으로는 코드 맥락 상, global 선언을 하지 않아도 전역변수 처럼 작동 되는 것 같아 보인다.... 아니다 이게 global max 를 선언하지 않았다고 가정하면 max 는 show_available_shortcut_list() 가 종료되면 max 는 사라진다. 그런데 global max를 선언하면 max 는 유지된다!
        #     # 혹시 객체의 인스턴스 같은 것을 global 을 통해서 변수에 저장하고 쓰면 싱글톤 처럼 쓸 수 있는 것일까? 메모리 효율은 많이 나빠질까?
        #
        #     numbers = []
        #     for key_shortcut, value in self.available_shortcut_list.items():
        #         numbers.append(len(value))
        #     max_no: int
        #     max_no = max(numbers)
        #     for key_shortcut, value in self.available_shortcut_list.items():
        #         print(f"{{0: <{max_no}}} : {key_shortcut}".format(value))

        def rotate_window_size_mode(self):
            if self.windows_size_mode == 0:
                self.resize(self.display_width_default, self.display_height_default)
                self.move_window_to_center()  # 불필요 하면 주석하는 게 나쁘지 않겠다
                self.windows_size_mode = self.windows_size_mode + 1
            elif self.windows_size_mode == 1:
                self.setGeometry(0, 0, int(self.display_width_default), int(self.display_height[0]))
                # self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 모든 창 앞에 위치하도록 설정
                self.windows_size_mode = self.windows_size_mode + 1
            elif self.windows_size_mode == 2:
                self.showMaximized()
                self.windows_size_mode = self.windows_size_mode + 1
            elif self.windows_size_mode == 3:
                self.setGeometry(1600 - int(self.display_width_default), 0, int(self.display_width_default), int(self.display_height[0]))
                self.windows_size_mode = 0

        def set_shortcut(self, shortcut_key_promised, function):
            # self.shortcut = QShortcut(QKeySequence(self.available_shortcut_list[btn_name_promised]), self)  # ctrl+1 2개 키들의 조합 설정
            self.shortcut = QShortcut(self.available_shortcut_list[shortcut_key_promised], self)  # ctrl+n+d 3개 키들의 조합 설정 시도
            self.shortcut.activated.connect(function)
            pass

        def get_btn(self, btn_name, function, btn_text_align="left"):
            from pk_internal_tools.pk_objects.pk_files import F_GMARKETSANSTTFLIGHT_TTF
            button = QPushButton(btn_name, self)  # alt f4 로 튜토리얼 해도 되겠다. 이건 그냥 설정 되어 있는 부분.
            button.clicked.connect(function)

            # 2023년 12월 14일 (목) 16:28:15
            # 결론, fixed width font로 시도해볼 수 있다 자릿 수를 맞출 수 있다.
            # non-fixed width font 이슈 JAVA 에서도 구현했을 때 마딱드렸던 내용인데,
            # 분명히 문장 전체 길이를 단어 사이의 공백의 수를 결정짓는 함수를 테스트 했음에도 자릿수가 맞지 않았는데
            # 이는 고정 폭이 아님이기 때문이었다 따라서 고정 폭 폰트로 출력되는 콘솔에서는 정상, 비고정 폭 폰트로 출력되는 콘솔에서는 비정상,
            # 이 경우에는 콘솔이 아니라 pyside6 로 만든 UI 에서 나타났다.
            # 새벽에 이 문제를 만나서 잠깐 넋나갔는데 아침에 다시보니 그때 경험이 떠올라서 실험해보니 잘 해결되었다. 덕분에 pyside6에서 위젯에 폰트 적용하는 법도 터득

            # pyside6 버튼 내장폰트 설정
            # pyside6 built in fixed width font
            # font = QFont("Monospace")
            # font = QFont("Ubuntu Mono")
            # font = QFont("Inconsolata")
            # font = QFont("Monaco")
            # font = QFont("Courier")
            # font = QFont("Courier 10 Pitch")
            # font = QFont("Courier Prime")
            # font = QFont("Droid Sans Mono")
            # font = QFont("Fira Mono")
            # font = QFont("Hack")
            # font = QFont("Menlo")
            # font = QFont("Monofur")
            # font = QFont("Noto Mono")
            # font = QFont("PT Mono")
            # font = QFont("Roboto Mono")
            # font = QFont("Source Code Pro")
            # font = QFont("Victor Mono")
            # font = QFont("Courier New")
            # font = QFont("Liberation Mono")
            # font = QFont("DejaVu Sans Mono")
            # font = QFont("Consolas")  # 그나마 가장 마음에 드는 폰트

            # pyside6 버튼 외부폰트 설정
            button.setFont(Pyside6Util.get_font_for_pyside6(font_path=F_GMARKETSANSTTFLIGHT_TTF))
            if btn_text_align == "right":
                # button.setStyleSheet("QPushButton { text-align: right; color: rgba(255,255,255, 0.9); height: 20px; font-size: 8px}")
                # button.setStyleSheet("QPushButton { text-align: right; color: rgba(255,255,255, 0.9);               font-size: 8px}")
                button.setStyleSheet("QPushButton { text-align: right; color: rgba(255,255,255, 0.9);               font-size: 13px}")
                # button.setStyleSheet("QPushButton { text-align: right; color: rgba(255,255,255, 0.9); height: 20px; font-size: 13px}")
                button.setFixedWidth(65)
                # button.setMinimumWidth(button.sizeHint().width())
            else:
                # button.setStyleSheet("QPushButton { text-align: left; color: rgba(255,255,255, 0.9); height: 20px; font-size: 8px}")
                # button.setStyleSheet("QPushButton { text-align: left; color: rgba(255,255,255, 0.9);                 font-size: 8px}")
                button.setStyleSheet("QPushButton { text-align: left; color: rgba(255,255,255, 0.9);                 font-size: 13px}")
                # button.setStyleSheet("QPushButton { text-align: left; color: rgba(255,255,255, 0.9); height: 20px; font-size: 13px}")
                button.setFixedWidth(225)
                # button.setMinimumWidth(button.sizeHint().width())
            return button

        def move_window_to_center(self):
            center = QScreen.availableGeometry(self.app.primaryScreen()).center()
            geo = self.frameGeometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())
            # if self.screens:
            #     primary_screen = self.screens[0]  # 첫 번째 화면을 기본 화면으로 설정합니다.
            #     center = primary_screen.availableGeometry().center()  # 기본 화면의 중앙 좌표를 가져옵니다.
            #     # 화면을 가운데로 이동시키는 코드를 작성하세요.
            #     # 예시로 윈도우를 생성하고 중앙 좌표를 이용하여 위치를 설정합니다.
            #     self.setGeometry(100, 100, 500, 300)  # 윈도우의 초기 위치와 크기를 설정합니다.
            #     self.move(center - self.rect().center())  # 윈도우를 화면 중앙으로 이동시킵니다.

        def move_pyside6_window_to_front(self):
            # self.activateWindow() 와 self.show() 의 위치는 서로 바뀌면 의도된대로 동작을 하지 않는다
            self.show()
            self.activateWindow()
            # active_window = win32gui.GetForegroundWindow()
            # win32gui.SetForegroundWindow(active_window)

    class MacroWindow(QDialog):
        # class MacroWindow(QWidget):
        def __init__(self):
            from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
            from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
            from pk_internal_tools.pk_functions.print_cyan import print_cyan
            from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
            from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV, F_ICON_PNG
            super().__init__()
            f = F_POP_SOUND_POP_SOUND_WAV
            if os.path.exists(f):
                #  import play_wav_f
                play_wav_f(f=F_POP_SOUND_POP_SOUND_WAV)

            #  매크로 창 전역 변수 설정
            self.previus_pressed_keys = []
            self.display_width = get_display_info()['width'],
            self.display_height = get_display_info()['height'],
            # self.display_width_default = int(int(self.display_width[0]) * 0.106)
            self.display_width_default = int(int(self.display_width[0]) * 0.06)
            self.display_height_default = int(int(self.display_height[0]) * 0.2)

            # 마우스 위치, 클릭 정보, 시간 정보를 저장할 리스트
            # self.positions = []

            # 녹화 시작 시간
            self.time_recording_start = time.time()
            # self.time_recording_start_rel = 0.0
            self.elapsed_full_recording_time = 0.0
            self.previous_time = time.time()
            self.time_recording_end = 0.0
            #  메인창 설정
            self.setWindowTitle('.')
            self.setWindowIcon(QIcon(str(F_ICON_PNG)))  # 메인창 아이콘 설정
            # self.setAttribute(Qt.WA_TranslucentBackground) # 메인창 블러 설정
            # self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 메인창 최상단 프레임레스 설정
            GlobalBlur(self.winId(), hexColor=False, Acrylic=False, Dark=True, QWidget=self)
            self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)  # 최대화 최소화 버튼 숨기기
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
            self.scale = 1 / 10
            self.windows_size_mode = 0  # 창크기 모드 설정  #0 ~ 3

            QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 고해상도 스케일링을 활성화합니다.
            self.screens = QGuiApplication.screens()  # 사용 가능한 모든 화면을 가져옵니다.
            self.rotate_window_size_mode()

            # label 설정
            self.label = QLabel(self)
            self.label.setStyleSheet("color: rgba(255,255,255, 0.9);")
            self.label.setText(f"녹화 중...\n녹화경과시간: None\n")

            # 단축키 설정
            self.available_shortcut_list = {
                'MACRO EXCUTE': 'Ctrl+E',
                'MACRO EXIT': 'Ctrl+Q',
            }
            # self.set_shortcut('MACRO RECORD',self.record_macro)
            self.set_shortcut('MACRO EXCUTE', self.execute_macro)
            self.set_shortcut('MACRO EXIT', self.exit_macro)

            # 버튼 설정
            btn_to_execute_macro = self.get_btn(self.get_btn_name_with_shortcut_name('MACRO EXCUTE'), self.execute_macro)
            btn_to_exit_macro = self.get_btn(self.get_btn_name_with_shortcut_name('MACRO EXIT'), self.exit_macro)

            # GRID SETTING
            grid = QtWidgets.QGridLayout(self)
            btns = [
                self.label,
                btn_to_execute_macro,
                btn_to_exit_macro
            ]
            cnt = 0
            for i in btns:
                grid.addWidget(i, cnt, 0)
                cnt = cnt + 1

            # 레이아웃 설정
            layout = QGridLayout(self)
            layout.addLayout(grid, 0, 0)

            # 단일 단축키가 같이 눌리는 문제 ( ctrl + v 를 누르면   ctrl + v 에 바인딩된 함수만 호출되길 기대하는데, ctrl 에 바인딩된 함수도 호출되는 문제 )
            # 이벤트를 나누어 만들어 하나의 이벤트가 호출되면 다른 하나의 이벤트는 호출되지 않도록 설정 시도
            self.is_processing_event = False

            # Condition 객체 생성
            # self.condition = threading.Condition()

            # 이벤트 우선순위 설정
            # self.is_event_shortcut_3_processing = False # highest priority
            # self.is_event_shortcut_1_processing = False

            # 마우스 이동 이벤트 핸들러 설정
            listener = pynput.mouse.Listener(on_move=self.on_mouse_move)
            listener.start()

            # 마우스 버튼 클릭 이벤트 핸들러 설정
            listener2 = pynput.mouse.Listener(on_click=self.on_mouse_btn_clicked)
            listener2.start()

            # 키보드 이벤트 핸들러 설정 ( 3개 조합 단축키 , 2개 조합 단축키 , 단일 단축키 모두가능)
            self.keyboard_main_listener = pynput.keyboard.Listener(on_press=self.on_keys_down, on_release=self.on_keys_up)
            self.keyboard_main_listener.start()
            # 충돌이 문제가 아니고 두 이벤트가 중복이 되면 안되고 이벤트에 우선순위를 더 두어서 두 이벤트 호출 시 우선순위가 높은 이벤트만 exec 되도록

            # self.is_processing_event = False

            # 이벤트 핸들러 스레드 생성
            # event1_thread = threading.Thread(target=self.listener3)
            # event2_thread = threading.Thread(target=self.listner_2_combination_shorcuts)

            # 이벤트 핸들러 스레드 시작
            # event1_thread.start()
            # event2_thread.start()

            # 키보드 이벤트 핸들러 설정 ( 단일 단축키 )
            # self.listener3 = pynput.keyboard.Listener(on_press=self.on_keboard_press, suppress=True)
            # self.listener3.start()

            # 모니터링 이벤트 설정
            # self.mouse_positions = []
            # self.previous_position = None
            # self.current_position = None
            # self.timer = QTimer()
            # self.timer.timeout.connect(self.on_left_mouse_btn_clicked)
            # self.timer.start(900)

            # 녹화 경과시간 업데이트
            self.timer2 = QTimer()
            self.timer2.timeout.connect(self.update_label)  # noqa # 해당 검사에 대해서는 예외 목록에 "connect"를 넣는 것을 권장합니다. jetbrain 오류로 다년간 지속된 것으로 생각 중이다,
            self.timer2.start(1000)

            print("매크로녹화를 시작합니다")

            # 매크로녹화시작 로깅
            log_title = "매크로녹화시작"
            #  import get_pk_time_2025_10_20_1159
            contents = f"{PK_UNDERLINE}{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')}{log_title}"
            print_cyan(contents)
            self.save_macro_log(contents=contents)

            self.bring_this_window()

            # event_loop = QEventLoop()
            # event_loop.exec()

        def on_mouse_move(self, x, y):  # 아주 빠르게 감지
            # 이방식으로 매크로 중지를 할까?
            # print(f"마우스 이동 - X: {x}, Y: {y}")
            # print("마우스가 움직였습니다")
            # 상단 네비게이션
            if 0 <= x <= 3440 and 0 <= y <= 25:
                self.rotate_window_size_mode()
            else:
                pass

        def eventFilter(self, obj, event):
            if event.type() == QEvent.MouseMove:
                x = event.globalX()
                y = event.globalY()
                print(f"pyside6 창 외부 마우스 이동 감지 시도 - X: {x}, Y: {y}")
            return super().eventFilter(obj, event)

            # if event.type() == QEvent.MouseButtonPress and not self.rect().contains(event.pos()):
            #     print("pyside6 창 외부 클릭 되었습니다")
            # return super().eventFilter(obj, event)

        def get_btn_name_with_shortcut_name(self, button_name_without_shortcut):
            numbers = []
            for key, value in self.available_shortcut_list.items():
                numbers.append(len(value) + len(key))
            max_len_value = max(numbers)
            # print(max_len_value)

            button_name_with_short_cut = ""
            for key, value in self.available_shortcut_list.items():
                # print(key == button_name_without_shortcut)
                # print(key)
                # print(button_name_without_shortcut)

                if key == button_name_without_shortcut:
                    space_between = " " * (max_len_value - len(key) - len(value) + 1)
                    # space_between = " "
                    # space_between = str(max_len_value - len(key) - len(value) + 1)
                    # button_name_with_short_cut = button_name_with_short_cut + f"{key}{space_between}{value}\n"
                    button_name_with_short_cut = button_name_with_short_cut + f"{key}{space_between}{value}".strip()
            print(button_name_with_short_cut)
            return button_name_with_short_cut

        def rotate_window_size_mode(self):
            if self.windows_size_mode == 0:
                self.bring_this_window()
                self.setGeometry(0, 0, int(self.display_width_default / 2), int(self.display_height[0] / 5))
                self.move_window_to_center()
                self.windows_size_mode = self.windows_size_mode + 1
            elif self.windows_size_mode == 1:
                self.showMinimized()
                self.windows_size_mode = 0

        def set_shortcut(self, btn_name_promised, function):
            self.shortcut = QShortcut(self.available_shortcut_list[btn_name_promised], self)  # ctrl+n+d 3개 키들의 조합 설정 시도
            self.shortcut.activated.connect(function)
            pass

        def get_btn(self, btn_name, function):
            from pk_internal_tools.pk_objects.pk_files import F_RUBIKDOODLESHADOW_REGULAR_TTF
            button = QPushButton(btn_name, self)
            button.clicked.connect(function)

            # 폰트 설정
            button.setFont(Pyside6Util.get_font_for_pyside6(font_path=F_RUBIKDOODLESHADOW_REGULAR_TTF))  # 입체감있는 귀여운 영어 폰트
            button.setStyleSheet("QPushButton { text-align: left; color: rgba(255,255,255, 0.9); height: 20px ; font-size: 10px}")
            # button.setLayoutDirection(QtCore.Qt.)
            return button

        def move_window_to_center(self):
            # center = QScreen.availableGeometry(app.primaryScreen()).center()
            # geo = self.frameGeometry()
            # geo.moveCenter(center)
            # self.move(geo.topLeft())
            if self.screens:
                primary_screen = self.screens[0]  # 첫 번째 화면을 기본 화면으로 설정합니다.
                center = primary_screen.availableGeometry().center()  # 기본 화면의 중앙 좌표를 가져옵니다.
                # 화면을 가운데로 이동시키는 코드를 작성하세요.
                # 예시로 윈도우를 생성하고 중앙 좌표를 이용하여 위치를 설정합니다.
                self.setGeometry(100, 100, 500, 300)  # 윈도우의 초기 위치와 크기를 설정합니다.
                self.move(center - self.rect().center())  # 윈도우를 화면 중앙으로 이동시킵니다.

                # self.show()

        def execute_macro(self):
            pass

        def exit_macro(self):
            from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
            from pk_internal_tools.pk_functions.print_cyan import print_cyan
            from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
            from pk_internal_tools.pk_objects.pk_files import F_MACRO_LOG
            #  import get_pk_time_2025_10_20_1159
            # 매크로녹화종료 로깅
            log_title = "매크로녹화종료"
            self.time_recording_end = self.elapsed_full_recording_time
            contents = f"{PK_UNDERLINE}{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')}{log_title}"
            print_cyan(contents)
            self.save_macro_log(contents=contents)

            # 매크로 로그 확인
            print("저장된 매크로 로그를 확인합니다")

            os.system(f'explorer "{F_MACRO_LOG}" ')

        # @Slot() # 최신 버전의 PySide6에서는 @Slot() 데코레이터를 사용하지 않고도 Slot 메서드를 정의할 수 있습니다. 이렇게 되면 자동으로 Slot으로 인식됩니다. 즉 최신버전 pyside6 에서는 쓸 필요 없다.
        def update_label(self):

            try:
                self.elapsed_full_recording_time = int(time.time() - self.time_recording_start)
                self.label.setText(f"녹화 중...\n녹화경과시간: {self.elapsed_full_recording_time} secs \n")
            except:
                traceback.print_exc(file=sys.stdout)

        def on_mouse_btn_clicked(self, x, y, button, pressed):
            from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
            from pk_internal_tools.pk_functions.print_cyan import print_cyan
            #  import get_pk_time_2025_10_20_1159
            # 현재 시간과 녹화 시작 시간의 차이 계산
            current_time = time.time()
            elapsed_time = int((current_time - self.previous_time) * 1000)
            # print(f"current_time : {current_time}")
            # print(f"self.previous_time : {self.previous_time}")

            # x, y = pyautogui.position() # parameter 에서 오는 값과 동일하므로 대안으로 남겨둠.
            if button == pynput.mouse.Button.left and pressed:
                info = f"sleep({elapsed_time})   %%%FOO%%%    click_mouse_left_btn(abs_x={x},abs_y={y}) "
                print_cyan(info)
                self.save_macro_log(contents=f"{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')} {info}")
            elif button == pynput.mouse.Button.right and pressed:
                info = f"sleep({elapsed_time})   %%%FOO%%%    click_mouse_right_btn(abs_x={x},abs_y={y}) "
                print_cyan(info)
                self.save_macro_log(contents=f"{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')} {info}")

            # 현재시간을 이전시간에 저장
            self.previous_time = current_time

        def save_macro_log(self, contents: str):
            from pk_internal_tools.pk_objects.pk_files import F_MACRO_LOG
            macro_log = F_MACRO_LOG
            os.makedirs(os.path.dirname(F_MACRO_LOG))
            with open(macro_log, "a", encoding="utf-8") as f:
                f.write(f"{contents}\n")

        def on_keboard_press(self, key):
            # global is_processing_event
            # if self.is_processing_event != False:
            print(f'키보드 입력: {key}')

            # isinstance()
            # all(list) # (iterable) 객체의 모든 요소가 참(True)인지 확인
            # all(dict) # (iterable) 객체의 모든 요소가 참(True)인지 확인
            # all(tuple) # (iterable) 객체의 모든 요소가 참(True)인지 확인

        def on_keys_down(self, key):
            from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
            from pk_internal_tools.pk_functions.print_cyan import print_cyan
            # 현재 시간과 녹화 시작 시간의 차이 계산
            current_time = time.time()
            elapsed_time = int((current_time - self.previous_time) * 1000)

            # for hotkey in self.HOTKEYS:
            #     hotkey.release(self.keyboard_listener1.canonical(key))
            #     print(f"key : {key}")

            # 키이름 여러 형식으로 출력
            # try:
            #     print(key)
            #     print(key.value)
            #     print(key.value.vk)
            # except:
            #     print(key)
            #     pass

            # 키이름 전처리
            key: str = str(key)
            key: str = key.lower()
            key: str = key.replace("\'", "")
            key: str = key.replace("\"", "")
            key: str = key.replace("key.", "")
            key: str = key.replace("<25>", "한자 or ctrl_r")
            key: str = key.replace("<21>", "한영 or alt_r")
            key: str = key.replace("12", "텐키 5")  # 텐키
            key: str = key.replace("cmd", "win")
            key: str = key.replace("page", "pg")
            key: str = key.replace("down", "dn")
            if key != "num_lock":
                key: str = key.replace("_l", "")
            key: str = key.replace("_r", "")

            key: str = key.replace(" ", "")
            key: str = key.replace("<", "")
            key: str = key.replace(">", "")
            # key: str = key.replace("_", "")

            # 전처리 후 출력
            # print(str(key))

            # if key == "ctrl+alt":
            log_title = "키보드인풋"
            info = f"sleep({elapsed_time})\nkeyDown('{key}') "
            print_cyan(info)
            #  import get_pk_time_2025_10_20_1159
            self.save_macro_log(contents=f"{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')}{log_title} {info}")

            # 현재시간을 이전시간에 저장
            self.previous_time = current_time

            # if self.store = []
            # global is_processing_event
            # if self.is_processing_event == False:
            # self.is_processing_event = True
            # self.is_processing_event = False

            # pynput.keyboard.Listener()는 다시 self.listener3.start() 할 수 없다.
            # 새로 만들어야 한다
            # if self.listener3.is_alive():
            #     self.listener3.stop()
            # else:

            # self.listener3 = pynput.keyboard.Listener(on_press=self.on_keboard_press)
            # self.listener3.start()

            # self.condition.notify()  # event1에게 동작 신호 보내기

        def on_single_key_pressed(self, key):
            from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
            from pk_internal_tools.pk_functions.print_cyan import print_cyan

            # 현재 시간과 녹화 시작 시간의 차이 계산
            current_time = time.time()
            elapsed_time = int((current_time - self.previous_time) * 1000)

            # print(str(key))
            if pynput.keyboard.GlobalHotKeys.name == "<ctrl>":
                log_title = "키보드단일키인풋"
                info = f"  sleep({elapsed_time})   %%%FOO%%%    press({str(key)}) "
                print_cyan(info)
                #  import get_pk_time_2025_10_20_1159
                self.save_macro_log(contents=f"{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')}{log_title} {info}")

            # 현재시간을 이전시간에 저장
            self.previous_time = current_time

            # try:
            #     # alphanumeric key
            #     print('{0}'.format(key.char))
            # except AttributeError:
            #     # special key
            #     print('{0}'.format(key.char))

        def on_keys_up(self, key):
            from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
            from pk_internal_tools.pk_functions.print_cyan import print_cyan
            # 현재 시간과 녹화 시작 시간의 차이 계산
            current_time = time.time()
            elapsed_time = int((current_time - self.previous_time) * 1000)

            # for hotkey in self.HOTKEYS:
            #     if hotkey
            #     hotkey.press(self.keyboard_listener1.canonical(key))
            #     print(f"key : {key}")

            # 키이름 전처리
            key: str = str(key)
            key: str = key.lower()
            key: str = key.replace("\'", "")
            key: str = key.replace("\"", "")
            key: str = key.replace("key.", "")
            key: str = key.replace("<25>", "한자 or ctrl_r")
            key: str = key.replace("<21>", "한영 or alt_r")
            key: str = key.replace("12", "텐키 5")  # 텐키
            key: str = key.replace("cmd", "win")
            key: str = key.replace("page", "pg")
            key: str = key.replace("down", "dn")
            if key != "num_lock":
                key: str = key.replace("_l", "")
            key: str = key.replace("_r", "")

            key: str = key.replace(" ", "")
            key: str = key.replace("<", "")
            key: str = key.replace(">", "")
            # key: str = key.replace("_", "")

            # 전처리 후 출력
            # print(str(key))

            log_title = "키보드릴리즈"
            info = f"sleep({elapsed_time})\nkeyUp('{key}') "
            print_cyan(info)
            #  import get_pk_time_2025_10_20_1159
            self.save_macro_log(contents=f"{get_pk_time_2025_10_20_1159('%Y-%m-%d_%H:%M:%S')}{log_title} {info}")

            # 현재시간을 이전시간에 저장
            self.previous_time = current_time
            pass

        def bring_this_window(self):
            self.show()
            self.activateWindow()
            # active_window = win32gui.GetForegroundWindow()
            # win32gui.SetForegroundWindow(active_window)

    class CustomQthread(QThread):
        finished = Signal()  # run()의 성공 신호를 보내기 위해 필요, run() 은 상속된 QThread 객체의 run()을 통해서 오버라이딩 되는 것 보인다.

        def __init__(self, q_application):  # 이 생성자는 q_application 를 받기 위해서 내가 작성 q_application 가 필요없는 void method QThread 이용 시 그냥 없애면 되는 생성자.
            super().__init__()
            self.q_application = q_application

        def run(self):
            # QThread 동작 테스트 코드
            print("QThread 초기화 시작")
            for i in range(10):
                print(i)
                self.msleep(30)

            def tmp2(q_application: QApplication):
                global dialog2
                dialog2 = PkGui.CustomDialog(q_application=q_application, q_wiget=PkGui.PkQdialog(prompt="테스트", buttons=["exec ", "exec 하지 않기"]), is_app_instance_mode=False)
                if dialog2.txt_clicked == "exec ":
                    print("정상적으로 동작합니다")

            def tmp(string: str):
                print(string)

            # 프로그램 외 단축키 이벤트 설정
            shortcut_keys_up_promised = {
                # "<ctrl>+<cmd>": self.close, #success
                # "<ctrl>+T": partial(tmp, "test"), #success
                # "<ctrl>+Q": partial(tmp2, self.q_application), #fail
                # "<ctrl>+h": partial(q_wiget.toogle_rpa_window, "<ctrl>+h"), #fail
            }
            keyboard_main_listener = pynput.keyboard.GlobalHotKeys(hotkeys=shortcut_keys_up_promised)
            keyboard_main_listener.start()

            self.finished.emit()  # 작업이 성공되었음을 신호로 알림 # flutter 상태관리와 비슷
            print("QThread exec  증...")

    @staticmethod
    def pop_up_as_complete(title: str, ment: str, auto_click_positive_btn_after_milliseconds: int, input_text_default="", btn_list=None):

        import os
        import platform

        from PySide6.QtWidgets import QApplication

        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        import logging
        from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
        from pk_internal_tools.pk_functions.print_cyan import print_cyan
        from pk_internal_tools.pk_functions.print_success import print_success
        from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV
        # should_i_do 가 앱 안과 밖에서도 잘 된다면 deprecated 하자
        if btn_list is None:
            btn_list = ["확인"]
        if platform.system() == 'Windows':
            func_n = get_caller_name()
            logging.debug(rf'''%%%FOO%%%''')
            f = F_POP_SOUND_POP_SOUND_WAV
            if os.path.exists(f):
                #  import play_wav_f
                play_wav_f(f=f)

            app_foo = None

            # QApplication 인스턴스 확인
            app = QApplication.instance()
            if app is None:
                app_foo = QApplication()
            if input_text_default == "":
                is_input_text_box = False
            else:
                is_input_text_box = True

            dialog = PkGui.PkQdialog(title=title, prompt=ment, buttons=btn_list, input_box_mode=is_input_text_box, input_box_text_default=input_text_default, auto_click_positive_btn_after_milliseconds=auto_click_positive_btn_after_milliseconds)
            dialog.exec()
            txt_clicked = dialog.txt_clicked

            if txt_clicked == "":
                print_cyan(f'버튼 입니다 {txt_clicked}')
            if app == True:  # .....app 은 bool 이 아닌데. 동작 되고있는데..
                print_cyan("여기는 좀 확인을 해야하는데. 호출 안되면 좋겠는데1")
                if isinstance(app_foo, QApplication):
                    print_cyan("여기는 좀 확인을 해야하는데. 호출 안되면 좋겠는데2")
                    app_foo.exec()
            if app == True:
                # app_foo.quit()# QApplication 인스턴스 제거시도 : fail
                # app_foo.deleteLater()# QApplication 인스턴스 파괴시도 : fail
                # del app_foo # QApplication 인스턴스 파괴시도 : fail
                # app_foo = None # QApplication 인스턴스 파괴시도 : fail
                print_cyan("여기는 좀 확인을 해야하는데. 호출 안되면 좋겠는데3")
                app_foo.shutdown()  # QApplication 인스턴스 파괴시도 : success  # 성공요인은 app.shutdown()이 호출이 되면서 메모리를 해제까지 수행해주기 때문
                # sys.exit()
        else:
            print_success(f"{ment}")


class Pyside6Util:
    @staticmethod
    def get_font_for_pyside6(font_path):
        from PySide6.QtGui import QFontDatabase, QFont

        font_id = QFontDatabase.addApplicationFont(font_path)
        font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_name)
        font.setFixedPitch(True)
        return font


def ask_user(text: str, function: Callable = None, auto_click_negative_btn_after_milliseconds: int = None, auto_click_positive_btn_after_milliseconds: int = None, input_box_text_default="", buttons=None, title="%%%FOO%%%", input_box_mode=False, sync_mode: bool = True):
    """
    사용자에게 질의하고 응답을 받습니다. GUI 다이얼로그를 통해 사용자 입력을 받습니다.
    
    Args:
        text: 사용자에게 표시할 질문 또는 메시지
        function: 콜백 함수 (비동기 모드에서 사용)
        auto_click_negative_btn_after_milliseconds: 자동으로 부정 버튼 클릭까지의 밀리초
        auto_click_positive_btn_after_milliseconds: 자동으로 긍정 버튼 클릭까지의 밀리초
        input_box_text_default: 입력 상자 기본 텍스트
        buttons: 버튼 목록 (기본값: [PkTexts.POSITIVE, PkTexts.NEGATIVE])
        title: 다이얼로그 제목
        input_box_mode: 입력 상자 모드 활성화 여부
        sync_mode: 동기 모드 여부 (True: dialog.exec() 블로킹, False: dialog.show() 비동기, 기본값: True)
        
    Returns:
        tuple: (txt_clicked, function, txt_written) - 동기 모드에서 즉시 반환
               None - 비동기 모드에서 즉시 반환 (결과는 콜백 함수로 전달)
    """
    import os
    import sys
    import platform

    from PySide6.QtWidgets import QApplication

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    import logging
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.play_wav_f import play_wav_f
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_files import F_POP_SOUND_POP_SOUND_WAV

    try:
        func_n = get_caller_name()
        logging.debug(f"ask_user 시작: title={title}, prompt={text[:50]}..., sync_mode={sync_mode}")

        # Windows가 아닌 환경에서는 GUI 팝업 불가
        if platform.system() != 'Windows':
            logging.warning(f"ask_user: Windows가 아닌 환경 ({platform.system()})에서는 GUI 팝업을 표시할 수 없습니다.")
            return (None, function, None)

        if not buttons:
            buttons = [PkTexts.POSITIVE, PkTexts.NEGATIVE]
        logging.debug(f"ask_user: 버튼 목록: {buttons}")

        # gui pop sound
        f = F_POP_SOUND_POP_SOUND_WAV
        if os.path.exists(f):
            try:
                play_wav_f(f=f)
                logging.debug(f"ask_user: 팝 사운드 재생 성공")
            except Exception as e:
                logging.warning(f"ask_user: 팝 사운드 재생 실패: {e}")

        # make QApplication
        app_foo = None
        app = QApplication.instance()
        logging.debug(f"ask_user: QApplication.instance() = {app}")

        if app is None:
            try:
                # sys.argv를 전달하여 QApplication 초기화
                app_foo = QApplication(sys.argv if hasattr(sys, 'argv') else [])
                logging.debug(f"ask_user: QApplication 생성 성공: {app_foo}")
            except Exception as e:
                logging.error(f"ask_user: QApplication 생성 실패: {e}", exc_info=True)
                return (None, function, None)
        else:
            logging.debug(f"ask_user: 기존 QApplication 인스턴스 사용: {app}")

        # dialog 생성
        try:
            logging.debug(f"ask_user: PkQdialog 생성 시작")
            dialog = PkGui.PkQdialog(
                title=title,
                prompt=text,
                buttons=buttons,
                input_box_mode=input_box_mode,
                input_box_text_default=input_box_text_default,
                auto_click_positive_btn_after_milliseconds=auto_click_positive_btn_after_milliseconds,
                auto_click_negative_btn_after_milliseconds=auto_click_negative_btn_after_milliseconds
            )
            logging.debug(f"ask_user: PkQdialog 생성 성공")

            # dialog가 제대로 생성되었는지 확인
            if dialog is None:
                logging.error("ask_user: PkQdialog 생성 결과가 None입니다.")
                return (None, function, None)

            # 창을 앞으로 가져오기
            try:
                ensure_window_to_front(title if title != "%%%FOO%%%" else ".")
                logging.debug(f"ask_user: ensure_window_to_front 호출 완료")
            except Exception as e:
                logging.warning(f"ask_user: ensure_window_to_front 실패: {e}")

            # 동기/비동기 모드에 따라 실행
            if sync_mode:
                # 동기 모드: dialog.exec() 사용 (블로킹)
                logging.debug(f"ask_user: 동기 모드 - dialog.exec() 호출 시작")
                dialog.show()
                if app_foo is not None:
                    app_foo.processEvents()
                elif app is not None:
                    app.processEvents()

                dialog.exec()
                logging.debug(f"ask_user: dialog.exec() 완료")

                txt_clicked = dialog.txt_clicked
                logging.debug(f"ask_user: 클릭된 버튼: {txt_clicked}")

                txt_written = None
                if not input_box_mode == False:
                    if hasattr(dialog, 'input_box') and dialog.input_box is not None:
                        if not dialog.input_box.text() is None:
                            txt_written = dialog.input_box.text()
                            logging.debug(f"ask_user: 입력된 텍스트: {txt_written}")

                logging.debug(f"ask_user: 완료: txt_clicked={txt_clicked}, txt_written={txt_written}")
                return (txt_clicked, function, txt_written)
            else:
                # 비동기 모드: dialog.show() 사용 (논블로킹)
                logging.debug(f"ask_user: 비동기 모드 - dialog.show() 호출")
                dialog.show()

                # 이벤트 루프 처리
                if app_foo is not None:
                    app_foo.processEvents()
                elif app is not None:
                    app.processEvents()

                # 콜백 함수가 있으면 다이얼로그가 닫힐 때 콜백 연결
                if function is not None:
                    def on_dialog_finished(result_code):
                        # 다이얼로그가 닫힐 때 txt_clicked 확인
                        txt_clicked = getattr(dialog, 'txt_clicked', None)
                        txt_written = None
                        if not input_box_mode == False:
                            if hasattr(dialog, 'input_box') and dialog.input_box is not None:
                                input_text = dialog.input_box.text()
                                if input_text is not None:
                                    txt_written = input_text
                        logging.debug(f"ask_user: 비동기 모드 - 콜백 호출: txt_clicked={txt_clicked}, txt_written={txt_written}")
                        try:
                            function(txt_clicked, txt_written)
                        except Exception as e:
                            logging.error(f"ask_user: 콜백 함수 실행 중 오류 발생: {e}", exc_info=True)

                    # 다이얼로그가 닫힐 때 콜백 호출
                    dialog.finished.connect(on_dialog_finished)
                else:
                    logging.warning("ask_user: 비동기 모드에서 콜백 함수가 제공되지 않았습니다. 결과를 받을 수 없습니다.")

                logging.debug(f"ask_user: 비동기 모드 - dialog.show() 완료, 즉시 반환")
                return None

        except Exception as e:
            logging.error(f"ask_user: dialog 생성 또는 실행 중 오류 발생: {e}", exc_info=True)
            try:
                import traceback as tb
                logging.error(f"ask_user: Traceback:\n{tb.format_exc()}")
            except Exception:
                pass
            return (None, function, None)

    except Exception as e:
        logging.error(f"ask_user: 전체 함수 실행 중 오류 발생: {e}", exc_info=True)
        try:
            import traceback as tb
            logging.error(f"ask_user: Traceback:\n{tb.format_exc()}")
        except Exception:
            pass
        return (None, function, None)


# 하위 호환성을 위한 별칭
def should_i_do(prompt: str = None, *args, **kwargs):
    """
    ask_user의 하위 호환성 별칭입니다.
    이 함수는 더 이상 사용되지 않으며, ask_user를 사용하세요.
    
    초 단위 인자를 밀리초로 자동 변환합니다.
    """
    import logging
    from pk_internal_tools.pk_functions.get_milliseconds_from_seconds import get_milliseconds_from_seconds

    logging.warning("should_i_do는 더 이상 사용되지 않습니다. ask_user를 사용하세요.")

    # prompt를 text로 변환
    if prompt is not None:
        kwargs['text'] = prompt
    elif 'prompt' in kwargs:
        kwargs['text'] = kwargs.pop('prompt')

    # 초 단위 인자를 밀리초로 변환
    if 'auto_click_negative_btn_after_seconds' in kwargs:
        seconds = kwargs.pop('auto_click_negative_btn_after_seconds')
        if seconds is not None:
            kwargs['auto_click_negative_btn_after_milliseconds'] = get_milliseconds_from_seconds(seconds)

    if 'auto_click_positive_btn_after_seconds' in kwargs:
        seconds = kwargs.pop('auto_click_positive_btn_after_seconds')
        if seconds is not None:
            kwargs['auto_click_positive_btn_after_milliseconds'] = get_milliseconds_from_seconds(seconds)

    return ask_user(*args, **kwargs)


def ensure_printed_as_gui(text: str, input_text_default="", auto_click_positive_btn_after_milliseconds: int = 3000, btn_list=None):
    import traceback

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    import logging
    from pk_internal_tools.pk_functions.print_red import print_red
    if not btn_list:
        btn_list = ["확인"]
    func_n = get_caller_name()
    logging.debug(rf'''%%%FOO%%%''')
    """
    이 함수는 특별한 사용요구사항이 있습니다
    pyside6 앱 내에서 해당 함수를 호출할때는 is_app_instance_mode 를 파라미터에 넣지 않고 쓰는 것을 default 로 디자인했습니다.
    pyside6 앱 밖에서 해당 함수를 호출할때는 is_app_instance_mode 를 True 로 설정하고 쓰십시오.

    사용 요구사항이 생기게 된 이유는 다음과 같습니다
    pyside6 는 app을 singletone으로 instance를 구현합니다. 즉, instance는 반드시 pyside6 app 내에서 하나여야 합니다.
    pyside6의 QApplication()이 앱 내/외에서도 호출이 될 수 있도록 디자인했습니다.
    앱 내에서 호출 시에는 is_app_instance_mode 파라미터를 따로 설정하지 않아도 되도록 디자인되어 있습니다.
    앱 외에서 호출 시에는 is_app_instance_mode 파라미터를 True 로 설정해야 동작하도록 디자인되어 있습니다.
    """
    # app_foo: QApplication = None
    # if is_app_instance_mode == True:
    #     app_foo: QApplication = QApplication()
    # if input_text_default == "":
    #     logging.debug(f"{inspect.currentframe().f_code.co_name}()")
    #     is_input_text_box = False
    # else:
    #     is_input_text_box = True
    # dialog = PkGui.PkQdialog(ment=f"{context}", buttons=["확인"], is_input_box=is_input_text_box, input_box_text_default=input_text_default)
    # logging.debug(f"{inspect.currentframe().f_code.co_name}()")
    # dialog.exec()
    # txt_clicked = dialog.txt_clicked
    # if txt_clicked == "":
    #     print_ment_magenta()(f'누르신 버튼은 {txt_clicked} 입니다')
    # if is_app_instance_mode == True:
    #     if isinstance(app_foo, QApplication):
    #         app_foo.exec()
    # if is_app_instance_mode == True:
    #     # app_foo.quit()# QApplication 인스턴스 제거시도 : fail
    #     # app_foo.deleteLater()# QApplication 인스턴스 파괴시도 : fail
    #     # del app_foo # QApplication 인스턴스 파괴시도 : fail
    #     # app_foo = None # QApplication 인스턴스 파괴시도 : fail
    #     app_foo.shutdown()  # QApplication 인스턴스 파괴시도 : success  # 성공요인은 app.shutdown()이 호출이 되면서 메모리를 해제까지 수행해주기 때문
    #     # sys.exit()
    # # return app_foo
    try:
        return PkGui.pop_up_as_complete(title="디버깅결과보고", ment=text, input_text_default=input_text_default, auto_click_positive_btn_after_milliseconds=auto_click_positive_btn_after_milliseconds, btn_list=btn_list)
    except:

        print_red(traceback.print_exc())
        return None


# THIS IS BAD FUNCTION... I SHOULD CHECK TYPE, WHEN I MADE THIS
def get_display_info():
    from screeninfo import get_monitors

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    import logging
    func_n = get_caller_name()
    logging.debug(rf'''%%%FOO%%%''')
    # 디스플레이 정보 가져오기  # pyautogui.size?() 로 대체할것.
    global height, width
    for infos in get_monitors():
        for info in str(infos).split(','):
            if 'width=' in info.strip():
                width = info.split('=')[1]
            elif 'height=' in info.strip():
                height = info.split('=')[1]
    display_setting = {
        'height': int(height),  # todo : chore : ,(comma) 실수로 써놨는데 런타임에서 발견못한 문제
        'width': int(width)
    }
    return display_setting


def get_display_setting():
    from screeninfo import get_monitors

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    import logging
    func_n = get_caller_name()
    logging.debug(rf'''%%%FOO%%%''')
    height = ''
    width = ''
    for monitor_info in get_monitors():
        for info in str(monitor_info).split(','):
            if 'width=' in info.strip():
                width = info.split('=')[1]
            elif 'height=' in info.strip():
                height = info.split('=')[1]
    display_setting = {
        'height': int(height),
        'width': int(width)
    }
    return display_setting