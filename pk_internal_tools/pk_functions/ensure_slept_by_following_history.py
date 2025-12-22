import logging
import time
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_following_history_reset_for_ensure_slept import get_pk_env_var_id, ensure_following_history_reset_for_ensure_slept
from pk_internal_tools.pk_objects.pk_directories import D_SLEEP_DURATION_HISTORY
from pk_internal_tools.pk_objects.pk_event import EventSystemManager, EventType

# 전역 이벤트 시스템 인스턴스 (ensure_mouse_clicked_by_coordination_history.py와 동일한 인스턴스 사용)
event_system_manager = EventSystemManager()
event_system_manager.start()  # 이벤트 시스템 시작 (이미 시작되었을 수 있으나, 중복 호출은 무시됨)


def ensure_slept_by_following_history(
        key_name: str,
        func_n: str,
        history_reset: bool = False,
        button: Optional[str] = None,
        keyboard_key: Optional[str] = None,
        event_type: Optional[EventType] = None,
) -> float | None:
    """
    이전 기록에 따라 지정된 시간만큼 대기하거나, 기록이 없으면 사용자 입력을 받아 대기 시간을 기록합니다.
    기본적으로 마우스 클릭을 트리거로 사용합니다.
    
    Args:ensure_windowtitle
        key_name: 환경 변수 키 이름
        func_n: 함수 이름
        history_reset: History 기록 초기화 여부
        button: 감지할 마우스 버튼 ("left", "right", "middle"). None이면 모든 버튼 클릭 감지 (기본값)
        key: 감지할 키보드 키 (문자열, 예: "enter", "space", "a" 등). None이면 사용하지 않음
        event_type: 감지할 이벤트 타입. None이면 사용하지 않음
        
    Returns:
        float: 측정된 대기 시간(초). 오류 시 None
        
    사용 예시:
        # 기본 사용 (모든 마우스 클릭 감지)
        ensure_slept_by_following_history(key_name="대기", func_n="test")
        
        # 왼쪽 버튼만 클릭 감지
        ensure_slept_by_following_history(key_name="대기", func_n="test", button="left")
        
        # 키보드 Enter 키 감지
        ensure_slept_by_following_history(key_name="대기", func_n="test", key="enter")
        
        # 특정 이벤트 타입 감지
        ensure_slept_by_following_history(key_name="대기", func_n="test", event_type=EventType.STATE_CHANGED)
    """
    if history_reset:
        logging.debug(f"대기 시간 기록 초기화 요청: {key_name}, {func_n}")
        ensure_following_history_reset_for_ensure_slept(key_name=key_name, func_n=func_n)

    file_id = f"{get_pk_env_var_id(key_name, func_n)}_for_ensure_slept"
    history_dir = D_SLEEP_DURATION_HISTORY
    history_dir.mkdir(parents=True, exist_ok=True)
    history_file = history_dir / f"{file_id}.txt"

    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                duration_str = f.read().strip()
            duration = float(duration_str)

            logging.debug(f"대기 시간(history) = {duration}초")
            logging.debug(f"대기 시작")
            time.sleep(duration)
            logging.debug(f"대기 완료: {duration}초")
            return duration

        except Exception as e:
            logging.error(f"대기 시간 파일 읽기 또는 대기 중 오류 발생: {e}. 새 시간을 기록합니다.")
            return _measure_and_record_duration(key_name, func_n, history_file, button, keyboard_key, event_type)
    else:
        logging.debug(f"대기 시간 기록이 없습니다. 새 시간을 기록합니다.")
        return _measure_and_record_duration(key_name, func_n, history_file, button, keyboard_key, event_type)


