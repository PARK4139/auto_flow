from typing import Optional
from dataclasses import dataclass

@dataclass
class PkFzfTheme:
    """
    Encapsulates fzf theme-related settings.
    """
    layout_reverse: bool = False
    border_style: Optional[str] = None
