"""
LM-100 milling DATA sending automation

TODO : milling Data sendable card detection logic
"""

from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_mouse_clicked_by_coordination_history import \
    ensure_mouse_clicked_by_coordination_history
from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_detected_identifiers_via_roi import get_detected_identifiers_via_roi
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

func_n = get_caller_name()


def _open_L_CAM():
    l_cam_lnk_path = ensure_env_var_completed(
        key_name="l_cam_lnk_path",
        func_n=func_n,
    )
    ensure_command_executed(f'start "" "{l_cam_lnk_path}')


def _ensure_cube_milling_on_actived():
    ensure_typed("0000")


def _ensure_clicked(key_name, history_reset=False, double_click: bool = False):
    ensure_mouse_clicked_by_coordination_history(
        key_name=key_name, func_n=func_n, history_reset=history_reset, double_click_mode=double_click
    )
    ensure_slept(milliseconds=111)
    if QC_MODE:
        alert_as_gui(rf"{key_name} is clicked")


def _wait_milling_data_sending_time():
    ensure_slept(milliseconds=1000 * 55)
    # TODO via ocr
    # while 1:
    #     if is_CAD_Data_sendable():
    #       break
    #     ensure_slept(milliseconds=1000*60)


def _ensure_l_cam_moved_front():
    test_title = "L-CAM"
    while 1:
        if is_window_title_front(window_title=test_title):
            break
        ensure_window_to_front(test_title)


def _wait_milling_data_loading_time():
    ensure_slept(milliseconds=1000 * 5)


def _wait_popup_moved_front(window_title):
    while True:
        if is_window_title_front(window_title=window_title):
            break
        ensure_window_to_front(window_title)
        ensure_slept(milliseconds=111)


def _is_popup_appeared(key_name, window_title, history_reset):
    while True:
        if not is_window_opened(window_title_seg=window_title):
            _ensure_clicked(key_name=key_name, history_reset=history_reset,
                            double_click=True)  # double click -> 밀링시작 popup appear
        ensure_slept(milliseconds=111)
        if is_window_opened(window_title_seg=window_title):
            if QC_MODE:
                alert_as_gui(rf"{window_title} is appeared")
            return True

def send_milling_data_L_CAM_to_LM_100():
    # _open_L_CAM()
    # ensure_slept(milliseconds=60 * 1000 * 2)  # wait approximity 2 mins for L-CAM Program stand by
    # select_milling_data() #

    if QC_MODE:
        LM_100_IDENTIFIERS = [
            'es8',
            # 'es9',
            # 'pp2',
            # 'pp3',
            # 'pp4',
            # 'pp5'
        ]
        # history_reset = True
        history_reset = False
    else:
        # LM_100_IDENTIFIERS = ['es8', 'es9', 'pp2', 'pp3', 'pp4', 'pp5']
        LM_100_IDENTIFIERS = ['es9',  'pp3', 'pp4']
        history_reset = False

    _ensure_l_cam_moved_front()
    detected_ids_of_lm_100 = get_detected_identifiers_via_roi(
        text_to_find="준비",
        identifiers=LM_100_IDENTIFIERS,
        history_reset=history_reset
    )
    while True:
        if QC_MODE:
            alert_as_gui(f"ACCEPTABLE TARGET ARE DETECTED\n{detected_ids_of_lm_100}")
        else:
            alert_as_gui(
                f"{detected_ids_of_lm_100} ARE DETECTED\nAS ACCEPTABLE TARGET\nIF YOU WANT SEND MILLING DATA AUTOMATICALLY(CONTINUE:YES)")

        for id in detected_ids_of_lm_100:
            _ensure_l_cam_moved_front()
            ensure_slept(milliseconds=111)
            # _ensure_clicked(key_name=id, history_reset=history_reset,
            #                 double_click=True)  # double click -> 밀링시작 popup appear
            _ensure_clicked(key_name=id, history_reset=history_reset)

            window_title = "밀링 시작"
            if _is_popup_appeared(key_name=id, window_title=window_title, history_reset=history_reset):
                _wait_popup_moved_front(window_title=window_title)

            _ensure_clicked(key_name="보내기", history_reset=history_reset)

            window_title = "데이터 내보내기"
            if _is_popup_appeared(key_name=id, window_title=window_title, history_reset=history_reset):
                _wait_popup_moved_front(window_title=window_title)
                _ensure_clicked(key_name="확인", history_reset=True)
                if not is_window_opened(window_title):
                    alert_as_gui(rf"milling data is sent to '{id}' automatically")
                else:
                    alert_as_gui(rf"event something appeared not intended")