def _measure_and_record_duration(
        key_name: str,
        func_n: str,
        history_file: Path,
        button: Optional[str] = None,
        key: Optional[str] = None,
        event_type: Optional[EventType] = None,
) -> float | None:
    from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text

    # 간결한 명시적 지시 메시지 생성
    # 기본 트리거는 마우스 클릭
    if button is not None:
        button_name = {
            "left": "왼쪽",
            "right": "오른쪽",
            "middle": "가운데",
        }.get(button, button)
        instruction_msg = f"마우스 {button_name} 버튼을 클릭하세요"
    elif key is not None:
        key_name_str = key if isinstance(key, str) else str(key)
        instruction_msg = f"키보드 {key_name_str} 키를 누르세요"
    elif event_type is not None:
        instruction_msg = f"이벤트 {event_type.value}를 발생시키세요"
    else:
        # 기본값: 모든 마우스 클릭 감지
        instruction_msg = "마우스를 클릭하세요"

    logging.debug(f"대기 시간 측정 시작: {instruction_msg} (key_name: {key_name}, func_n: {func_n})")
    ensure_spoken(get_easy_speakable_text(f"대기 시간 측정: {instruction_msg}"))

    import threading
    from pynput import mouse, keyboard

    stop_event = threading.Event()
    start_time = time.time()

    # Event system handler: event_type이 지정된 경우에만 사용
    click_event_handler = None
    target_event_type = None

    if event_type is not None:
        target_event_type = event_type

        def click_event_handler(event):
            # 이벤트 타입 확인
            if event.type != target_event_type:
                return

            # 이벤트 데이터에 key_name과 func_n이 포함되어 있는지 확인하고 필터링
            if event.data.get('key_name') == key_name and event.data.get('func_n') == func_n:
                logging.debug(f"이벤트 감지: {event.type.value}. 측정 종료. (key_name: {key_name}, func_n: {func_n})")
                stop_event.set()

        # Register the event handler
        event_system_manager.event_queue.register_handler(target_event_type, click_event_handler)

    def on_click(x, y, button_clicked, pressed):
        if not pressed:
            return

        # 버튼 필터링
        if button is not None:
            button_matched = False
            if button == "left" and button_clicked == mouse.Button.left:
                button_matched = True
            elif button == "right" and button_clicked == mouse.Button.right:
                button_matched = True
            elif button == "middle" and button_clicked == mouse.Button.middle:
                button_matched = True

            if not button_matched:
                return

        logging.debug(f"마우스 {button_clicked.name if button is None else button} 클릭 감지: ({x}, {y}). 측정 종료.")
        stop_event.set()
        return False  # Stop mouse listener

    def on_press(key_pressed):
        # 키 필터링
        if key is not None:
            key_matched = False
            # 문자열 키 비교
            if isinstance(key, str):
                # 일반 문자 키
                if hasattr(key_pressed, 'char') and key_pressed.char == key:
                    key_matched = True
                # 특수 키 (예: 'esc', 'enter', 'space' 등)
                elif hasattr(key_pressed, 'name'):
                    key_name_normalized = key_pressed.name.lower().replace('_l', '').replace('_r', '')
                    if key_name_normalized == key.lower() or key_pressed.name == key:
                        key_matched = True
            # keyboard.Key 객체 비교
            elif isinstance(key, keyboard.Key):
                if key_pressed == key:
                    key_matched = True

            if not key_matched:
                return

        try:
            key_name_str = key_pressed.char if hasattr(key_pressed, 'char') else key_pressed.name
            logging.debug(f"키보드 입력 감지: {key_name_str}. 측정 종료.")
        except AttributeError:
            logging.debug(f"특수 키 입력 감지: {key_pressed}. 측정 종료.")

        stop_event.set()
        return False  # Stop keyboard listener

    # 리스너 생성 및 시작
    mouse_listener = None
    keyboard_listener = None

    # 마우스 리스너: 기본적으로 항상 활성화 (button=None이면 모든 버튼, 아니면 필터링)
    # 키보드나 이벤트 타입이 지정되지 않은 경우 마우스 클릭을 기본 트리거로 사용
    if key is None and event_type is None:
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

    # 키보드 리스너: key가 지정된 경우에만 활성화
    if key is not None:
        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.start()

    stop_event.wait()  # Wait until an event is set

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Ensure listeners are stopped and joined
    if mouse_listener and mouse_listener.running:
        mouse_listener.stop()
    if keyboard_listener and keyboard_listener.running:
        keyboard_listener.stop()

    # Unregister the event handler
    if click_event_handler is not None and target_event_type is not None:
        event_system_manager.event_queue.unregister_handler(target_event_type, click_event_handler)

    # Give a moment for threads to finish stopping
    time.sleep(0.1)

    logging.debug(f"{elapsed_time:.2f}초 측정완료 ")
    ensure_spoken(get_easy_speakable_text(f"{elapsed_time:.2f}초 측정완료 "), read_finished_wait_mode=True)
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            f.write(f"{elapsed_time}")
        logging.debug(f"대기 시간 저장 완료: {elapsed_time:.2f}초 -> {history_file}")
        return elapsed_time
    except Exception as e:
        logging.error(f"대기 시간 저장 중 오류 발생: {e}")
        return None
