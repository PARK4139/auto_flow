import logging
import traceback
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_losslescut_killed import ensure_losslescut_killed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_objects.pk_media_file_controller import PkMediaFileController
from pk_internal_tools.pk_objects.pk_modes import PlayerSelectionMode, PkModesForManualMediaFileSelection


class PkLosslesscut(PkMediaFileController):
    def __init__(
            self,
            d_working: Path = None,
            selection_mode: PlayerSelectionMode = PlayerSelectionMode.AUTO) -> None:

        from pk_internal_tools.pk_functions.get_hash import get_hash
        from pk_internal_tools.pk_functions.get_idle_title_of_losslesscut import get_idle_title_of_losslesscut
        from pk_internal_tools.pk_objects.pk_database_manager import db_manager
        from pk_internal_tools.pk_objects.pk_file_extensions import PK_FILE_EXTENSIONS
        from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
        from pk_internal_tools.pk_objects.pk_modes import PlayerSelectionMode
        from pk_internal_tools.pk_objects.pk_one_data_database import PkSingleDataDataBase
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        from pk_internal_tools.pk_objects.pk_reg_patterns import FILENAME_PARTS_TO_IGNORE, REGEX_PATTERNS_TO_IGNORE

        super().__init__(d_working)

        # --- Argument Type Handling ---
        # Ensure selection_mode is an Enum instance, regardless of input type
        if isinstance(selection_mode, str):
            try:
                # Convert string value (e.g., "auto") to Enum member
                self.selection_mode = PlayerSelectionMode(selection_mode.lower())
            except ValueError:
                logging.warning(f"Invalid selection_mode string '{selection_mode}'. Falling back to AUTO.")
                self.selection_mode = PlayerSelectionMode.AUTO
        elif isinstance(selection_mode, PlayerSelectionMode):
            self.selection_mode = selection_mode
        else:
            logging.warning(f"Unexpected type for selection_mode '{type(selection_mode)}'. Falling back to AUTO.")
            self.selection_mode = PlayerSelectionMode.AUTO

        # --- DB State Loading ---
        self.db_manager = db_manager
        self.state_key = 'losslesscut_instance_state'  # Key for instance-specific state
        self._load_instance_state()  # Call helper to load instance state

        self.idle_title = get_idle_title_of_losslesscut()
        self.f_losslesscut: Path = F_LOSSLESSCUT_EXE
        self.allowed_extensions: list[str] = list(
            PK_FILE_EXTENSIONS['videos'] | PK_FILE_EXTENSIONS['audios'])

        self.file_name_parts_to_ignore: list[str] = []
        self.file_name_regex_patterns_to_ignore: list[str] = []

        self._loop_id = 'pk_losslesscut'
        self.pk_loop = PkSingleDataDataBase(loop_id=get_hash(self._loop_id))
        self.pk_loop.init_loop_cnt()

        if QC_MODE:
            self.file_name_parts_to_ignore = FILENAME_PARTS_TO_IGNORE
            self.file_name_regex_patterns_to_ignore = REGEX_PATTERNS_TO_IGNORE

        self.is_segments_toggled = False
        self._last_known_titles = None
        self._reexecute_losslesscut()
        logging.debug(f"PkLosslesscut initialized")

        # Initial state save after initialization
        self._save_instance_state()

    @ensure_seconds_measured
    def _execute_losslesscut(self):
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        func_n = get_caller_name()
        if not Path(self.f_losslesscut).exists():
            losslesscut_alternative_path = ensure_value_completed(
                key_name="losslesscut_alternative_path",
                func_n=func_n,
            )
            if not Path(losslesscut_alternative_path):
                logging.error("losslesscut_alternative_path is not exist")
                raise FileNotFoundError
            self.f_losslesscut = losslesscut_alternative_path
        cmd = rf'start "" "{self.f_losslesscut}"'
        ensure_command_executed(cmd=cmd, mode='a')
        return True

    @ensure_seconds_measured
    def ensure_target_file_loaded(self, file_to_play: Path):
        from pk_internal_tools.pk_functions.ensure_command_executed_2025_08_04 import ensure_command_executed_2025_08_04
        from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
        from pywinauto import Application
        from pywinauto.findwindows import ElementNotFoundError
        from pywinauto.timings import TimeoutError
        import re

        try:
            if file_to_play and file_to_play.exists():
                # Execute command to load file
                ensure_command_executed_2025_08_04(
                    cmd=rf'start "" {get_text_chain(self.f_losslesscut, file_to_play)}',
                    mode='a')

                # Connect to LosslessCut application
                # app = Application(backend="uia").connect(path=str(self.f_losslesscut), timeout=15)
                app = Application(backend="uia").connect(path=str(self.f_losslesscut), timeout=5)

                # Wait for the window title to change, indicating the file is loaded.
                expected_title_pattern = f".*{re.escape(file_to_play.name)}.*"
                window = app.window(title_re=expected_title_pattern)
                # window.wait('visible', timeout=5, retry_interval=0.5)
                window.wait('visible', timeout=2, retry_interval=0.5)

                # Get the actual window title
                actual_window_title = window.window_text()
                logging.debug(f"File '{file_to_play.name}' loaded, actual window title: '{actual_window_title}'")

                # Update file state in DB
                self.db_manager.update_file_state(str(file_to_play), "loaded", window_title=actual_window_title)

                return True
            logging.warning(f"File to play does not exist: {file_to_play}")
            return False
        except (ElementNotFoundError, TimeoutError) as e:
            logging.error(f"Timeout or error waiting for window after loading file '{file_to_play.name}': {e}")
            self.db_manager.update_file_state(str(file_to_play), "error", window_title=None)  # Record error state
            return False
        except Exception as e:
            logging.error(f"Error loading file in Player: {e}", exc_info=True)
            self.db_manager.update_file_state(str(file_to_play), "error", window_title=None)  # Record error state
            return False

    @ensure_seconds_measured
    def setup_playlist(self, with_sync: bool = True):

        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
        from pk_internal_tools.pk_objects.pk_modes import PlayerSelectionMode

        logging.info(f"Setting up playlist with with_sync={with_sync}")
        if self.d_working is None:
            self.d_working = self.get_d_working_from_options()
        if not self.d_working:
            logging.error("Working directory is not set for Player.")
            return

        potential_files = get_files_filtered_from_db(
            directory_to_scan=Path(self.d_working),
            allowed_extensions=self.allowed_extensions,
            name_parts_to_ignore=self.file_name_parts_to_ignore,
            regex_patterns_to_ignore=self.file_name_regex_patterns_to_ignore,
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

        self._save_state()

    def _get_next_file_from_autoplay_queue(self) -> bool:

        from pk_internal_tools.pk_functions.get_nx import get_nx
        from pk_internal_tools.pk_objects.pk_modes import PlayerSelectionMode

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
                # Before setting to None, if there was a previous file, mark it idle
                if self.file_to_play:
                    self.db_manager.update_file_state(str(self.file_to_play), "idle")
                self.file_to_play = None
                self._save_instance_state()  # Save instance state after file_to_play becomes None
                return False
            self.autoplay_queue = list(refill_source)

        while self.autoplay_queue:
            media_file_to_load = self.autoplay_queue.pop(0)
            candidate_file_path = Path(media_file_to_load)
            if candidate_file_path.exists():
                # If there was a previous file, mark it idle before moving to the next
                if self.file_to_play and self.file_to_play != candidate_file_path:
                    self.db_manager.update_file_state(str(self.file_to_play), "idle")

                self.file_to_play = candidate_file_path
                self.title_loaded_predicted = rf"{get_nx(self.file_to_play)} - {self.idle_title}"
                logging.info(f"Next file to play: {self.file_to_play.name}")
                self.db_manager.update_file_state(str(self.file_to_play), "idle")  # Mark new file as idle initially
                self._save_instance_state()  # Save instance state after file_to_play changes
                return True
            else:
                logging.warning(f"File from autoplay queue does not exist, skipping: {candidate_file_path}")
                # If a file is skipped, we don't want to leave it in an unknown state
                self.db_manager.update_file_state(str(candidate_file_path), "skipped")

        logging.info("Autoplay queue is empty and no valid files could be found. Stopping playback.")
        # Before setting to None, if there was a previous file, mark it idle
        if self.file_to_play:
            self.db_manager.update_file_state(str(self.file_to_play), "idle")
        self.file_to_play = None
        self._save_instance_state()  # Save instance state after file_to_play becomes None
        return False

    def _handle_manual_selection(self, potential_files: list[Path], func_n: str):

        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
        from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
        from pk_internal_tools.pk_functions.get_file_id import get_file_id
        from pk_internal_tools.pk_functions.get_last_selected import get_last_selected
        from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureValueCompleted, PkModesForManualMediaFileSelection

        self.files_allowed_to_load = potential_files
        options_for_display_mode = [member.value.lower() for member in PkModesForManualMediaFileSelection]

        display_mode_key_name = "manual_media_file_selection_display_mode"
        file_id = get_file_id(display_mode_key_name, func_n)
        f_historical = get_history_file_path(file_id=file_id)
        last_selected_display_mode = get_last_selected(f_historical)

        logging.debug(f"_handle_manual_selection - key_name: {display_mode_key_name}, func_n: {func_n}")
        logging.debug(f"_handle_manual_selection - f_historical: {f_historical}")
        logging.debug(f"_handle_manual_selection - last_selected_display_mode: '{last_selected_display_mode}'")
        logging.debug(f"_handle_manual_selection - options_for_display_mode: {options_for_display_mode}")

        if last_selected_display_mode and last_selected_display_mode in options_for_display_mode:
            selected_display_mode_str = last_selected_display_mode
            logging.debug(f"_handle_manual_selection - AUTO-SELECTED: {selected_display_mode_str}")
        else:
            logging.debug(f"_handle_manual_selection - PROMPTING user for selection.")
            selected_display_mode_str = ensure_value_completed(
                key_name=display_mode_key_name,
                func_n=func_n,
                options=options_for_display_mode,
                guide_text="파일 목록 표시 방식을 선택하세요 (전체경로 | 파일명만):",
                sort_order=PkModesForEnsureValueCompleted.HISTORY)

        self.manual_selection_display_mode = PkModesForManualMediaFileSelection(selected_display_mode_str.upper())

        if self.manual_selection_display_mode == PkModesForManualMediaFileSelection.FILENAME_ONLY:
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
                if self.manual_selection_display_mode == PkModesForManualMediaFileSelection.FILENAME_ONLY:
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

        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
        from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
        from pk_internal_tools.pk_functions.get_file_id import get_file_id
        from pk_internal_tools.pk_functions.get_last_selected import get_last_selected
        from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureValueCompleted, PkModesForManualMediaFileSelection

        if not self.files_allowed_to_load:
            options_for_display_mode = [member.value.lower() for member in PkModesForManualMediaFileSelection]
            auto_display_mode_key_name = "auto_media_file_initial_selection_display_mode"
            file_id_auto = get_file_id(auto_display_mode_key_name, func_n)
            f_historical_auto = get_history_file_path(file_id=file_id_auto)
            last_selected_auto_display_mode = get_last_selected(f_historical_auto)

            logging.debug(f"_handle_auto_selection - key_name: {auto_display_mode_key_name}, func_n: {func_n}")
            logging.debug(f"_handle_auto_selection - f_historical_auto: {f_historical_auto}")
            logging.debug(f"_handle_auto_selection - last_selected_auto_display_mode: '{last_selected_auto_display_mode}'")
            logging.debug(f"_handle_auto_selection - options_for_display_mode: {options_for_display_mode}")

            if last_selected_auto_display_mode and last_selected_auto_display_mode in options_for_display_mode:
                selected_display_mode_str = last_selected_auto_display_mode
                logging.debug(f"_handle_auto_selection - AUTO-SELECTED: {selected_display_mode_str}")
            else:
                logging.debug(f"_handle_auto_selection - PROMPTING user for selection.")
                selected_display_mode_str = ensure_value_completed(
                    key_name=auto_display_mode_key_name, func_n=func_n,
                    options=options_for_display_mode, guide_text="자동 재생할 초기 미디어 파일 목록 표시 방식을 선택하세요 (전체경로 | 파일명만):",
                    sort_order=PkModesForEnsureValueCompleted.HISTORY)
            manual_selection_display_mode_for_auto = PkModesForManualMediaFileSelection(selected_display_mode_str.upper())

            if manual_selection_display_mode_for_auto == PkModesForManualMediaFileSelection.FILENAME_ONLY:
                file_selection_options_for_auto = [p.name for p in potential_files]
            else:
                file_selection_options_for_auto = [str(p) for p in potential_files]

            interesting_files_to_load = ensure_values_completed(
                key_name="interesting_files_to_load", func_n=func_n, options=file_selection_options_for_auto,
                guide_text="자동 재생할 초기 미디어 파일들을 (다중) 선택하세요:", multi_select=True)

            self.files_allowed_to_load = []
            if interesting_files_to_load:
                for display_value in interesting_files_to_load:
                    if manual_selection_display_mode_for_auto == PkModesForManualMediaFileSelection.FILENAME_ONLY:
                        found_path = next((p for p in potential_files if p.name == display_value), None)
                    else:
                        found_path = Path(display_value)
                    if found_path:
                        self.files_allowed_to_load.append(found_path)
                    else:
                        logging.warning(f"Selected file not found in potential list: {display_value}")
            if not self.files_allowed_to_load:
                logging.warning("No media files selected by user for auto playback.")

        self._save_state()

    @ensure_seconds_measured
    def ensure_media_file_controller_played(self, hwnd: Optional[int]) -> bool:
        from pk_internal_tools.pk_functions.ensure_focus_on import ensure_focus_on
        from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

        if hwnd:
            logging.debug(f"Sending 'ctrl + space' to hwnd: {hwnd}")
            ensure_focus_on(hwnd)
            ensure_slept(milliseconds=111)
            ensure_pressed("ctrl", "space")
            ensure_slept(milliseconds=111)  # 안정성을 위한 짧은 지연 (증가)
            # alert_as_gui("ctrl + space is pressed")
            return True
        logging.warning("Could not find Player window to send play command.")
        return False

    def _is_losslesscut_executed(self) -> bool:
        from pk_internal_tools.pk_functions.get_nx import get_nx
        from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened

        for title in get_windows_opened():
            if self.idle_title in title:
                logging.debug(f"{self.idle_title} is running (window found: '{title}')")
                return True
        logging.debug(f"{get_nx(self.f_losslesscut)} is not running.")
        return False

    def ensure_clicked(self, key_name, reset=False):

        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        from pk_internal_tools.pk_functions.ensure_mouse_clicked_by_coordination_history import ensure_mouse_clicked_by_coordination_history
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.is_pc_remote_controlled_by_renova import is_pc_remote_controlled_by_renova

        try:
            func_n = get_caller_name()
            if is_pc_remote_controlled_by_renova():
                key_name = f"{key_name} for renova"
                ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=reset)
            else:
                key_name = f"{key_name}"
                ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=reset)
            return True
        except BaseException as e:
            ensure_debugged_verbose(traceback, e)
            return False

    @ensure_seconds_measured
    def ensure_pk_losslesscut_screen_maximized(self, hwnd):

        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        from pk_internal_tools.pk_functions.ensure_focus_on import ensure_focus_on
        from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

        try:
            if not hwnd:
                logging.debug(f"'{hwnd}' can be maximized. for hwnd not found")
                return False
            ensure_focus_on(hwnd)
            ensure_slept(milliseconds=22)  # 안정성을 위해 약간의 딜레이 추가
            ensure_pressed("f10")
            logging.debug(f"F10 pressed for '{hwnd}'.")
            return True
        except BaseException as e:
            logging.error(f"Error in ensure_media_file_controller_screen_maximized: {e}")
            ensure_debugged_verbose(traceback, e)
            return False

    def ensure_pk_losslesscut_screen_relocated(self, hwnd):

        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        from pk_internal_tools.pk_functions.ensure_focus_on import ensure_focus_on

        # self._move_to_front(self.idle_title) # This was the problematic line
        ensure_focus_on(hwnd)  # Use the provided hwnd to focus the correct window

        if QC_MODE:
            # ensure_window_resized_and_positioned_left_half()
            # ensure_window_resized_and_positioned_right_half()

            # TODO:  파일 로드 직후 불필요창 요소 숨기기 시도
            # ensure_slept(milliseconds=1000)  # losslesscut 창 대기
            # ensure_mouse_clicked_by_coordination_history(key_name="내보낼 세그먼트 최소화", history_reset=True)
            # ensure_mouse_clicked_by_coordination_history(key_name="내보내기 완료 닫기", history_reset=True)

            self.ensure_pk_losslesscut_screen_maximized(hwnd)
        else:
            self.ensure_pk_losslesscut_screen_maximized(hwnd)

    def ensure_player_played_following_routine(self, idle_title, is_already_loaded: bool = False):
        from pywinauto import Application
        from pywinauto.findwindows import ElementNotFoundError
        from pywinauto.timings import TimeoutError
        from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
        from pk_internal_tools.pk_functions.get_window_hwnd import get_window_hwnd
        import re

        logging.debug(f"ensure_player_played_following_routine called. title='{idle_title}', is_already_loaded={is_already_loaded}")

        try:
            # Connect to LosslessCut application
            app = Application(backend="uia").connect(path=str(self.f_losslesscut), timeout=15)
            window = None

            # --- 1. 파일 로드 및 창 대기 ---
            if not is_already_loaded:
                logging.debug("File is not already loaded. Attempting to load file.")
                if not self.ensure_target_file_loaded(file_to_play=self.file_to_play):
                    logging.error("Failed to execute file load command.")
                    self._get_next_file_from_autoplay_queue()
                    return False

                # Wait for the window title to change, indicating the file is loaded.
                expected_title_pattern = f".*{re.escape(self.file_to_play.name)}.*"
                logging.debug(f"Waiting for window with title pattern: '{expected_title_pattern}'")
                window = app.window(title_re=expected_title_pattern)
                window.wait('visible', timeout=5, retry_interval=0.5)
                hwnd = window.handle
                logging.debug(f"Window with title '{window.window_text()}' found and visible. HWND: {hwnd}")
            else:
                logging.debug(f"File is already loaded. Finding window by title: {idle_title}")
                hwnd = get_window_hwnd(idle_title)
                if not hwnd:
                    logging.error(f"Could not get window handle for already loaded title: {idle_title}")
                    return False
                window = app.window(handle=hwnd)

            # --- 2. 창 활성화 및 최대화 ---
            if window:
                window.set_focus()
                if not window.is_active():
                    window.wait_active(timeout=5)
                logging.debug("Window is active.")

                if not self.ensure_pk_losslesscut_screen_relocated(hwnd=hwnd):
                    logging.warning("Failed to maximize/relocate screen.")

                # Update DB state for the loaded file with the actual window title
                self.db_manager.update_file_state(str(self.file_to_play), "loaded", window_title=window.window_text())

            else:
                logging.error("Could not get window object.")
                return False

            # --- 3. 재생 ---
            logging.debug("Attempting to play/pause media.")
            if not self.ensure_media_file_controller_played(hwnd=hwnd):
                logging.warning("Failed to play/pause media. Pausing console.")
                ensure_paused("Failed to play/pause media. Pausing console.")
                self.db_manager.update_file_state(str(self.file_to_play), "error_playing", window_title=None)  # Record error state
                return False
            logging.debug("Media play/pause command sent successfully.")
            self.db_manager.update_file_state(str(self.file_to_play), "played", window_title=window.window_text())  # Record played state

            return True

        except (ElementNotFoundError, TimeoutError) as e:
            logging.error(f"Timeout or error waiting for LosslessCut window/element: {e}")
            logging.error(f"Predicted title pattern was: '.*{re.escape(self.file_to_play.name)}.*'")

            # --- 디버깅을 위한 현재 창 목록 로깅 추가 ---
            from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
            logging.error("--- All currently open window titles at the time of timeout: ---")
            try:
                all_windows = get_windows_opened()
                for title in all_windows:
                    logging.error(f" -> {title}")
            except Exception as log_e:
                logging.error(f"Failed to get window list for debugging: {log_e}")
            logging.error("--------------------------------------------------------------------")

            ensure_paused("LosslessCut 창을 기다리다가 타임아웃이 발생했습니다.")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred in player routine: {e}")
            import traceback
            traceback.print_exc()
            return False

    def ensure_state_machine_executed(self, file_to_load: Path | None = None) -> None:

        import time

        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.get_window_hwnd import get_window_hwnd
        from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
        from pk_internal_tools.pk_objects.pk_colorful_logging_formatter import PK_UNDERLINE

        high_perpormance_mode = False
        logging.info("Starting Player event loop...")
        if file_to_load:
            file_to_load_path = Path(file_to_load)
            if file_to_load_path.exists():
                self.autoplay_queue = [file_to_load_path]
                self.files_allowed_to_load = [file_to_load_path]  # Also populate this for consistency
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
        while self._get_next_file_from_autoplay_queue():  # This will also set self.file_to_play and save its initial idle state
            logging.debug(PK_UNDERLINE)
            logging.info(f"Player Loop Cnt: {loop_cnt}")
            playback_complete = False
            while not playback_complete:
                if self._is_losslesscut_executed():
                    windows = get_windows_opened()
                    found_window = False
                    for idle_title in windows:
                        if idle_title == self.title_loaded_predicted or idle_title == self.idle_title:
                            logging.debug(f"Loop check: Current title='{idle_title}', Predicted='{self.title_loaded_predicted}', Idle='{self.idle_title}'")
                            is_already_loaded = idle_title == self.title_loaded_predicted
                            logging.debug(f"is_already_loaded set to: {is_already_loaded}")
                            if self.ensure_player_played_following_routine(idle_title=idle_title, is_already_loaded=is_already_loaded):
                                # Playback successful, ensure file state is saved as played
                                if self.file_to_play:
                                    self.db_manager.update_file_state(str(self.file_to_play), "played")  # Ensure final played state is saved

                                playback_complete = True
                                found_window = True
                                break
                    if not found_window:
                        ensure_slept(milliseconds=77)
                else:
                    self._execute_losslesscut()

                    timeout = 5
                    start_time = time.time()
                    idle_title_hwnd = None
                    while time.time() - start_time < timeout:
                        idle_title_hwnd = get_window_hwnd(self.idle_title)
                        if idle_title_hwnd:
                            logging.debug(f"LosslessCut window found with HWND: {idle_title_hwnd}")
                            break
                        ensure_slept(milliseconds=250)

                    if not idle_title_hwnd:
                        logging.error(f"Timed out waiting for LosslessCut window ('{self.idle_title}') to appear.")

                    if not self.ensure_pk_losslesscut_screen_relocated(hwnd=idle_title_hwnd):
                        logging.warning("Failed to relocate losslesscut window after file load. Pausing console.")
                        # ensure_paused()
                    ensure_slept(milliseconds=77)

            logging.info("Playback complete for the current file. Waiting for LosslessCut to become idle...")
            # After a file completes playback and before moving to the next, set its status to idle.
            if self.file_to_play:
                self.db_manager.update_file_state(str(self.file_to_play), "idle")  # Mark current file as idle

            idle_wait_start_time = time.time()
            while True:
                if not self._is_losslesscut_executed():
                    logging.warning("LosslessCut was closed during idle wait. Exiting")
                    # If LosslessCut closes, ensure the last played file is marked idle
                    if self.file_to_play:
                        self.db_manager.update_file_state(str(self.file_to_play), "idle")
                    return
                current_titles = get_windows_opened()
                is_idle = any(self.idle_title == title for title in current_titles)

                # current_titles가 변경되었을 때만 출력
                if self._last_known_titles is None or list(self._last_known_titles) != list(current_titles):
                    logging.debug(f"Idle check: current_titles contents updated. Before: {self._last_known_titles}, After: {current_titles}")
                    # ensure_iterable_data_printed(iterable_data=current_titles, iterable_data_n="current_titles")
                    self._last_known_titles = list(current_titles)
                else:
                    logging.debug(f"skipped printing")

                logging.debug(f"Idle check: idle_title='{self.idle_title}', is_idle={is_idle}")

                if is_idle:
                    logging.info("LosslessCut is idle. Proceeding to next file.")
                    break

                if high_perpormance_mode:
                    ensure_slept(milliseconds=111)
                else:
                    ensure_slept(milliseconds=1500)

            loop_cnt += 1

    def _save_instance_state(self):  # Renamed
        """
        Saves the current instance-specific state of the PkLosslesscut instance to the database.
        """
        instance_state_data = {
            'd_working': str(self.d_working) if self.d_working else None,
            'selection_mode': self.selection_mode.value,
            'manual_selection_display_mode': self.manual_selection_display_mode.value,
        }
        self.db_manager.upsert_state(self.state_key, instance_state_data)
        logging.debug(f"Instance state saved for key: {self.state_key}")

    def _load_instance_state(self):
        """
        Loads the instance-specific state of the PkLosslesscut instance from the database.
        """
        last_instance_state = self.db_manager.get_state(self.state_key)

        if last_instance_state:
            logging.info(f"Loading last instance state for '{self.state_key}' from DB.")
            self.d_working = Path(last_instance_state.get('d_working')) if last_instance_state.get('d_working') else None

            if 'selection_mode' in last_instance_state:
                self.selection_mode = PlayerSelectionMode(last_instance_state.get('selection_mode'))

            self.manual_selection_display_mode = PkModesForManualMediaFileSelection(last_instance_state.get('manual_selection_display_mode', PkModesForManualMediaFileSelection.FILENAME_ONLY.value))

            # File-specific states are not loaded here
            self.file_to_play = None
            self.files_allowed_to_load = []
            self.selected_files = []
            self.autoplay_queue = []
        else:
            logging.info("No previous instance state found. Initializing with default values.")
            # self.d_working and self.selection_mode are set by __init__ arguments
            self.manual_selection_display_mode = PkModesForManualMediaFileSelection.FILENAME_ONLY

            # File-specific states are dynamically initialized
            self.file_to_play = None
            self.files_allowed_to_load = []
            self.selected_files = []
            self.autoplay_queue = []

    def _reexecute_losslesscut(self):
        self._close_losslesscut()
        self._execute_losslesscut()

    def _move_to_front(self, window_title_seg):
        return ensure_window_to_front(window_title_seg)

    def _close_losslesscut(self):
        # ensure_windows_killed_like_human_by_window_title_seg(window_title_seg=self.idle_title)
        while 1:
            ensure_losslescut_killed()
            if not is_window_opened(window_title_seg=self.idle_title):
                break
            ensure_slept(milliseconds=111)
