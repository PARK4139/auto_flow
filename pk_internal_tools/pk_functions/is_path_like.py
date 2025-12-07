import zlib

import webbrowser
import tqdm
import sqlite3
import mutagen
import json
import colorama
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical

from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE


def is_path_like(s: str) -> bool:
    import os
    import re
    if not isinstance(s, str):
        return False

    s = s.strip()

    #  URL 은 제외
    if re.match(r'^(https?|ftp)://', s) or re.match(r'^(www\.|youtu\.be|drive\.google\.com)', s):
        return False

    #  절대 경로 (Windows, POSIX)
    if os.path.isabs(s):
        return True

    #  상대 경로라도 디렉토리 구분자 포함되면 (예: a/b, a\b)
    if '/' in s or '\\' in s:
        return True

    #  확장자만 있다고 해서 경로라고 단정하지 않음
    return False
