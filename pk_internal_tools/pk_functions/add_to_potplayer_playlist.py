from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE


def add_to_potplayer_playlist(file_path: str):
    import shlex
    import subprocess

    # 파일 경로에 공백·특수문자 포함될 수 있으므로 shlex.quote로 안전하게 감싸기
    safe_file = shlex.quote(file_path)
    cmd = f'"{F_POT_PLAYER_EXE}" {safe_file} /add'
    try:
        # blocking 실행 방식
        ret = subprocess.call(cmd, shell=True)
        if ret != 0:
            print(f"[에러] PotPlayer 명령 실패 (exit {ret}): {cmd}")
    except Exception as e:
        print(f"[예외] PotPlayer 재생목록 추가 실패: {e}")
