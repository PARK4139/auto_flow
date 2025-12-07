"""
Event 기반 시스템의 핵심 클래스들
Observer Pattern + Event Queue 하이브리드 방식
"""

import logging
import time
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from threading import Thread, Lock
from typing import List, Dict, Any, Callable


# ===== Event System =====

class EventType(Enum):
    """이벤트 타입 정의"""
    STATE_CHANGED = "STATE_CHANGED"
    WINDOW_TITLE_LOSSLESSCUT_IDLE_NAME_MATCHED = "WINDOW_TITLE_LOSSLESSCUT_IDLE_NAME_MATCHED"
    VIDEO_PLAY_STARTED = "VIDEO_PLAY_STARTED"
    VIDEO_PLAY_COMPLETED = "VIDEO_PLAY_COMPLETED"
    EXPORT_STARTED = "EXPORT_STARTED"
    EXPORT_COMPLETED = "EXPORT_COMPLETED"
    FILE_SELECTED = "FILE_SELECTED"
    ERROR_OCCURRED = "ERROR_OCCURRED"
    CLIPBOARD_CHANGED = "CLIPBOARD_CHANGED"
    WINDOW_STATE_CHANGED = "WINDOW_STATE_CHANGED"
    CLICK_DETECTED_EVENT = "CLICK_DETECTED_EVENT"


@dataclass
class Event:
    """이벤트 데이터 클래스"""
    type: EventType
    data: Dict[str, Any]
    timestamp: float
    source: str

    def __post_init__(self):
        """이벤트 생성 후 처리"""
        if not self.timestamp:
            self.timestamp = time.time()


class EventQueue:
    """이벤트 큐 관리"""

    def __init__(self, max_size: int = 1000):
        self.queue = Queue(maxsize=max_size)
        self.handlers: Dict[EventType, List[Callable]] = {}
        self.lock = Lock()
        self.stats = {
            "events_processed": 0,
            "events_dropped": 0,
            "handler_errors": 0
        }

    def add_event(self, event: Event) -> bool:
        """이벤트 추가 (큐가 가득 찬 경우 False 반환)"""
        try:
            self.queue.put_nowait(event)
            return True
        except:
            self.stats["events_dropped"] += 1
            logging.warning(f"이벤트 큐가 가득 참: {event.type.value}")
            return False

    def register_handler(self, event_type: EventType, handler: Callable):
        """이벤트 핸들러 등록"""
        with self.lock:
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            if handler not in self.handlers[event_type]:
                self.handlers[event_type].append(handler)

    def unregister_handler(self, event_type: EventType, handler: Callable):
        """이벤트 핸들러 제거"""
        with self.lock:
            if event_type in self.handlers and handler in self.handlers[event_type]:
                self.handlers[event_type].remove(handler)

    def process_events(self, max_events: int = 10) -> int:
        """이벤트 처리 (처리된 이벤트 수 반환)"""
        processed = 0

        for _ in range(max_events):
            if self.queue.empty():
                break

            try:
                event = self.queue.get_nowait()
                if event.type in self.handlers:
                    for handler in self.handlers[event.type]:
                        try:
                            handler(event)
                        except Exception as e:
                            self.stats["handler_errors"] += 1
                            logging.error(f"이벤트 핸들러 실행 실패: {str(e)}")
                            logging.error(f"이벤트: {event.type.value}, 소스: {event.source}")

                self.queue.task_done()
                processed += 1
                self.stats["events_processed"] += 1

            except Exception as e:
                logging.error(f"이벤트 처리 중 오류: {str(e)}")

        return processed

    def get_stats(self) -> Dict[str, Any]:
        """이벤트 큐 통계 반환"""
        return {
            **self.stats,
            "queue_size": self.queue.qsize(),
            "registered_handlers": sum(len(handlers) for handlers in self.handlers.values())
        }

    def clear(self):
        """이벤트 큐 비우기"""
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except:
                pass


# ===== Observer Pattern =====

class Observer:
    """Observer 인터페이스"""

    def on_state_change(self, old_state: str, new_state: str):
        """상태 변경 시 호출"""
        pass

    def on_event(self, event: Event):
        """이벤트 발생 시 호출"""
        pass


