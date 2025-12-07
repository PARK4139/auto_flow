import logging


def merge_silent_mp3_and_ment_mp3_and_ment__mp3_via_ffmepeg(ment_mp3, ment__mp3):
    import os

    """
    앞부분 소리가 들리지 않는 현상
    전체 소리가 다 들려야 하는데
    앞부분의 단어가 들리지 않은채로 소리가 들린다.
    음악f의 앞부분에 빈소리를 추가
    ffmpeg를 이용하여 silent.mp3(1초간 소리가 없는 mp3 f)을 소리를 재생해야할 mp3 f의 앞부분에 합쳐서 재생
    """
    silent_mp3 = F_SILENT_MP3
    if not os.path.exists(silent_mp3):
        logging.debug(rf"사일런트 mp3 f({silent_mp3})이 없습니다")
        raise
    if not os.path.exists(ment_mp3):
        cmd = rf'echo y | "ffmpeg" -i "concat:{os.path.abspath(silent_mp3)}|{os.path.abspath(ment__mp3)}" -acodec copy -metadata "title=Some Song" "{os.path.abspath(ment_mp3)}" -map_metadata 0:-1  >NUL 2>&1'
        ensure_command_executed_like_human_as_admin(cmd)
