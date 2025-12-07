import subprocess
import textwrap
import threading
from dataclasses import dataclass
from typing import Callable, Optional, Dict, Any

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_magnets_collected_from_nyaa_si import ensure_magnets_collected_from_nyaa_si
from pk_internal_tools.pk_functions.ensure_target_found import ensure_target_file_system_scanned
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.ensure_windows_minimized import ensure_windows_minimized
from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
from pk_internal_tools.pk_functions.get_length_of_str import get_length_of_str
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
from pk_internal_tools.pk_objects.pk_losslesscut import PkLosslesscut
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers
from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE


@dataclass
class TimeRange:
    """시간 구간 데이터 클래스"""
    start_time: str
    end_time: str
    duration_minutes: int
    name: str
    routine_func: Callable
    executed: bool = False


class PkScheduler:
    """스케줄링의 모든 로직과 데이터를 캡슐화한 싱글턴 클래스"""

    _instance: Optional['PkScheduler'] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, state_file: Optional[str] = None, speak_mode: bool = True):
        import logging
        import asyncio
        import datetime
        import threading
        from pathlib import Path
        from typing import List, Optional

        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForEnsureSlept

        from pk_internal_tools.pk_functions.ensure_routine_startup_enabled import ensure_routine_startup_enabled

        from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADED_FROM_TORRENT

        is_initialized = hasattr(self, '_initialized') and self._initialized
        settings_changed = False
        self.state_file = None  # pk_checkpoint
        self.speak_mode = speak_mode
        if is_initialized:
            if self.state_file != state_file or self.speak_mode != speak_mode:
                settings_changed = True
                logging.info("스케줄러 설정이 변경되어 재초기화를 진행합니다.")
                if self.is_running:
                    self.stop()

        if not is_initialized or settings_changed:
            self.speak_mode = speak_mode

            if state_file:
                self.state_file = Path(state_file)
            else:
                from pk_internal_tools.pk_objects.pk_files import F_SCHEDULER_STATE
                self.state_file = F_SCHEDULER_STATE

            self.time_ranges: List[TimeRange] = []
            self.current_routine: Optional[TimeRange] = None
            self.is_running = False
            self.demo_start_time: Optional[datetime.datetime] = None
            self.loop: Optional[asyncio.AbstractEventLoop] = None
            self.thread: Optional[threading.Thread] = None
            self.completion_logger: Optional[logging.Logger] = None
            self._initialized = True
            self.define_routines()
            logging.info(f"PkScheduler가 초기화되었습니다, 음성: {self.speak_mode}, 상태파일: {self.state_file})")
            if self.speak_mode:
                from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
                from pk_internal_tools.pk_functions.ensure_losslescut_killed import ensure_losslescut_killed

                from pk_internal_tools.pk_functions.ensure_potplayer_killed import ensure_potplayer_killed

                # pk_* -> life schedule entry point
                # ensure_spoken("pk 스케줄러가 시작되었습니다.")
                logging.debug("pk life assistance is started")

                ensure_windows_minimized()

                # initialize media_file_controller
                d_working = D_DOWNLOADED_FROM_TORRENT

                # selection_mode를 사용자에게 선택받도록 추가
                from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
                from pk_internal_tools.pk_objects.pk_system_operation_options import PlayerSelectionMode, SetupOpsForEnsureValueCompleted20251130
                from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_30 import ensure_value_completed_2025_11_30

                func_n = get_caller_name()

                selection_mode_options = [member.value.lower() for member in PlayerSelectionMode]
                selected_mode_str = ensure_value_completed_2025_11_30(
                    key_name="player_selection_mode",
                    func_n=func_n,
                    guide_text="플레이어 파일 선택 모드를 선택하세요:",
                    options=selection_mode_options,
                    sort_order=SetupOpsForEnsureValueCompleted20251130.HISTORY
                )

                selected_selection_mode = PlayerSelectionMode[selected_mode_str.upper()] if selected_mode_str else PlayerSelectionMode.AUTO

                self.pk_losslesscut = PkLosslesscut(d_working=d_working, selection_mode=selected_selection_mode)

                # ensure_python_file_executed_advanced(file_path=d_pk_wrappers / 'pk_ensure_pk_log_editable.py')
                ensure_routine_startup_enabled()

                logging.info("========== 등록된 일정 ==========")
                for start, end, name, _ in self.schedules:
                    logging.info(f"- {start} ~ {end}: {name}")
                logging.info("===================================")

                ensure_slept(seconds=3, setup_op=SetupOpsForEnsureSlept.SILENT)

    def define_routines(self):
        import traceback
        import logging
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        from pk_internal_tools.pk_functions.ensure_os_locked_at_sleeping_time import ensure_os_locked_at_sleeping_time
        from pk_internal_tools.pk_functions.ensure_losslescut_killed import ensure_losslescut_killed
        from pk_internal_tools.pk_functions.ensure_potplayer_killed import ensure_potplayer_killed
        from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.ensure_sound_file_executed import ensure_sound_file_executed
        from pk_internal_tools.pk_functions.ensure_window_to_front_of_pycharm import ensure_pycharm_window_to_front

        @self._routine_decorator
        def do_routine_rest():
            try:
                self.speak_routine_start(self.current_routine.name)
                ensure_potplayer_killed()

                # 비디오 이어서 재생
                # if self.pk_losslesscut.current_state == "not_initialized":
                #     self.pk_losslesscut.ensure_media_file_controller_reopened()
                # if not self.pk_losslesscut.is_video_loaded_already(loop_cnt=0):
                #     self.pk_losslesscut.ensure_video_file_loaded_on_media_file_controller(file_to_play=self.pk_losslesscut.f_media_to_load)
                # self.pk_losslesscut.ensure_media_file_controller_play_button_pressed()
                # self.pk_losslesscut.ensure_media_file_controller_screen_maximized()

                file_to_execute = d_pk_wrappers / "pk_ensure_target_files_played_on_losslesscut_auto.py"
                subprocess.Popen(
                    [F_UV_PYTHON_EXE, file_to_execute],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )

            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_routine_dinner():
            try:
                self.speak_routine_start(self.current_routine.name)

                # 즐거운노래
                ensure_sound_file_executed()
                ensure_slept(milliseconds=77)

            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_routine_go_to_sleep():
            try:
                self.speak_routine_start(self.current_routine.name)

                # 즐거운노래
                ensure_sound_file_executed()
                ensure_slept(milliseconds=77)

                ensure_os_locked_at_sleeping_time()


            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_routine_work():
            try:
                self.speak_routine_start(self.current_routine.name)
                # self._ensure_resource_not_necessary_to_routine_removed()

                # video stop
                # if self.lossclescut.is_video_played():
                #     self.lossclescut.ensure_video_toogled_between_pause_and_play()
                #
                # if self.potplayer.is_video_played():
                #     self.potplayer.ensure_video_toogled_between_pause_and_play()
                ensure_losslescut_killed()
                ensure_potplayer_killed()
                # ensure_slept(milliseconds=77) # TODO loop 함수 만들어서 조건 충족하지 못하면 10 milliseconds slept 하는 쪽이 속도면에서는 빠를것. 다만 CPU 측면에서는 많은 리소스를 사용해야 할것임.

                # 노동요
                ensure_sound_file_executed()
                found_potplayer = False
                while 1:
                    for window_title in get_windows_opened():
                        if "팟플레이어" in window_title:
                            logging.debug(f'팟플레이어 창 발견')
                            found_potplayer = True
                            break
                    if found_potplayer == True:
                        break

                # 코드 작성 유도
                ensure_pycharm_window_to_front()
            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_routine_lunch():
            try:
                self.speak_routine_start(self.current_routine.name)
                #     n. 락스희석액 붓기
                #     n. 가방에 넣기
            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_morning_tutorial():
            try:
                self.speak_routine_start(self.current_routine.name)

                ensure_target_file_system_scanned()

                animation_title_keyword = ''
                nyaa_si_supplier = 'SubsPlease'
                resolution_keyword = '1080'
                driver = get_selenium_driver(headless_mode=False)
                pages = 10
                ensure_magnets_collected_from_nyaa_si(animation_title_keyword=animation_title_keyword, nyaa_si_supplier=nyaa_si_supplier, resolution_keyword=resolution_keyword, driver=driver, pages=pages)

                # pk_* -> morning tutorial
                guide_text = textwrap.dedent(rf'''
                    # {self.current_routine.name} 튜토리얼 (Tip : 수행하기 곤란하다면, 쉬운일부터 수행하세요)
                    n. 매트리스 개기
                    n. 가글양치/혀양치         # -> 가글액 양치->구강 세균 저감-> GOOD  
                    n. 물가글
                    n. 로션   
                    n. 세수               
                    n. 머리감기                # -> 가능한 빨리 말리기 -> 머리건강 -> GOOD               
                    n. 로션  
                    n. 머리말리기
                    n. 로션  
                    n. 화장실                  # -> 가능하면 집에서 해결 -> 밖에서 안할 수 있음 -> GOOD 
                    n. 팬티 환복               # -> 쾌적 -> GOOD
                     
                    n. 벽 카프레이즈 22회      # -> 발 사이에 테니스공 유지한채로 # 방에서 수행
                    n. 벽 흉추 스트레칭        # -> 등을 뒤로 기대고 -> 윗방향으로 손등 벽대기 -> 아래방향으로 손끝 벽대기 ->흉추 relax-> GOOD
                    n. 등근육 풀기             # -> 벽 앞에 선다 -> 깍지끼고 뒷통수 뼈 감싼채로 -> 테니스공 발에 끼고 -> 까치발 -> 벽에 팔꿈치로 기대기
                    n. 좌우로 광배근 늘리기 스트레칭
                    n. 벽 푸쉬업 22회          # -> 발 사이에 테니스공 유지한채로 
                    n. 바닥 푸쉬업 22회        # -> 발 사이에 테니스공 유지한채로 
                    n. 벽 흉추 스트레칭 
                    n. 벽 카프레이즈 22회      # -> 발 사이에 테니스공 유지한채로 # 방에서 수행
                    n. 물 120 ml               # -> 물섭취-> 물컵설거지 -> 물 2소분 하여 냉장고로 이동 -> GOOD
                      
                    n. 손톱깍기                # -> 바닥 손톱 버리기-> 청소-> GOOD
                    n. 청소기 돌리기           # -> 조금이라도
                    n. 빨래                    # -> 빨래할게 있다면 ->수행
                    n. 아침식사                # -> 배고프기 전->수행 -> 계란, 키위, 블루베리 
                    n. 물가글 
                    n. 하늘이 산책             # -> 오늘이 주말 ->수행
                    n. 외출전준비              # -> 키보드 챙기기
                    n. 도시락 1개 이동         # -> 냉장고에서 가방으로
                    n. 양말신기                # -> 외출 직전에서 -> GOOD
                    n. 물컵 이동               # -> 살균소에서 가방으로
                
                    TODO daily
                    n. 헤어에센스
                    n. 케틀벨 8kg 22회
                    n. 선풍기로 방환기 1분 이상  
                    n. 프로폴리스 한알
                    n. 평행봉 잡은채로 좌우로 다리흔들기       # 테니스공 또는 곽티슈 발로 잡은채로  
                    
                    TODO next spring
                    
                    TODO next summer
                    
                    TODO next autoum  
                    n. 점빼기
                    
                    TODO next winter  
                    
                    #  어제의 나의 말을 오늘의 나에게
                    n. 언어행동이 나의 기분을 결정한다. # 작은 일에도 쉽게 욕을 하는 나의 언어행동은 나의 뇌 수행능력을 저하시킬지도 모른다, 
                    n. 뇌를 다시 프로그래밍을 해야한다. # 실패와 후회 등에 나의 뇌는 길들여저 있다
                    n. 긍정의 말을 나에게
                    n. 웃음을 나에게
                    n. 난 천재는 아닌걸 깨달았다.       # 별수 없다, 천재는 될수 없으니 `노력의 천재`가 되자
                    n. 지금부터 행복하게 살거야.        # 지금부터 새 인생인거야
                    n. 조금은 귀찮은 오늘도, 다신 오지 않을 오늘입니다.
                    n. code will make my life fun
                     
                ''')  # TODO : text = get_str_replaced_from_n_dot_to_ordered_number(text)
                logging.warning(f"튜토리얼에 {get_length_of_str(text=guide_text) - 1}개 TASK가 있어요")
                ensure_spoken("튜토리얼를 보면서 진행해주세요, 완료를 하시면 다음 일정으로 넘어 갈수 있어요")
                while True:
                    ensure_window_to_front(window_title_seg=get_current_console_title())
                    logging.warning(get_text_yellow(guide_text))
                    question = f'{self.current_routine.name} 수동 튜토리얼를 완료하셨나요?'
                    ok = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                    if ok != PkTexts.YES:
                        break
                    elif ok != PkTexts.YES:
                        ensure_spoken(f"{self.current_routine.name}을 수행하시는게 좋을것 같아요")
                        continue
            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_afternoon_tutorial():
            try:
                self.speak_routine_start(self.current_routine.name)
                # '물가글(혹시 구내염 있으시면 가글양치)', # 오후주간작업전준비
                # '양치 WITHOUT TOOTH PASTE', # 오후주간작업전준비
                # '양치 WITH TOOTH PASTE', # 오후주간작업전준비
                # '양치 WITH GARGLE', # 오후주간작업전준비
                # '물가글', # 오후주간작업전준비
                # '스트레칭 밴드 V 유지 런지 33개', # 오후주간작업전준비
                # '계단 스쿼트 33 개', # 오후주간작업전준비
                # '푸쉬업 33 개', # 오후주간작업전준비

                # '점심식사', # 오후주간작업전준비
                #     n. 락스희석액 붓기
                #     n. 가방에 넣기
                ensure_spoken(f"{self.current_routine.name} 준비 완료")
            except:
                ensure_debug_loged_verbose(traceback)

        @self._routine_decorator
        def do_evening_tutorial():
            try:
                self.speak_routine_start(self.current_routine.name)

                # pk_* -> evening tutorial
                guide_text = textwrap.dedent(rf'''
                    # {self.current_routine.name} 튜토리얼 (Tip : 수행하기 곤란하다면, 쉬운일부터 수행하세요)
                    
                    n. 저녁식사전 운동
                    
                    n. 저녁식사
                    
                    n. 씻기 
                    n. 환복
                    n. 도시락 설겆이 및 살균
                    n. 도시락 6개 준비 (6일 치)
                        n. 삶은 계란 
                        n. 삶은 서리태 
                        n. 냉동 키워
                        n. 주먹밥
                        n. 아로니아 + 블루베리 주스
                        n. 김치
                        n. 유산균
                        n. 홍삼
                        n. 쥐눈이콩 물
                        n. 콩스낵
                        n. 간식 많이 준비
                        n. 고산지유기농 바나나 후미후루
                        n. 3락 젓가락/숫가락/도시락 챙기기 ( move to 페브릭 도시락 가방)
                    n. 면도
                    n. 가글양치/혀양치  
                    n. 물가글 
                    n. 세수
                ''')
                logging.warning(f"튜토리얼에 {get_length_of_str(text=guide_text) - 1}개 TASK가 있어요")
                ensure_spoken("튜토리얼를 보면서 진행해주세요, 완료를 하시면 다음 일정으로 넘어 갈수 있어요")
                while True:
                    ensure_window_to_front(window_title_seg=get_current_console_title())
                    logging.warning(get_text_yellow(guide_text))
                    question = f'{self.current_routine.name} 수동 튜토리얼를 완료하셨나요?'
                    ok = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                    if ok != PkTexts.YES:
                        break
                    elif ok != PkTexts.YES:
                        ensure_spoken(f"{self.current_routine.name}을 수행하시는게 좋을것 같아요")
                        continue
            except:
                ensure_debug_loged_verbose(traceback)

        self.schedules = [
            ("07:00", "07:10", "휴식튜토리얼", do_routine_rest),
            ("07:10", "09:00", "07시 루틴 튜토리얼", do_morning_tutorial),
            ("09:00", "09:25", "작업시간", do_routine_work),
            ("09:25", "09:30", "휴식튜토리얼", do_routine_rest),
            ("09:30", "10:00", "작업시간", do_routine_work),
            ("10:00", "10:05", "휴식튜토리얼", do_routine_rest),
            ("10:05", "10:35", "작업시간", do_routine_work),
            ("10:35", "10:40", "휴식튜토리얼", do_routine_rest),
            ("10:40", "11:10", "작업시간", do_routine_work),
            ("11:10", "11:15", "휴식튜토리얼", do_routine_rest),
            ("11:15", "11:40", "작업시간", do_routine_work),
            ("12:40", "14:14", "휴식튜토리얼", do_routine_rest),
            ("14:14", "15:15", "14시 루틴 튜토리얼", do_afternoon_tutorial),  # TODO 운동튜토리얼 추가
            ("15:15", "15:20", "휴식튜토리얼", do_routine_rest),
            ("15:20", "15:50", "작업시간", do_routine_work),
            ("15:50", "15:55", "휴식튜토리얼", do_routine_rest),
            ("15:55", "16:25", "작업시간", do_routine_work),
            ("16:25", "16:30", "휴식튜토리얼", do_routine_rest),
            ("16:30", "17:00", "작업시간", do_routine_work),
            ("17:00", "17:05", "휴식튜토리얼", do_routine_rest),
            ("17:05", "17:17", "추가휴식튜토리얼", do_routine_rest),
            ("17:17", "18:25", "17시 루틴 튜토리얼", do_evening_tutorial),  # TODO 운동튜토리얼 추가
            ("18:25", "19:00", "휴식튜토리얼", do_routine_rest),
            ("19:00", "19:30", "작업시간", do_routine_work),
            ("19:30", "19:35", "휴식튜토리얼", do_routine_rest),
            ("19:35", "20:05", "작업시간", do_routine_work),
            ("20:05", "20:20", "휴식튜토리얼", do_routine_rest),
            ("20:20", "21:00", "20시 루틴 튜토리얼", do_routine_rest),
            ("21:00", "23:59", "자야할시간", do_routine_go_to_sleep),
            ("00:00", "05:00", "자야할시간", do_routine_go_to_sleep),
        ]

    def speak_routine_start(self, routine_title: str):
        import datetime
        import logging
        from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken

        if not self.speak_mode:
            return
        logging.info(f"{routine_title} 튜토리얼 실행")
        end_time_str = self.current_routine.end_time  # e.g., "07:10"
        duration = self.current_routine.duration_minutes
        dummy_date = datetime.date.today()
        end_datetime = datetime.datetime.strptime(f"{dummy_date.strftime('%Y-%m-%d')} {end_time_str}", "%Y-%m-%d %H:%M")
        formatted_end_time = end_datetime.strftime("%H시 %M분")
        now_datetime = datetime.datetime.now()
        time_difference = end_datetime - now_datetime
        remaining_duration_minutes = max(0, int(time_difference.total_seconds() / 60))
        text_to_speak = f"{routine_title}, {formatted_end_time}까지, {remaining_duration_minutes + 1}분 동안 진행해주세요"
        logging.debug(f"text_to_speak='{text_to_speak}'")
        try:
            ensure_spoken(text_to_speak, wait=True)
        finally:
            # ensure_spoken(speech_text)
            ensure_spoken(wait=True)

    def _routine_decorator(self, func: Callable) -> Callable:

        from functools import wraps

        """튜토리얼 함수에 공통 로직(완료 로깅)을 적용하는 데코레이터"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if self.completion_logger:
                self.completion_logger.info(f"튜토리얼 실행 완료: {func.__name__}")
            return result

        return wrapper

    def _setup_completion_logger(self):

        from pathlib import Path

        import logging

        if not self.demo_start_time:
            return
        try:
            from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
        except ImportError:
            logging.warning("d_pk_logs import 실패")
            return

        start_time_str = self.demo_start_time.strftime('%Y_%m_%d_%H%M%S')
        log_filename = Path(d_pk_logs) / f"pk_schedule_executed_at_{start_time_str}.log"
        logger = logging.getLogger(f'routine_completion_{id(self)}')
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        if not logger.handlers:
            handler = logging.FileHandler(log_filename, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self.completion_logger = logger

    def _load_execution_state(self) -> set:
        import json
        from datetime import date

        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                today_str = str(date.today())
                return {name for name, exec_date in state_data.items() if exec_date == today_str}
        except (IOError, json.JSONDecodeError):
            return set()
        return set()

    def _save_execution_state(self, routine_name: str):
        import traceback

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

        import json
        from datetime import date

        import logging

        try:
            try:
                if self.state_file.exists():
                    with open(self.state_file, 'r', encoding='utf-8') as f:
                        state_data = json.load(f)
                else:
                    state_data = {}
            except (IOError, json.JSONDecodeError):
                state_data = {}

            today_str = str(date.today())
            state_data[routine_name] = today_str

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=4)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"튜토리얼 상태 파일 저장 실패")
            ensure_debug_loged_verbose(traceback)

    def _prepare_routines(self):

        import datetime

        self.time_ranges.clear()
        # Always reset executed status on scheduler startup to ensure routines run.
        for start, end, name, func in self.schedules:
            time_format = "%H:%M"
            start_time = datetime.datetime.strptime(start, time_format)
            end_time = datetime.datetime.strptime(end, time_format)
            duration_minutes = int((end_time - start_time).total_seconds() / 60)
            time_range = TimeRange(start, end, duration_minutes, name, func)
            time_range.executed = False  # Force executed to False on startup
            self.time_ranges.append(time_range)

    def _ensure_resource_not_necessary_to_routine_removed(self):

        # 작업 튜토리얼에 불 필요한 리소스 제거
        # from pk_internal_tools.pk_functions import ensure_slept

        # ensure_slept(milliseconds=77)
        # ensure_potplayer_killed()
        # ensure_slept(milliseconds=77)
        pass

    def get_current_time_range(self) -> Optional[TimeRange]:

        import datetime

        """현재 시간에 맞는 튜토리얼을 찾습니다"""
        now = datetime.datetime.now()

        # 실제 모드: 현재 시간으로 계산
        current_time_str = now.strftime("%H:%M")
        for time_range in self.time_ranges:
            if time_range.start_time <= current_time_str < time_range.end_time:
                return time_range
        return None

    async def _execute_routine(self, time_range: TimeRange):
        import traceback

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

        import asyncio

        import logging

        logging.debug(f"Attempting to execute: {time_range.name}, initial executed: {time_range.executed}")
        if time_range.executed:
            logging.debug(f"Routine {time_range.name} already executed, returning.")
            return
        try:
            logging.info(f"튜토리얼 실행 시작: {time_range.name}")
            logging.debug(f"Calling routine={time_range.routine_func.__name__}()")
            await asyncio.get_event_loop().run_in_executor(None, time_range.routine_func)
            logging.debug(f"Routine function {time_range.routine_func.__name__} completed.")
            time_range.executed = True
            logging.debug(f"Set {time_range.name}.executed to True.")
            self._save_execution_state(time_range.name)
            logging.debug(f"Saved execution state for {time_range.name}.")
        except:
            logging.error(f"튜토리얼 실행 실패 {time_range.name}")
            ensure_debug_loged_verbose(traceback)

    async def _main_loop(self):
        import traceback

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

        import asyncio
        import datetime

        import logging

        while self.is_running:
            try:
                current_range = self.get_current_time_range()

                # Debugging: Log current_range and self.current_routine
                # logging.debug(f"current_range: {current_range.routine_name if current_range else 'None'}, executed: {current_range.executed if current_range else 'N/A'}")
                # logging.debug(f"self.current_routine: {self.current_routine.routine_name if self.current_routine else 'None'}")

                # Update current_routine if it has changed
                if current_range != self.current_routine:
                    if current_range:
                        now = datetime.datetime.now()
                        current_time_str = now.strftime("%H:%M:%S")
                        logging.info(f"현재 튜토리얼 변경: {current_range.name} ({current_range.start_time}-{current_range.end_time}) - 현재 시간: {current_time_str} - 함수: {current_range.routine_func.__name__}")
                    self.current_routine = current_range

                # Attempt to execute the current routine if it exists and hasn't been executed today
                if current_range and not current_range.executed:
                    logging.debug(f"Executing routine: {current_range.name}, executed status: {current_range.executed}")
                    await self._execute_routine(current_range)
                else:
                    # logging.debug(f"Not executing routine. current_range: {current_range.routine_name if current_range else 'None'}, executed: {current_range.executed if current_range else 'N/A'}")
                    pass

                # pk_option
                # await asyncio.sleep(1)
                await asyncio.sleep(20)  # 부하를 줄이기 위해 sleep time 을 1에서 20으로 증가
                # logging.debug(f"pk_flow_assistance loop is working")
            except:
                ensure_debug_loged_verbose(traceback)
                await asyncio.sleep(5)

    def _run_in_thread(self):
        import traceback

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

        import asyncio
        import datetime

        import logging

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.is_running = True
        if not self.demo_start_time:
            self.demo_start_time = datetime.datetime.now()
        self._setup_completion_logger()
        try:
            self.loop.run_until_complete(self._main_loop())
        except RuntimeError as e:
            if "Event loop stopped before Future completed" in str(e):
                logging.debug("이벤트 루프가 정상적으로 중지되었습니다.")
            else:
                logging.error(f"스케줄러 스레드에서 예기치 않은 런타임 오류 발생")
                ensure_debug_loged_verbose(traceback)

    def start(self):

        import threading

        import logging

        if self.thread and self.thread.is_alive():
            logging.info("기존 스케줄러 스레드를 중지하고 재시작합니다.")
            self.stop()

        self._prepare_routines()
        self.thread = threading.Thread(target=self._run_in_thread, daemon=True)
        self.thread.start()

    def stop(self):

        import logging

        if not self.is_running:
            return
        self.is_running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        logging.info("스케줄러가 중지되었습니다.")

    def get_status(self) -> Dict[str, Any]:

        progress = {}
        # if self.demo_mode and self.demo_start_time:
        #     elapsed_seconds = (datetime.datetime.now() - self.demo_start_time).total_seconds()
        #     total_duration_minutes = sum(r.duration_minutes for r in self.time_ranges)
        #     total_duration_seconds_in_demo = total_duration_minutes / 10
        #
        #     progress_percent = min(100, (elapsed_seconds / total_duration_seconds_in_demo) * 100) if total_duration_seconds_in_demo > 0 else 0
        #     progress = {
        #         "elapsed_seconds": elapsed_seconds,
        #         "total_duration_in_demo_seconds": total_duration_seconds_in_demo,
        #         "progress_percent": progress_percent,
        #     }

        return {
            "is_running": self.is_running,
            "current_routine": self.current_routine.name if self.current_routine else None,
            "total_ranges": len(self.time_ranges),
            "executed_ranges": sum(1 for r in self.time_ranges if r.executed),
            "speak_mode": self.speak_mode,
            "state_file": str(self.state_file),
            "demo_progress": progress
        }


def get_pk_flow_assistance(state_file: Optional[str] = None, speak_mode: bool = True) -> PkScheduler:
    """스케줄러 싱글턴 인스턴스를 반환합니다. 설정 변경 시 재초기화합니다."""
    instance = PkScheduler(state_file=state_file, speak_mode=speak_mode)
    return instance