class Observable:
    """관찰 가능한 객체"""

    def __init__(self):
        self.observers: List[Observer] = []
        self.lock = Lock()

    def add_observer(self, observer: Observer):
        """Observer 추가"""
        with self.lock:
            if observer not in self.observers:
                self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Observer 제거"""
        with self.lock:
            if observer in self.observers:
                self.observers.remove(observer)

    def notify_observers(self, event: Event):
        """모든 Observer에게 이벤트 알림"""
        with self.lock:
            for observer in self.observers:
                try:
                    observer.on_event(event)
                except Exception as e:
                    logging.error(f"Observer 알림 실패: {str(e)}")


# ===== State Machine =====

class StateMachine(Observable):
    """상태 머신 기본 클래스"""

    def __init__(self, initial_state: str):
        super().__init__()  # Observable 초기화
        self.current_state = initial_state
        self.previous_state = None
        self.state_history: List[Dict[str, Any]] = []
        self.transition_handlers: Dict[str, Callable] = {}
        self.state_handlers: Dict[str, Callable] = {}

    def change_state(self, new_state: str, data: Dict[str, Any] = None):
        """상태 변경"""
        if new_state != self.current_state:
            old_state = self.current_state
            self.previous_state = old_state
            self.current_state = new_state

            # 상태 변경 이벤트 발생
            self.on_state_change(old_state, new_state, data)

            # 상태별 핸들러 실행
            if new_state in self.state_handlers:
                try:
                    self.state_handlers[new_state](data)
                except Exception as e:
                    logging.error(f"상태 핸들러 실행 실패: {str(e)}")

    def on_state_change(self, old_state: str, new_state: str, data: Dict[str, Any] = None):
        """상태 변경 시 호출 (하위 클래스에서 오버라이드)"""
        # 상태 변경 기록
        self.state_history.append({
            "timestamp": time.time(),
            "old_state": old_state,
            "new_state": new_state,
            "data": data
        })

        # 최근 100개만 유지
        if len(self.state_history) > 100:
            self.state_history = self.state_history[-100:]

        # Observer들에게 상태 변경 알림
        for observer in self.observers:
            try:
                observer.on_state_change(old_state, new_state)
            except Exception as e:
                logging.error(f"Observer 상태 변경 알림 실패: {str(e)}")

    def register_state_handler(self, state: str, handler: Callable):
        """상태별 핸들러 등록"""
        self.state_handlers[state] = handler

    def register_transition_handler(self, from_state: str, to_state: str, handler: Callable):
        """상태 전환별 핸들러 등록"""
        key = f"{from_state}->{to_state}"
        self.transition_handlers[key] = handler

    def get_state_info(self) -> Dict[str, Any]:
        """현재 상태 정보 반환"""
        return {
            "current_state": self.current_state,
            "previous_state": self.previous_state,
            "state_history_count": len(self.state_history),
            "registered_states": list(self.state_handlers.keys()),
            "registered_transitions": list(self.transition_handlers.keys())
        }


# ===== Event Handler Base =====

class EventHandler:
    """이벤트 핸들러 기본 클래스"""

    def __init__(self, event_queue: EventQueue, name: str = "Unknown"):
        self.event_queue = event_queue
        self.name = name
        self.enabled = True
        self.handler_stats = {
            "events_processed": 0,
            "errors": 0,
            "last_processed": None
        }

    def register_handlers(self):
        """이벤트 핸들러 등록 (하위 클래스에서 구현)"""
        pass

    def process_event(self, event: Event):
        """이벤트 처리 (하위 클래스에서 구현)"""
        pass

    def on_event(self, event: Event):
        """이벤트 수신 시 호출"""
        if not self.enabled:
            return

        try:
            self.process_event(event)
            self.handler_stats["events_processed"] += 1
            self.handler_stats["last_processed"] = time.time()
        except Exception as e:
            self.handler_stats["errors"] += 1
            logging.error(f"핸들러 {self.name} 이벤트 처리 실패: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """핸들러 통계 반환"""
        return {
            "name": self.name,
            "enabled": self.enabled,
            **self.handler_stats
        }

    def enable(self):
        """핸들러 활성화"""
        self.enabled = True

    def disable(self):
        """핸들러 비활성화"""
        self.enabled = False


# ===== Event System Manager =====

class EventSystemManager:
    """이벤트 시스템 전체 관리"""

    def __init__(self):
        self.event_queue = EventQueue()
        self.handlers: List[EventHandler] = []
        self.observables: List[Observable] = []
        self.running = False
        self.event_thread = None

    def add_handler(self, handler: EventHandler):
        """이벤트 핸들러 추가"""
        if handler not in self.handlers:
            self.handlers.append(handler)
            handler.register_handlers()

    def remove_handler(self, handler: EventHandler):
        """이벤트 핸들러 제거"""
        if handler in self.handlers:
            self.handlers.remove(handler)

    def add_observable(self, observable: Observable):
        """관찰 가능한 객체 추가"""
        if observable not in self.observables:
            self.observables.append(observable)

    def start(self):
        """이벤트 시스템 시작"""
        if self.running:
            return

        self.running = True
        self.event_thread = Thread(target=self._event_processing_loop, daemon=True)
        self.event_thread.start()
        logging.info("이벤트 시스템 시작됨")

    def stop(self):
        """이벤트 시스템 중지"""
        self.running = False
        if self.event_thread and self.event_thread.is_alive():
            self.event_thread.join(timeout=1.0)
        logging.info("이벤트 시스템 중지됨")

    def _event_processing_loop(self):
        """이벤트 처리 루프"""
        while self.running:
            try:
                self.event_queue.process_events()
                time.sleep(0.01)  # CPU 사용량 최소화
            except Exception as e:
                logging.error(f"이벤트 처리 루프 오류: {str(e)}")
                time.sleep(0.1)

    def get_system_stats(self) -> Dict[str, Any]:
        """시스템 전체 통계 반환"""
        return {
            "running": self.running,
            "event_queue": self.event_queue.get_stats(),
            "handlers": [handler.get_stats() for handler in self.handlers],
            "observables_count": len(self.observables)
        }

    def shutdown(self):
        """시스템 종료"""
        self.stop()
        self.event_queue.clear()
        logging.info("이벤트 시스템 종료됨")


# ===== Utility Functions =====

def create_event(event_type: EventType, data: Dict[str, Any] = None, source: str = "System") -> Event:
    """이벤트 생성 유틸리티"""
    return Event(
        type=event_type,
        data=data or {},
        timestamp=time.time(),
        source=source
    )


def log_event(event: Event, level: str = "INFO"):
    """이벤트 로깅 유틸리티"""
    log_message = f"[{event.type.value}] {event.source}: {event.data}"

    if level.upper() == "DEBUG":
        logging.debug(log_message)
    elif level.upper() == "INFO":
        logging.info(log_message)
    elif level.upper() == "WARNING":
        logging.warning(log_message)
    elif level.upper() == "ERROR":
        logging.error(log_message)
    else:
        logging.info(log_message)
