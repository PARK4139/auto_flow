from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from bs4 import BeautifulSoup


def get_pk_wsl_mount_d_v2(windows_path: str, path_to_mount: str = 'Downloads/pk_working') -> str:
    # v1 속도 개선 시도
    import os
    import subprocess

    # 윈도우 경로 -> WSL 경로로 변환
    try:
        # sample: C:\Users\WIN10PROPC3\Downloads\Videos → /mnt/c/Users/...
        wsl_path = subprocess.check_output(["wslpath", "-u", windows_path], text=True).strip()
    except Exception as e:
        raise RuntimeError(f"wslpath 변환 실패: {windows_path} → {e}")

    # 실제 마운트 경로를 구성해서 반환
    home_dir = os.path.expanduser("~")
    mounted_path = os.path.join(home_dir, path_to_mount)

    # 최종 경로로 매핑 (사용자 컨벤션에 따라 적절히 조합)
    # 여기서는 그냥 wslpath 결과를 반환하는 형태로 유지
    return wsl_path
