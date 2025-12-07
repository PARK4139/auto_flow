import time
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles

from pk_internal_tools.pk_functions.ensure_video_playied_at_losslesscut import ensure_video_playied_at_losslesscut


def is_editing_or_exporting(titles):
    for title in titles:
        if "출력" in title or "Export" in title or "편집" in title or "Edit" in title:
            return True
    return False


def auto_load_and_play(video_path, check_interval=2.0):
    while True:
        titles = get_window_titles()
        if is_editing_or_exporting(titles):
            print("편집/출력 중이므로 대기...")
        else:
            print("자동 로드/재생 시도")
            ensure_f_video_loaded_on_losslesscut(video_path)
            time.sleep(1)
            ensure_video_playied_at_losslesscut()
            print("비디오 로드 및 재생 완료")
            break
        time.sleep(check_interval)

# example
# auto_load_and_play(r"C:\path\to\your\video.mp4")
