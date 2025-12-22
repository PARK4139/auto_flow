from abc import ABC, abstractmethod
from pathlib import Path


class PkMediaFileController(ABC):
    def __init__(self, d_working):
        self.d_working = d_working
        self.idle_title = None

    # @abstractmethod
    # def is_player_opened(self) -> bool:
    #     """Check if the media player process is running."""
    #     pass

    # @abstractmethod
    # def ensure_player_opened(self) -> None:
    #     """Ensure the media player application is open."""
    #     pass
    # -> 주석이유 -> Potplayer 는 ensure_target_file_loaded로 대응가능 -> 호출필요 없음.

    @abstractmethod
    def ensure_target_file_loaded(self, file_to_play: Path) -> None:
        """Ensure the specified file is loaded in the player."""
        pass

    def _get_d_working_from_options(self):
        from pathlib import Path
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADED_FROM_TORRENT
        key_name = "d_working"
        func_n = get_caller_name()
        options = [Path(p) for p in [
            D_DOWNLOADED_FROM_TORRENT,
        ]]
        selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=list(set(options)))
        d_working = selected
        return d_working

    def get_d_working_from_options(self) -> Path | str:
        d_working = self._get_d_working_from_options()
        return d_working
