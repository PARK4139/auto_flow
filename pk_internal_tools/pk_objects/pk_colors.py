# TrueColor RGB to ANSI escape codes
def _tc_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def _tc_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


class PkColors:
    """
    Encapsulates ANSI and TrueColor definitions for terminal output.
    Provides color codes as direct class attributes, enabling IDE auto-completion.
    """
    # ANSI Standard Colors (Foreground)
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"  # Also often used for GREY
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_YELLOW_TONE1 = "\033[93m"
    BRIGHT_WHITE = "\033[97m"

    # ANSI Background Colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # ANSI Aliases / Special Codes
    GREY = BRIGHT_BLACK  # Alias for consistency
    RESET = "\033[0m"

    # TrueColor Presets (Foreground)
    TC_WHITE_TONE1 = _tc_fg(255, 255, 255)
    TC_RED_TONE1 = _tc_fg(255, 107, 107)
    TC_SKYBLUE_TONE1 = _tc_fg(77, 166, 255)
    TC_SKYBLUE_TONE2 = _tc_fg(51, 153, 255)
    TC_MINT_TONE1 = _tc_fg(0, 206, 209)
    TC_MINT_TONE2 = _tc_fg(32, 178, 170)
    TC_DARKPURPLE_TONE1 = _tc_fg(75, 0, 130)
    TC_DARKPURPLE_TONE2 = _tc_fg(72, 61, 139)
    TC_PASTELBLUE_TONE1 = _tc_fg(135, 206, 250)
    TC_PASTELBLUE_TONE2 = _tc_fg(30, 144, 255)

    TC_WHITE_PURE = _tc_fg(255, 255, 255)
    TC_BLACK_PURE = _tc_fg(0, 0, 0)
    TC_RED_PURE = _tc_fg(255, 0, 0)
    TC_GREEN_PURE = _tc_fg(0, 255, 0)
    TC_BLUE_PURE = _tc_fg(0, 0, 255)
    TC_YELLOW_PURE = _tc_fg(255, 255, 0)

    TC_PINK_TONE1 = _tc_fg(230, 157, 252)
    TC_ORANGE_TONE1 = _tc_fg(255, 132, 38)
    TC_DARKGREY_TONE1 = _tc_fg(64, 62, 77)
    TC_GREY_TONE1 = _tc_fg(66, 65, 65)
    TC_PEACH_TONE1 = _tc_fg(245, 201, 201)
    TC_CYAN_TONE1 = _tc_fg(77, 166, 255)
    TC_PURPLE_TONE_FALLBACK = _tc_fg(128, 0, 128)

    # TrueColor Presets (Background)
    TCBG_WHITE_TONE1 = _tc_bg(255, 255, 255)
    TCBG_RED_TONE1 = _tc_bg(255, 107, 107)
    TCBG_SKYBLUE_TONE1 = _tc_bg(77, 166, 255)
    TCBG_SKYBLUE_TONE2 = _tc_bg(51, 153, 255)
    TCBG_MINT_TONE1 = _tc_bg(0, 206, 209)
    TCBG_MINT_TONE2 = _tc_bg(32, 178, 170)
    TCBG_DARKPURPLE_TONE1 = _tc_bg(75, 0, 130)
    TCBG_DARKPURPLE_TONE2 = _tc_bg(72, 61, 139)
    TCBG_PASTELBLUE_TONE1 = _tc_bg(135, 206, 250)
    TCBG_PASTELBLUE_TONE2 = _tc_bg(30, 144, 255)

    TCBG_WHITE_PURE = _tc_bg(255, 255, 255)
    TCBG_BLACK_PURE = _tc_bg(0, 0, 0)
    TCBG_RED_PURE = _tc_bg(255, 0, 0)
    TCBG_GREEN_PURE = _tc_bg(0, 255, 0)
    TCBG_BLUE_PURE = _tc_bg(0, 0, 255)
    TCBG_YELLOW_PURE = _tc_bg(255, 255, 0)

    TCBG_PINK_TONE1 = _tc_bg(230, 157, 252)
    TCBG_ORANGE_TONE1 = _tc_bg(255, 132, 38)
    TCBG_DARKGREY_TONE1 = _tc_bg(64, 62, 77)
    TCBG_GREY_TONE1 = _tc_bg(66, 65, 65)
    TCBG_PEACH_TONE1 = _tc_bg(245, 201, 201)
    TCBG_CYAN_TONE1 = _tc_bg(77, 166, 255)
    TCBG_PURPLE_TONE_FALLBACK = _tc_bg(128, 0, 128)

    @staticmethod
    def colorize(text: str, color_code: str) -> str:
        """Wraps text with the given ANSI escape code for color."""
        return f"{color_code}{text}{PkColors.RESET}"

    @classmethod
    def fg_rgb(cls, r: int, g: int, b: int) -> str:
        """Generates a TrueColor foreground escape code."""
        return _tc_fg(r, g, b)

    @classmethod
    def bg_rgb(cls, r: int, g: int, b: int) -> str:
        """Generates a TrueColor background escape code."""
        return _tc_bg(r, g, b)
