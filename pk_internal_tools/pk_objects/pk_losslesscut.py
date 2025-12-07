import logging
import textwrap
import time
import traceback
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_command_executed_advanced import ensure_command_executed_advanced
from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_focus_on import ensure_focus_on
from pk_internal_tools.pk_functions.ensure_mouse_clicked_by_coordination_history import ensure_mouse_clicked_by_coordination_history
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_30 import ensure_value_completed_2025_11_30
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.get_hash import get_hash
from pk_internal_tools.pk_functions.get_idle_title_of_losslesscut import get_idle_title_of_losslesscut
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_functions.get_window_hwnd import get_window_hwnd
from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
from pk_internal_tools.pk_functions.is_pc_remote_controlled_by_renova import is_pc_remote_controlled_by_renova
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_case_debugger_executed import ensure_case_debugger_executed
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical

from pk_internal_tools.pk_objects.pk_file_extensions import FILE_EXTENSIONS
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_loop import PkLoop
from pk_internal_tools.pk_objects.pk_media_file_controller import PkMediaFileController
from pk_internal_tools.pk_objects.pk_reg_patterns import FILENAME_PARTS_TO_IGNORE, REGEX_PATTERNS_TO_IGNORE
from pk_internal_tools.pk_objects.pk_system_operation_options import PlayerSelectionMode, SetupOpsForEnsureValueCompleted20251130, SetupOpsForManualMediaFileSelection
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


