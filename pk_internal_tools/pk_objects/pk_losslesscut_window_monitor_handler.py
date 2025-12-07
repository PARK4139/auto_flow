import logging
import threading

from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_target_files_played_on_losslesscut import ensure_target_files_played_on_losslesscut
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_objects.pk_event import Event, EventType, EventHandler, create_event, EventQueue


class LosslessCutWindowMonitorHandler(EventHandler):
    def __init__(self, event_queue: EventQueue, media_file_controller_instance):
        super().__init__(event_queue, name="LosslessCutWindowMonitorHandler")
        self.media_file_controller = media_file_controller_instance
        self._monitoring_thread = None
        self._running = False

    def register_handlers(self):
        self.event_queue.register_handler(EventType.WINDOW_TITLE_LOSSLESSCUT_IDLE_NAME_MATCHED, self.on_losslesscut_window_matched)

    def on_losslesscut_window_matched(self, event: Event):
        logging.info(f"이벤트 수신: LosslessCut 창이 감지되었습니다. 비디오 재생 로직을 실행합니다. event.type.name={event.type.name}. ")
        ensure_target_files_played_on_losslesscut(self.media_file_controller, loop_cnt=self.loop_cnt)

    def _monitor_loop(self):
        logging.info("LosslessCut 창 모니터링 스레드 시작.")
        self.loop_cnt = 1
        while self._running:
            if is_window_opened_via_window_title(window_title=get_idle_title_of_losslesscut()):
                logging.debug("LosslessCut 창 감지. 이벤트 발생.")
                event = create_event(
                    event_type=EventType.WINDOW_TITLE_LOSSLESSCUT_IDLE_NAME_MATCHED,
                    data={"window_title": get_idle_title_of_losslesscut()},
                    source="LosslessCutWindowMonitorHandler"
                )
                self.event_queue.add_event(event)
                # ensure_slept(milliseconds=500) # 최대화 진행 중 -> 모니터 루프 종료 -> 최대화 실패(되다가 안됨)
                # ensure_slept(milliseconds=1000) # 최대화 진행 중 -> 모니터 루프 종료 -> 최대화 실패(되다가 안됨)
                # ensure_slept(milliseconds=5000) # -> succeeded -> 충분히 시간 sleep -> 최대화 -> 느림
                # ensure_slept(milliseconds=3000) # -> succeeded -> 충분히 시간 sleep -> 최대화 -> 느림
                ensure_slept(milliseconds=2000)  # -> succeeded -> 충분히 시간 sleep -> 최대화 -> 느림
            else:
                logging.debug("LosslessCut 창 아직 감지되지 않음. 대기 중...")
                ensure_slept(milliseconds=500) # -> succeeded -> 리소스 점유 과하다고 판단 -> 줄이기로 결정 -> 빠른게 나은듯
                # ensure_slept(milliseconds=3000)
            self.loop_cnt += 1

    def start_monitoring(self):
        if not self._running:
            self._running = True
            self._monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitoring_thread.start()
            logging.info("LosslessCut 창 모니터링 시작됨.")

    def stop_monitoring(self):
        if self._running:
            self._running = False
            if self._monitoring_thread and self._monitoring_thread.is_alive():
                self._monitoring_thread.join(timeout=1.0)
            logging.info("LosslessCut 창 모니터링 중지됨.")
