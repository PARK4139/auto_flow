# TODO : DEPRECATE THIS FILE
import socket
from enum import Enum
from os import environ

HOSTNAME = environ.get('HOSTNAME', socket.gethostname())  #

WSL_PK_DISTRO_N = 'wsl_pk_ubuntu_24_04'
pk_ = 'pk_'

PK_DEBUG_LINE = "PK_DEBUG " * 22
PK_USERLESS_LINE = "USELESS " * 22
PK_BLANK = " "
PK_UNDERLINE_HALF = '_' * 33
PK_UNDERLINE = PK_UNDERLINE_HALF * 2 + rf"{PK_BLANK}"  # pk_option # python pep8 최대권장길이(79)를 기준으로 13 자 내외로 제목작성을 작성을 최대한 준수
PK_WINDOWS_LONG_PATH_ALLOWED_SPECIAL_PREFIX = '\\\\?\\'
PK_DIVIDER = PK_UNDERLINE  # pk_option
PK_UNDERLINE_SHORT = '_' * 2  # pk_option
pk_INDENTATION_PROMISED = ' ' * 5  # pk_option
PK_BLANK = ' '  # pk_option

pi = 3.141592

# hope to deprecate
members = []  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
BIGGEST_PNXS = []  # 300 MB 이상 백업대상
SMALLEST_PNXS = []
PK_HEX_COLOR_MAP = {
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "RED": "#FF0000",
    "GREEN": "#00FF00",
    "YELLOW": "#FFFF00",
    "BLUE": "#0000FF"
}


class PkFilter(Enum):  # TODO : will deprecate
    url_like = 'url_like'
    url_false = 'url_false'
