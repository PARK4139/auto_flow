
def _tc_fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def _tc_bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


# dict가 보통 20~30% 더 빠름, class 보다
pk_ANSI_COLOR_MAP = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",

    "BRIGHT_BLACK": "\033[90m",    # alias: GREY
    "BRIGHT_RED": "\033[91m",
    "BRIGHT_GREEN": "\033[92m",
    "BRIGHT_YELLOW": "\033[93m",
    "BRIGHT_BLUE": "\033[94m",
    "BRIGHT_MAGENTA": "\033[95m",
    "BRIGHT_CYAN": "\033[96m",
    "BRIGHT_WHITE": "\033[97m",

    # Aliases & reset
    "GREY": "\033[90m",
    "RESET_CODE": "\033[0m",
    "RESET": "\033[0m",


    # =================================================================
    # TrueColor Presets (fzf 주석에서 가져온 프리셋들)
    # 규칙:
    #   - 전경: TC_<TONENAME>_TONE<n>
    #   - 배경: TCBG_<TONENAME>_TONE<n>
    # =================================================================

    # White
    "TC_WHITE_TONE1": _tc_fg(255, 255, 255),
    "TCBG_WHITE_TONE1": _tc_bg(255, 255, 255),

    # Red Soft (#ff6b6b)
    "TC_RED_TONE1": _tc_fg(255, 107, 107),
    "TCBG_RED_TONE1": _tc_bg(255, 107, 107),

    # SkyBlue (#4da6ff, #3399ff)
    "TC_SKYBLUE_TONE1": _tc_fg(77, 166, 255),   # pointer
    "TCBG_SKYBLUE_TONE1": _tc_bg(77, 166, 255),
    "TC_SKYBLUE_TONE2": _tc_fg(51, 153, 255),   # hl
    "TCBG_SKYBLUE_TONE2": _tc_bg(51, 153, 255),

    # MintBlue (#00ced1, #20b2aa)
    "TC_MINT_TONE1": _tc_fg(0, 206, 209),       # pointer
    "TCBG_MINT_TONE1": _tc_bg(0, 206, 209),
    "TC_MINT_TONE2": _tc_fg(32, 178, 170),      # hl
    "TCBG_MINT_TONE2": _tc_bg(32, 178, 170),

    # DarkPurple (#4b0082, #483d8b)
    "TC_DARKPURPLE_TONE1": _tc_fg(75, 0, 130),  # pointer
    "TCBG_DARKPURPLE_TONE1": _tc_bg(75, 0, 130),
    "TC_DARKPURPLE_TONE2": _tc_fg(72, 61, 139), # hl
    "TCBG_DARKPURPLE_TONE2": _tc_bg(72, 61, 139),

    # PastelBlue (#87cefa, #1e90ff)
    "TC_PASTELBLUE_TONE1": _tc_fg(135, 206, 250), # pointer
    "TCBG_PASTELBLUE_TONE1": _tc_bg(135, 206, 250),
    "TC_PASTELBLUE_TONE2": _tc_fg(30, 144, 255),  # hl
    "TCBG_PASTELBLUE_TONE2": _tc_bg(30, 144, 255),
}

ANSI_COLOR_MAP = pk_ANSI_COLOR_MAP

RESET_COLOR = "\033[0m"


