# TODO : DEPRECATE THIS FILE
import socket
from os import environ

HOSTNAME = environ.get('HOSTNAME', socket.gethostname())  #

pi = 3.141592

# hope to deprecate
members = []  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
BIGGEST_PNXS = []  # 300 MB 이상 백업대상
SMALLEST_PNXS = []

PK_WHITE = "#FFFFFF"
PK_BLACK = "#000000"
PK_PINK = "#e69dfc"
PK_RED = '#FF0000'
PK_SOFT_RED = '#ff6b6b'
PK_GREEN = '#00FF00'
PK_BLUE = '#0000FF'
PK_CYAN = '#4da6ff'
PK_CYAN_FALLBACK = '#3399ff'
PK_YELLOW = '#FFFF00'
PK_ORANGE = '#ff8426'
PK_DARK_GREY = "#403e4d"
PK_GREY = "#424141"
PK_PEACH = "#f5c9c9"
PK_MINT_BLUE = "#20b2aa"
PK_MINT_BLUE_FALLBACK = "#00ced1"
PK_DARK_PURPLE = "#4b0082"
PK_PURPLE = "#483d8b"
PK_PURPLE_FALLBACK = '#800080'
PK_SKY_BLUE = "#1e90ff"
PK_PASTEL_COLOR = "#87cefa"

PK_TEST_COLOR = "#FFFFFF"

PK_SPINNER_COLOR = PK_WHITE
PK_PROMPT_COLOR = PK_WHITE
PK_QUERY_COLOR = PK_ORANGE  # user query color
PK_POINTER_COLOR = PK_WHITE
PK_HL_COLOR = PK_ORANGE  # matched segment color
PK_HL_ACTIVE_COLOR = PK_ORANGE
PK_FG_ACTIVE_COLOR = PK_ORANGE  # hover color
PK_FOOTER_COLOR = PK_PINK

# PK_POINTER_TEXT = "▶"
# PK_POINTER_TEXT = "✅"
# PK_POINTER_TEXT = "🧩"
# PK_POINTER_TEXT = "⚡"
PK_POINTER_TEXT = "🦋"
