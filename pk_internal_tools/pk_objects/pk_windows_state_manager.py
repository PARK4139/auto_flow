import logging
import threading
from typing import List, Tuple, Optional

# Lazy import for get_windows_opened
_get_windows_opened_func = None


class PkWindowsStateManager:
    """
    열려 있는 윈도우 목록의 상태를 관리하고, 백그라운드에서 주기적으로 업데이트하며,
    빠르게 조회할 수 있는 기능을 제공하는 클래스입니다.
    """

    def __init__(self):
        self._windows_cache: List[Tuple[int, str]] = []
        self._cache_lock = threading.Lock()
        self._updater_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lazy_import_get_windows_opened_once = False  # get_windows_opened 임포트가 한 번만 되도록

    def _lazy_import_get_windows_opened(self):
        """get_windows_opened를 한 번만 임포트합니다."""
        global _get_windows_opened_func
        if not self._lazy_import_get_windows_opened_once:
            if _get_windows_opened_func is None:
                try:
                    from pk_internal_tools.pk_functions.get_windows_opened_raw import get_windows_opened_raw
                    _get_windows_opened_func = get_windows_opened_raw
                except ImportError as e:
                    logging.error(f"Failed to import get_windows_opened: {e}")
                    raise
            self._lazy_import_get_windows_opened_once = True

    def ensure_windows_opened_db_updated(self, update_interval_seconds: float = 0.5) -> None:
        """
        백그라운드에서 주기적으로 열려 있는 윈도우 목록을 업데이트하여 메모리 캐시에 저장합니다.
        이 메서드는 별도의 스레드에서 실행되어야 합니다.
        """
        self._lazy_import_get_windows_opened()
        if _get_windows_opened_func is None:
            logging.error("get_windows_opened function is not available. Cannot update cache.")
            return

        logging.info("윈도우 캐시 업데이트 스레드 시작.")
        while not self._stop_event.is_set():
            try:
                current_windows = _get_windows_opened_func(return_hwnds=True, limit=None)
                sorted_current_windows = sorted(current_windows) # 현재 윈도우 목록을 정렬하여 비교 일관성 확보
                
                with self._cache_lock:
                    sorted_cached_windows = sorted(self._windows_cache) # 캐시된 윈도우 목록을 정렬
                    
                    if sorted_current_windows != sorted_cached_windows: # 두 목록이 다를 경우에만 업데이트
                        self._windows_cache.clear()
                        self._windows_cache.extend(current_windows)
                        # logging.debug(f"윈도우 캐시 업데이트 완료. 현재 윈도우 수: {len(self._windows_cache)}")
                    else:
                        # logging.debug("윈도우 상태 변경 없음. 캐시 업데이트 건너뜀.")
                        pass
            except Exception as e:
                logging.error(f"윈도우 캐시 업데이트 중 오류 발생: {e}")

            self._stop_event.wait(update_interval_seconds)
        logging.info("윈도우 캐시 업데이트 스레드 종료.")

    def get_windows_opened_from_db(self) -> List[Tuple[int, str]]:
        """
        메모리 캐시에서 현재 열려 있는 윈도우 목록을 조회합니다.
        이 메서드는 매우 빠르게 동작합니다.
        """
        with self._cache_lock:
            return list(self._windows_cache)  # Return a copy to prevent external modification

    def ensure_windows_updater_started(self, update_interval_seconds: float = 0.5) -> None:
        """
        윈도우 캐시 업데이트 스레드를 시작합니다.
        """
        if self._updater_thread is None or not self._updater_thread.is_alive():
            self._stop_event.clear()
            self._updater_thread = threading.Thread(
                target=self.ensure_windows_opened_db_updated,
                args=(update_interval_seconds,),
                daemon=True  # Daemon thread exits when main program exits
            )
            self._updater_thread.start()
            logging.info("윈도우 캐시 업데이트 스레드가 백그라운드에서 시작되었습니다.")
        else:
            logging.info("윈도우 캐시 업데이트 스레드가 이미 실행 중입니다.")

    def ensure_windows_updater_stopped(self) -> None:
        """
        윈도우 캐시 업데이트 스레드를 중지합니다.
        """
        if self._updater_thread and self._updater_thread.is_alive():
            self._stop_event.set()
            self._updater_thread.join(timeout=5)  # Wait for the thread to finish
            if self._updater_thread.is_alive():
                logging.warning("윈도우 캐시 업데이트 스레드가 5초 내에 종료되지 않았습니다.")
            else:
                logging.info("윈도우 캐시 업데이트 스레드가 성공적으로 종료되었습니다.")
            self._updater_thread = None
        else:
            logging.info("윈도우 캐시 업데이트 스레드가 실행 중이 아닙니다.")

    def is_window_title_db_thread_executed(self) -> bool:
        """
        백그라운드 윈도우 업데이트 스레드가 현재 실행 중인지 확인합니다.
        """
        return self._updater_thread is not None and self._updater_thread.is_alive()


# 모듈 레벨에서 PkWindowsStateManager 인스턴스를 생성하여 싱글톤처럼 사용
pk_windows_state_manager = PkWindowsStateManager()

# 기존 함수명과 동일하게 모듈 레벨에서 메서드를 노출 (선택 사항, 직접 pk_windows_state_manager.메서드명 호출도 가능)
# ensure_windows_opened_db_updated = pk_windows_state_manager.ensure_windows_opened_db_updated
# get_windows_opened_from_db = pk_windows_state_manager.get_windows_opened_from_db
# ensure_windows_updater_started = pk_windows_state_manager.ensure_windows_updater_started
# ensure_windows_updater_stopped = pk_windows_state_manager.ensure_windows_updater_stopped
# is_window_title_db_thread_executed = pk_windows_state_manager.is_window_title_db_thread_executed
# -> 객체지향적인 느낌이 들지 않아서 코드스타일 개인적으로 별로였다.
# -> 레거시 코드를 수정할 수 없다면 이 방법은 괜찮은 방법 -> 하지만 스파게티 될듯