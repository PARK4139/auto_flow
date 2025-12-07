def get_pnx_from_fzf(pnx=None):
    import os
    import subprocess
    import sys

    try:
        # Windows 환경에서 fzf 실행 (CMD에서 실행되도록)
        if os.name == 'nt':  # Windows
            # CMD에서 fzf 실행하기 위해 dir /b /s | fzf 사용
            if pnx is None:
                cmd = 'dir /b /s "g:" | fzf'  # G: 드라이브에서 파일 선택
            else:
                cmd = f'dir /b /s "{pnx}" | fzf'  # pnx 경로에서 파일 선택

            # CMD에서 명령어 실행
            result = subprocess.run(cmd,
                                    shell=True,
                                    stdin=sys.stdin,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,  # 텍스트 형식으로 출력받기
                                    encoding='utf-8')  # 인코딩을 UTF-8로 설정
        else:  # Linux / WSL 환경
            # Linux / WSL 환경에서는 find 명령어 사용
            if pnx is None:
                cmd = 'find . -type f | fzf'  # 현재 디렉토리에서 fzf 실행
            else:
                cmd = f'find {pnx} -type f | fzf'  # pnx 디렉토리에서 fzf 실행

            # Linux / WSL에서 명령어 실행
            result = subprocess.run(cmd,
                                    shell=True,
                                    stdin=sys.stdin,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    encoding='utf-8')  # 인코딩을 UTF-8로 설정

        # 결과 출력
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        logging.error(f"fzf 실행 중 예외 발생: {e}")
        return None
