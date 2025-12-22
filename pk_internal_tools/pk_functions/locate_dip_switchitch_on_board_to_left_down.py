import pyaudio
import numpy as np

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from mutagen.mp3 import MP3

from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def locate_dip_switchitch_on_board_to_left_down():
    # if no:
    #     left_down # 위치 재확인필요
    #     #         2개 스위치 제외(A/B selector, S/W 5) # 위치 재확인필요
    todo('%%%FOO%%%')