class PkLosslesscut(PkMediaFileController):
    def __init__(
            self,
            d_working: Path = None,
            selection_mode: PlayerSelectionMode = PlayerSelectionMode.AUTO) -> None:

        super().__init__(d_working)
        self.idle_title = get_idle_title_of_losslesscut()
        logging.debug(f"PkLosslesscut initialized with idle_title: '{self.idle_title}'")
        self.f_player: Path = F_LOSSLESSCUT_EXE
        self.d_working: Path = d_working
        self.file_to_play: Path | None = None
        self.files_allowed_to_load: list = []
        self.selected_files: list = []
        self.allowed_extensions: list[str] = list(
            FILE_EXTENSIONS['videos'] | FILE_EXTENSIONS['audios'])

        self.filename_parts_to_ignore: list[str] = []
        self.filename_regex_patterns_to_ignore: list[str] = []

        self._loop_id = 'pk_losslesscut'
        self.pk_loop = PkLoop(loop_id=get_hash(self._loop_id))
        self.pk_loop.init_loop_cnt()

        if QC_MODE:
            self.filename_parts_to_ignore = FILENAME_PARTS_TO_IGNORE
            self.filename_regex_patterns_to_ignore = REGEX_PATTERNS_TO_IGNORE
        
        self.is_segments_toggled = False
        self.selection_mode: PlayerSelectionMode = selection_mode
        self.manual_selection_display_mode: SetupOpsForManualMediaFileSelection = SetupOpsForManualMediaFileSelection.FILENAME_ONLY
        self.autoplay_queue: list[Path] = []

    def ensure_player_opened(self):
        func_n = get_caller_name()
        if Path(self.f_player).exists():
            cmd = rf'start "" "{self.f_player}"'
            ensure_command_executed(cmd=cmd, mode='a')
            return True
        else:
            alternative_path = ensure_value_completed_2025_11_30(
                key_name="alternative_path",
                func_n=func_n,
                guide_text=f"{self.idle_title} 후보경로 입력",
            )
            self.f_player = alternative_path
            cmd = rf'start "" "{self.f_player}"'
            ensure_command_executed(cmd=cmd, mode='a')
            return True
        return False

    def ensure_target_file_loaded(self, file_to_play: Path):
        try:
            if file_to_play and file_to_play.exists():
                ensure_command_executed_advanced(
                    cmd=rf'start "" {get_text_chain(self.f_player, file_to_play)}',
                    mode='a')
                return True
            logging.warning(f"File to play does not exist: {file_to_play}")
            return False
        except Exception as e:
            logging.error(f"Error loading file in Player: {e}")
            return False

    @ensure_seconds_measured
    def setup_playlist(self, with_sync: bool = True):
        logging.info(f"Setting up playlist with with_sync={with_sync}")
        if self.d_working is None:
            self.d_working = self.get_d_working_from_options()
        if not self.d_working:
            logging.error("Working directory is not set for Player.")
            return

        potential_files = get_files_filtered_from_db(
            directory_to_scan=Path(self.d_working),
            allowed_extensions=self.allowed_extensions,
            name_parts_to_ignore=self.filename_parts_to_ignore,
            regex_patterns_to_ignore=self.filename_regex_patterns_to_ignore,
            with_sync=with_sync
        )
        potential_files = [Path(p) for p in potential_files]
        func_n = get_caller_name()

        if self.selection_mode == PlayerSelectionMode.AUTO:
            self._handle_auto_selection(potential_files, func_n)
            self.autoplay_queue = list(self.files_allowed_to_load)
        elif self.selection_mode == PlayerSelectionMode.MANUAL:
            self._handle_manual_selection(potential_files, func_n)
            self.autoplay_queue = list(self.selected_files)
            logging.debug(f"Manual selection: populated self.autoplay_queue: {self.autoplay_queue}")

    def _get_next_file_from_autoplay_queue(self) -> bool:
        if not self.autoplay_queue:
            logging.info("Autoplay queue is empty. Attempting to refill...")
            refill_source = []
            if self.selection_mode == PlayerSelectionMode.MANUAL:
                if self.selected_files:
                    logging.info("Refilling queue from user's manual selection.")
                    refill_source = self.selected_files
            elif self.selection_mode == PlayerSelectionMode.AUTO:
                if self.files_allowed_to_load:
                    logging.info("Refilling queue from allowed files for continuous loop.")
                    refill_source = self.files_allowed_to_load
            
            if not refill_source:
                logging.info("Autoplay queue is empty and could not be refilled. Stopping playback.")
                self.file_to_play = None
                return False
            self.autoplay_queue = list(refill_source)

        while self.autoplay_queue:
            media_file_to_load = self.autoplay_queue.pop(0)
            candidate_file_path = Path(media_file_to_load)
            if candidate_file_path.exists():
                self.file_to_play = candidate_file_path
                self.title_loaded_predicted = rf"{get_nx(self.file_to_play)} - {self.idle_title}"
                logging.info(f"Next file to play: {self.file_to_play.name}")
                return True
            else:
                logging.warning(f"File from autoplay queue does not exist, skipping: {candidate_file_path}")

        logging.info("Autoplay queue is empty and no valid files could be found. Stopping playback.")
        self.file_to_play = None
        return False

    def _handle_manual_selection(self, potential_files: list[Path], func_n: str):
        self.files_allowed_to_load = potential_files
        options_for_display_mode = [member.value.lower() for member in SetupOpsForManualMediaFileSelection]
        from pk_internal_tools.pk_functions.get_file_id import get_file_id
        from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
        from pk_internal_tools.pk_functions.get_last_selected import get_last_selected

        display_mode_key_name = "manual_media_file_selection_display_mode"
        file_id = get_file_id(display_mode_key_name, func_n)
        f_historical = get_history_file_path(file_id=file_id)
        last_selected_display_mode = get_last_selected(f_historical)

        logging.debug(f"[DEBUG] _handle_manual_selection - key_name: {display_mode_key_name}, func_n: {func_n}")
        logging.debug(f"[DEBUG] _handle_manual_selection - f_historical: {f_historical}")
        logging.debug(f"[DEBUG] _handle_manual_selection - last_selected_display_mode: '{last_selected_display_mode}'")
        logging.debug(f"[DEBUG] _handle_manual_selection - options_for_display_mode: {options_for_display_mode}")

        if last_selected_display_mode and last_selected_display_mode in options_for_display_mode:
            selected_display_mode_str = last_selected_display_mode
            logging.debug(f"[DEBUG] _handle_manual_selection - AUTO-SELECTED: {selected_display_mode_str}")
        else:
            logging.debug(f"[DEBUG] _handle_manual_selection - PROMPTING user for selection.")
            selected_display_mode_str = ensure_value_completed(
                key_name=display_mode_key_name,
                func_n=func_n,
                options=options_for_display_mode,
                guide_text="파일 목록 표시 방식을 선택하세요 (전체경로 | 파일명만):",
                sort_order=SetupOpsForEnsureValueCompleted20251130.HISTORY)

        self.manual_selection_display_mode = SetupOpsForManualMediaFileSelection(selected_display_mode_str.upper())

        if self.manual_selection_display_mode == SetupOpsForManualMediaFileSelection.FILENAME_ONLY:
            file_selection_options = [p.name for p in self.files_allowed_to_load]
        else:
            file_selection_options = [str(p) for p in self.files_allowed_to_load]

        selected_file_display_values = ensure_values_completed(
            key_name="manual_media_file_selection", func_n=func_n, options=file_selection_options,
            guide_text="재생할 파일을 (다중) 선택하세요:", multi_select=True)
        logging.debug(f"Manual selection: user chose: {selected_file_display_values}")

        self.selected_files = []
        if selected_file_display_values:
            for display_value in selected_file_display_values:
                if self.manual_selection_display_mode == SetupOpsForManualMediaFileSelection.FILENAME_ONLY:
                    found_path = next((p for p in potential_files if p.name == display_value), None)
                else:
                    found_path = Path(display_value)
                if found_path:
                    self.selected_files.append(found_path)
                else:
                    logging.warning(f"Selected file not found in allowed list: {display_value}")
            logging.debug(f"Manual selection: populated self.selected_files: {self.selected_files}")
        
        if not self.selected_files:
            logging.info("No media files manually selected by user.")

    def _handle_auto_selection(self, potential_files: list[Path], func_n: str):
        if not self.files_allowed_to_load:
            options_for_display_mode = [member.value.lower() for member in SetupOpsForManualMediaFileSelection]
            auto_display_mode_key_name = "auto_media_file_initial_selection_display_mode"
            file_id_auto = get_file_id(auto_display_mode_key_name, func_n)
            f_historical_auto = get_history_file_path(file_id=file_id_auto)
            last_selected_auto_display_mode = get_last_selected(f_historical_auto)

            logging.debug(f"[DEBUG] _handle_auto_selection - key_name: {auto_display_mode_key_name}, func_n: {func_n}")
            logging.debug(f"[DEBUG] _handle_auto_selection - f_historical_auto: {f_historical_auto}")
            logging.debug(f"[DEBUG] _handle_auto_selection - last_selected_auto_display_mode: '{last_selected_auto_display_mode}'")
            logging.debug(f"[DEBUG] _handle_auto_selection - options_for_display_mode: {options_for_display_mode}")

            if last_selected_auto_display_mode and last_selected_auto_display_mode in options_for_display_mode:
                selected_display_mode_str = last_selected_auto_display_mode
                logging.debug(f"[DEBUG] _handle_auto_selection - AUTO-SELECTED: {selected_display_mode_str}")
            else:
                logging.debug(f"[DEBUG] _handle_auto_selection - PROMPTING user for selection.")
                selected_display_mode_str = ensure_value_completed(
                    key_name=auto_display_mode_key_name, func_n=func_n,
                    options=options_for_display_mode, guide_text="자동 재생할 초기 미디어 파일 목록 표시 방식을 선택하세요 (전체경로 | 파일명만):",
                    sort_order=SetupOpsForEnsureValueCompleted20251130.HISTORY)
            manual_selection_display_mode_for_auto = SetupOpsForManualMediaFileSelection(selected_display_mode_str.upper())

            if manual_selection_display_mode_for_auto == SetupOpsForManualMediaFileSelection.FILENAME_ONLY:
                file_selection_options_for_auto = [p.name for p in potential_files]
            else:
                file_selection_options_for_auto = [str(p) for p in potential_files]

            interesting_files_to_load = ensure_values_completed(
                key_name="interesting_files_to_load", func_n=func_n, options=file_selection_options_for_auto,
                guide_text="자동 재생할 초기 미디어 파일들을 (다중) 선택하세요:", multi_select=True)

            self.files_allowed_to_load = []
            if interesting_files_to_load:
                for display_value in interesting_files_to_load:
                    if manual_selection_display_mode_for_auto == SetupOpsForManualMediaFileSelection.FILENAME_ONLY:
                        found_path = next((p for p in potential_files if p.name == display_value), None)
                    else:
                        found_path = Path(display_value)
                    if found_path:
                        self.files_allowed_to_load.append(found_path)
                    else:
                        logging.warning(f"Selected file not found in potential list: {display_value}")
            if not self.files_allowed_to_load:
                logging.warning("No media files selected by user for auto playback.")

    def ensure_media_file_controller_played(self, hwnd: Optional[int]) -> bool:
        if hwnd:
            logging.debug(f"Sending 'ctrl + space' to hwnd: {hwnd}")
            ensure_focus_on(hwnd)
            ensure_slept(milliseconds=100) # 안정성을 위한 짧은 지연 (증가)
            ensure_pressed("ctrl", "space")
            ensure_slept(milliseconds=100) # 안정성을 위한 짧은 지연 (증가)
            logging.debug(f"'ctrl + space' sent to hwnd: {hwnd}")
            return True
        logging.warning("Could not find Player window to send play command.")
        return False

    def is_player_executed(self) -> bool:
        for title in get_windows_opened():
            if self.idle_title in title:
                logging.debug(f"{self.idle_title} is running (window found: '{title}')")
                return True
        logging.debug(f"{get_nx(self.f_player)} is not running.")
        return False

    def ensure_clicked(self, key_name, reset=False):
        try:
            func_n = get_caller_name()
            if is_pc_remote_controlled_by_renova():
                key_name = f"{key_name} for renova"
                ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=reset)
            else:
                key_name = f"{key_name}"
                ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=reset)
            return True
        except BaseException:
            ensure_debug_loged_verbose(traceback)
            return False

    @ensure_seconds_measured
    def ensure_media_file_controller_screen_maximized(self, hwnd):
        try:
            if not hwnd:
                logging.debug(f"'{hwnd}' can be maximized. for hwnd not found")
                return False
            
            ensure_focus_on(hwnd)
            ensure_slept(milliseconds=22) # 안정성을 위해 약간의 딜레이 추가
            ensure_pressed("f10")
            logging.debug(f"F10 pressed for '{hwnd}'.")
            return True
        except BaseException as e:
            logging.error(f"Error in ensure_media_file_controller_screen_maximized: {e}")
            ensure_debug_loged_verbose(traceback)
            return False

    def ensure_player_played_following_routine(self, title, is_already_loaded: bool = False):
        logging.debug(f"ensure_player_played_following_routine called. title='{title}', is_already_loaded={is_already_loaded}")
        if not is_window_title_front(window_title=title):
            logging.debug(f"Window '{title}' not front. Bringing to front.")
            ensure_window_to_front(window_title_seg=title)
        
        if is_window_title_front(window_title=title):
            hwnd = get_window_hwnd(title)
            if not hwnd:
                logging.error(f"Could not get window handle for title: {title}")
                return False

            if not is_already_loaded:
                logging.debug("File is not already loaded. Attempting to load file and maximize.")
                if not self.ensure_target_file_loaded(file_to_play=self.file_to_play):
                    logging.error("Failed to load target file. Pausing console.")
                    # ensure_console_paused()
                    # mkr..
                    self._get_next_file_from_autoplay_queue()
                    return False
                logging.debug("Target file loaded successfully.")
                
                # 파일 로드 직후 한 번 최대화 시도
                if not self.ensure_media_file_controller_screen_maximized(hwnd=hwnd):
                    logging.warning("Failed to maximize screen after file load. Pausing console.")
                    ensure_console_paused()
                    # 실패하더라도 계속 진행 (치명적이지 않다고 가정)
            else:
                logging.debug("File is already loaded. Skipping file load and initial maximize.")
            
            ensure_focus_on(hwnd)
            ensure_pressed("esc") # LosslessCut이 풀스크린일 경우 빠져나오기 위함 (복구)
            # esc 키 입력 후 최대화가 해제될 경우를 대비하여 다시 최대화 시도
            if not self.ensure_media_file_controller_screen_maximized(hwnd=hwnd):
                logging.warning("Failed to maximize screen after esc key press.")
                # 실패하더라도 계속 진행 (치명적이지 않다고 가정)
            
            # loop_cnt 관련 로직은 현재 사용되지 않으므로 주석 처리 유지 또는 제거 고려
            # loop_cnt = self.pk_loop.get_loop_cnt()
            # reset = loop_cnt == 1
            # if not self.ensure_clicked(key_name="닫기", reset=reset):
            #     ensure_console_paused()
            #     return False
            # self.pk_loop.set_loop_cnt(loop_cnt + 1)
            # ensure_slept(milliseconds=2000)
            
            # LosslessCut UI 안정화를 위한 대기
            logging.debug("Waiting for LosslessCut UI to stabilize before sending play command.")
            ensure_slept(milliseconds=1000)
            
            # 재생/일시정지 명령
            logging.debug("Attempting to play/pause media.")
            if not self.ensure_media_file_controller_played(hwnd=hwnd):
                logging.error("Failed to play/pause media. Pausing console.")
                ensure_console_paused()
                return False
            logging.debug("Media play/pause command sent.")

            # 재생 명령 후 한 번 더 최대화 시도 (이전 버전의 동작 유지)
            # is_already_loaded가 True일 때는 최대화 재확인도 건너뜀
            if not is_already_loaded:
                if not self.ensure_media_file_controller_screen_maximized(hwnd=hwnd):
                    logging.warning("Failed to maximize screen after play/pause command.")
                    # 실패하더라도 계속 진행 (치명적이지 않다고 가정)
                logging.debug("Screen maximization re-checked after play/pause command.")
            
            return True
        logging.warning(f"Window '{title}' not front after attempt. Cannot proceed with routine.")
        return False

    def ensure_state_machine_executed(self, file_to_load: Path | None = None) -> None:
        is_performance_mode  = False
        logging.info("Starting Player event loop...")
        if file_to_load:
            file_to_load_path = Path(file_to_load)
            if file_to_load_path.exists():
                self.autoplay_queue = [file_to_load_path]
                self.files_allowed_to_load = [file_to_load_path] # Also populate this for consistency
                logging.info(f"Single file playback specified: {self.file_to_play}")
            else:
                logging.error(f"Specified file not found: {file_to_load_path}")
                return
        else:
            self.setup_playlist()

        if not self.autoplay_queue:
            logging.warning("No files selected to play. Exiting.")
            return
        
        loop_cnt = 1
        while self._get_next_file_from_autoplay_queue():
            logging.info(f"Player Loop Cnt: {loop_cnt}")
            playback_complete = False
            while not playback_complete:
                if self.is_player_executed():
                    windows = get_windows_opened()
                    found_window = False
                    for title in windows:
                        if title == self.title_loaded_predicted or title == self.idle_title:
                            logging.debug(f"Loop check: Current title='{title}', Predicted='{self.title_loaded_predicted}', Idle='{self.idle_title}'")
                            is_already_loaded = title == self.title_loaded_predicted
                            logging.debug(f"is_already_loaded set to: {is_already_loaded}")
                            if self.ensure_player_played_following_routine(title=title, is_already_loaded=is_already_loaded):
                                ensure_slept(milliseconds=500)
                                playback_complete = True
                                found_window = True
                                break
                    if not found_window:
                        ensure_slept(milliseconds=77)
                else:
                    self.ensure_player_opened()
                    ensure_slept(milliseconds=77)

            logging.info("Playback complete for the current file. Waiting for LosslessCut to become idle...")
            idle_wait_start_time = time.time()
            while True:
                if not self.is_player_executed():
                    logging.warning("LosslessCut was closed during idle wait. Exiting.")
                    return

                current_titles = get_windows_opened()
                is_idle = any(self.idle_title == title for title in current_titles)
                logging.debug(f"Idle check: current_titles contents:")
                ensure_iterable_log_as_vertical(item_iterable=current_titles, item_iterable_n="current_titles in idle check")
                logging.debug(f"Idle check: idle_title='{self.idle_title}', is_idle={is_idle}")

                if is_idle:
                    logging.info("LosslessCut is idle. Proceeding to next file.")
                    break

                # 무조건 대기해야함.
                # if time.time() - idle_wait_start_time > 30: # 30-second timeout
                #     logging.warning("Timeout waiting for LosslessCut to become idle. Forcing next file.")
                #     break

                if is_performance_mode:
                    ensure_slept(milliseconds=200) # 고속성능모드
                else:
                    ensure_slept(milliseconds=1500) # 절약모드

            loop_cnt += 1
