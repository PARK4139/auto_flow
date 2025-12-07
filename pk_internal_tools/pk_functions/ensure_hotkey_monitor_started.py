"""
백그라운드 단축키 모니터링 시스템
매번 새로 시작하는 대신 백그라운드에서 대기하다가 단축키가 눌리면 즉시 실행
"""

import keyboard
import threading
import subprocess
import os
import time
from typing import Optional, Callable

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed import ensure_pk_wrapper_starter_executed
import logging
from pk_internal_tools.pk_objects.pk_directories import d_pk_root


class HotkeyMonitor:
    """백그라운드 단축키 모니터링 클래스"""
    
    def __init__(self, hotkey: str = "ctrl+alt+p", python_path: Optional[str] = None):
        self.hotkey = hotkey
        self.is_running = False
        self.monitor_thread = None

    def start_monitoring(self):
        """백그라운드 모니터링 시작"""
        if self.is_running:
            logging.debug(f"️ 이미 모니터링이 실행 중입니다.")
            return
            
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logging.debug(f"단축키 모니터링 시작: {self.hotkey}")
        logging.debug(f"백그라운드에서 대기 중... (Ctrl+C로 종료)")
        
    def stop_monitoring(self):
        """모니터링 중지"""
        self.is_running = False
        keyboard.unhook_all()
        logging.debug(f"단축키 모니터링 중지됨")
        
    def _monitor_loop(self):
        """백그라운드 모니터링 루프"""
        try:
            # 단축키 등록
            keyboard.add_hotkey(self.hotkey, self._execute_pk_system, suppress=True)
            
            # 모니터링 루프
            while self.is_running:
                time.sleep(0.1)  # CPU 사용량 최소화
                
        except Exception as e:
            logging.debug(f"모니터링 오류: {e}")
        finally:
            keyboard.unhook_all()
            
    def _execute_pk_system(self):
        """pk_system 실행 (최적화된 버전)"""
        try:
            logging.debug(f"단축키 감지됨! pk_system 실행 중...")
            
            # 실행 시간 측정
            start_time = time.time()
            
            # 최적화된 실행 명령어
            # cmd = [
            #     self.python_path,
            #     self.target_script
            # ]
            #
            # # 백그라운드에서 실행 (UI 블로킹 방지)
            # process = subprocess.Popen(
            #     cmd,
            #     cwd=d_pk_system,
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE,
            #     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            # )

            ensure_pk_wrapper_starter_executed()

            execution_time = time.time() - start_time
            logging.debug(f"실행 완료 (시작 시간: {execution_time:.3f}초)")
            
        except Exception as e:
            logging.debug(f"실행 오류: {e}")


def ensure_hotkey_monitor_started(hotkey: str, auto_start: bool = True):
    """
    백그라운드 단축키 모니터링 시작
    
    Args:
        hotkey: 모니터링할 단축키 (기본값: ctrl+alt+p)
        auto_start: 자동으로 모니터링 시작 여부
    """
    monitor = HotkeyMonitor(hotkey=hotkey)
    
    if auto_start:
        monitor.start_monitoring()
        
        # 메인 스레드에서 Ctrl+C 대기
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            logging.debug(f"모니터링 종료됨")
    
    return monitor


def ensure_hotkey_monitor_as_service():
    """서비스 모드로 백그라운드 실행"""
    import sys
    
    # 서비스 모드 설정
    if len(sys.argv) > 1:
        hotkey = sys.argv[1]
    else:
        hotkey = "ctrl+alt+p"
    
    logging.debug(f"서비스 모드 시작: {hotkey}")
    ensure_hotkey_monitor_started(hotkey=hotkey, auto_start=True)



