from watchdog.events import FileSystemEventHandler
import logging


class FileChangeHandler(FileSystemEventHandler):
    """파일 변경 감지 핸들러 클래스"""
    
    def __init__(self, observer, change_cnt_limit=None):
        super().__init__()
        self.observer = observer  # Observer 인스턴스를 받아 저장
        self.f_changed_list = []
        self.f_change_level = 0
        self.change_cnt_limit = change_cnt_limit

    def on_created(self, event):
        """파일 생성 이벤트 처리"""
        logging.debug(f"f_created={event.src_path}")
        self.f_changed_list.append(event.src_path)
        self.f_change_level += 1
        self.check_limit()

    def on_deleted(self, event):
        """파일 삭제 이벤트 처리"""
        logging.debug(f"f_deleted={event.src_path}")
        self.f_changed_list.append(event.src_path)
        self.f_change_level += 1
        self.check_limit()

    def on_modified(self, event):
        """파일 수정 이벤트 처리"""
        logging.debug(f"f_modified={event.src_path}")
        self.f_changed_list.append(event.src_path)
        self.f_change_level += 1
        self.check_limit()

    def check_limit(self):
        """변경 제한 확인 및 Observer 중지"""
        if self.change_cnt_limit is not None and self.f_change_level >= self.change_cnt_limit:
            logging.debug("Change limit reached. Stopping observer.")
            self.observer.stop()  # Stop the observer instead of raising an exception
