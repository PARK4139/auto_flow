import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_condition_choosen import ensure_condition_choosen
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_window_hwnd import get_window_hwnd
from pk_internal_tools.pk_objects.pk_reg_patterns import FILENAME_PARTS_TO_IGNORE, REGEX_PATTERNS_TO_IGNORE
from pk_internal_tools.pk_objects.pk_media_file_controller import PkMediaFileController


class PkPotplayer(PkMediaFileController):
    """
        window pot player control util
    """
    def __init__(self, d_working: Path = None) -> None:
        from pathlib import Path
        from typing import List
        from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
        from pk_internal_tools.pk_objects.pk_file_extensions import FILE_EXTENSIONS
        super().__init__(self)
        self.idle_title = "팟플레이어"
        self.d_working: Path = d_working
        self.f_player: Path = F_POT_PLAYER_EXE
        self.file_to_load: Path | None = None
        self.file_to_allowed: list = []
        self.allowed_extensions: list[str] = list(FILE_EXTENSIONS['videos'] | FILE_EXTENSIONS['audios'])
        func_n = get_caller_name()

        # is_filename_filter_on = bool(ensure_value_completed_2025_11_11(key_name="is_filename_filter", func_n=func_n, options=["True", "False"]))
        # self.filename_parts_to_ignore: List[str] = ensure_condition_choosen(
        #     is_condition=is_filename_filter_on,
        #     positive_return=FILENAME_PARTS_TO_IGNORE,
        #     negative_return=['without filename fileter'],
        # )
        self.filename_parts_to_ignore =  []

        # is_regex_patterns_on = bool(ensure_value_completed_2025_11_11(key_name="is_regex_patterns_on", func_n=func_n, options=["True", "False"]))
        # self.filename_regex_patterns_to_ignore: List[str] = ensure_condition_choosen(
        #     is_condition=is_regex_patterns_on,
        #     positive_return=REGEX_PATTERNS_TO_IGNORE,
        #     negative_return=['without regex pattern'],
        # )
        self.filename_regex_patterns_to_ignore = []

    def ensure_target_file_loaded(self, file_to_play: Path):
        import logging

        from pk_internal_tools.pk_functions.ensure_command_executed_advanced import ensure_command_executed_advanced
        from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain

        try:
            if file_to_play and file_to_play.exists():
                # ensure_command_executed_advanced_async(cmds=[self.f_player, file_to_play])
                # ensure_command_executed_advanced(cmd=rf'start "" {get_text_chain(self.f_player, file_to_play)}')
                ensure_command_executed_advanced(cmd=rf'start "" {get_text_chain(self.f_player, file_to_play)}', mode='a')
                return True
            logging.warning(f"File to play does not exist: {file_to_play}")
            return False
        except Exception as e:
            logging.error(f"Error loading file in PotPlayer: {e}")
            return False

    @ensure_seconds_measured
    def update_video_to_load(self, refresh_list: bool = False):
        import logging
        from pathlib import Path
        from pk_internal_tools.pk_functions.get_f_video_to_load import get_f_media_to_load
        from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db

        if refresh_list or not self.file_to_allowed:
            logging.info("Refreshing allowed media list...")
            if self.d_working is None:
                self.d_working = self.get_d_working_from_options()

            d_working = self.d_working

            if not d_working:
                logging.error("Working directory is not set for PotPlayer.")
                self.file_to_allowed = []
            else:
                # Pass filter arguments directly to the function and remove the redundant inner loop.
                files_from_db = get_files_filtered_from_db(
                    directory_to_scan=d_working,
                    allowed_extensions=self.allowed_extensions,
                    name_parts_to_ignore=self.filename_parts_to_ignore,
                    regex_patterns_to_ignore=self.filename_regex_patterns_to_ignore,
                    with_sync=refresh_list  # Pass refresh_list as with_sync
                )
                self.file_to_allowed = [Path(p) for p in files_from_db]
            logging.info(f"Found {len(self.file_to_allowed)} media files.")

        new_video_str = get_f_media_to_load([str(p) for p in self.file_to_allowed])

        if new_video_str:
            self.file_to_load = Path(new_video_str)
            # Remove the selected file from the list to avoid re-playing
            self.file_to_allowed = [p for p in self.file_to_allowed if str(p) != new_video_str]
            logging.debug(f"Next file to play: {self.file_to_load}. Remaining files: {len(self.file_to_allowed)}")
        else:
            self.file_to_load = None
            logging.debug("No more media files to play from the list.")

    def ensure_media_file_controller_played(self):
        import logging

        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.get_nx import get_nx

        from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
        from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
        import win32gui
        import win32con

        player_window_title = None
        for title in get_windows_opened():
            if self.idle_title in title or get_nx(self.f_player) in title:
                player_window_title = title
                break

        if player_window_title:
            hwnd = win32gui.FindWindow(None, player_window_title)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                ensure_pressed("d")  # Press 'd' first
                ensure_slept(milliseconds=100)  # Short delay
                ensure_pressed("space")  # Then press 'space'
                logging.debug(f"Sent 'd' then 'space' to PotPlayer window: '{player_window_title}'")
                return True
        logging.warning("Could not find PotPlayer window to send play command.")
        return False

    def is_player_executed(self) -> bool:
        import logging
        from pk_internal_tools.pk_functions.get_nx import get_nx
        from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
        for title in get_windows_opened():
            if self.idle_title in title:
                logging.debug(f"{self.idle_title} is running (window found: '{title}')")
                return True
        logging.debug(f"{get_nx(self.f_player)} is not running.")
        return False

    def ensure_focus_on(self, hwnd):
        import win32gui
        import win32con
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    @ensure_seconds_measured
    def ensure_media_file_controller_screen_maximized(self, hwnd):
        import logging
        try:
            if not hwnd:
                logging.debug(f"'{hwnd}' can be maximized. for hwnd not found")
                return False

            self.ensure_focus_on(hwnd)  # 이게 중요
            ensure_slept(milliseconds=22)
            ensure_pressed("`")
            ensure_slept(milliseconds=22)
            ensure_pressed("enter")
            ensure_slept(milliseconds=22)
            logging.debug(f"'{hwnd}' is maximized.")
            return True

        except:
            ensure_debug_loged_verbose(traceback)
            return False

    def ensure_state_machine_executed(self) -> None:
        import logging

        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
        from pk_internal_tools.pk_functions.get_nx import get_nx
        from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
        from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
        from pk_internal_tools.pk_functions.get_window_hwnd import get_window_hwnd


        logging.info("Starting Player event loop...")

        # Initially load a video, prompting user if necessary
        # This will set self.file_to_load based on user selection or None
        self.update_video_to_load(refresh_list=True)

        loop_cnt = 1
        while 1:
            logging.info(f"Player Loop Cnt: {loop_cnt}")

            is_playing = False
            is_idle = False
            player_title = None

            # Check player state (simplified, focus on initial load issue)
            if self.is_player_executed(): # Checks if PotPlayer window is open
                windows = get_windows_opened()
                for title in windows:
                    if self.idle_title in title and " - " in title: # PotPlayer is playing something
                        is_playing = True
                        player_title = title
                        break
                    elif self.idle_title == title: # PotPlayer is open but idle
                        is_idle = True
                        player_title = title
                        break

            # Logic to handle playback:
            # 1. If a file is loaded and player is idle/not playing, attempt to play it.
            # 2. If no file is loaded AND player is idle, get a new file.
            # 3. If player is already playing, or busy loading, wait.

            if self.file_to_load and (is_idle or not (is_playing or is_idle)): # Attempt to play the loaded file
                logging.info(f"Attempting to play next file: {self.file_to_load}")
                file_played_successfully = self.ensure_target_file_loaded(self.file_to_load)
                
                if file_played_successfully:
                    ensure_slept(milliseconds=500) # Give PotPlayer time to load
                    
                    new_window_title = None
                    file_nx = get_nx(self.file_to_load)
                    for w_title in get_windows_opened():
                        if file_nx in w_title and self.idle_title in w_title:
                            new_window_title = w_title
                            break

                    if new_window_title:
                        ensure_window_to_front(window_title_seg=new_window_title)
                        if is_window_title_front(window_title=new_window_title):
                            self.ensure_media_file_controller_played() # Send 'd' then 'space'
                            hwnd = get_window_hwnd(title=new_window_title)
                            self.ensure_media_file_controller_screen_maximized(hwnd=hwnd)
                        self.file_to_load = None # Clear file_to_load after successful play/attempt
                    else:
                        logging.warning(f"Could not find player window for '{file_nx}' after loading.")
                        self.file_to_load = None # Clear if window not found to get new file
                else: # File could not be played
                    logging.warning(f"File '{self.file_to_load}' could not be played. Getting a new one.")
                    self.file_to_load = None # Clear to get a new file

            elif not self.file_to_load and (is_idle or not (is_playing or is_idle)): # Player is idle and no file is loaded, so get a new one
                logging.info("Player is idle and no file loaded. Getting a new file.")
                self.update_video_to_load() # This call will prompt for selection

            elif is_playing and loop_cnt == 1:
                # Special case: Script started while a video was already playing.
                logging.info(f"Player already playing '{player_title}'. Bringing to front and ensuring playback once.")
                ensure_window_to_front(window_title_seg=player_title)
                if is_window_title_front(window_title=player_title):
                    self.ensure_media_file_controller_played()
                    hwnd = get_window_hwnd(title=player_title)
                    self.ensure_media_file_controller_screen_maximized(hwnd=hwnd)

            ensure_slept(milliseconds=2222)
            loop_cnt += 1
