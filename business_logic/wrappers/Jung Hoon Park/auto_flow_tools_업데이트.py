import subprocess
import sys
from pathlib import Path

# 프로젝트 루트 경로를 동적으로 계산합니다.
# 현재 파일 (ensure_pk_system_update.py) -> Jung_Hoon_Park -> wrappers -> source -> 프로젝트 루트
D_PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent

def ensure_pk_system_update():
    """
    scripts/install_pk_system.cmd 스크립트를 실행하여 pk_system을 업데이트합니다.
    """
    install_script_path = D_PROJECT_ROOT_PATH / "scripts" / "install_pk_system.cmd"

    if not install_script_path.is_file():
        print(f"오류: 설치 스크립트를 찾을 수 없습니다: {install_script_path}", file=sys.stderr)
        sys.exit(1)

    print(f"pk_system 업데이트 스크립트를 실행합니다: {install_script_path}")
    print("-" * 50)

    try:
        # .cmd 파일을 직접 실행합니다.
        # shell=True를 사용하면 Windows에서 .cmd 파일을 직접 실행할 수 있습니다.
        # 하지만 보안상의 이유로 shell=True는 지양되므로, 명시적으로 powershell을 호출합니다.
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-Command', f'"{install_script_path}"'],
            capture_output=True,
            text=True,
            check=True,  # 오류 발생 시 CalledProcessError 발생
            encoding='utf-8',
            errors='replace'
        )
        print("스크립트 실행 결과:")
        print(result.stdout)
        if result.stderr:
            print("오류 출력:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
        
        print("-" * 50)
        print("pk_system 업데이트 스크립트 실행 완료.")

    except subprocess.CalledProcessError as e:
        print(f"오류: 스크립트 실행 중 문제가 발생했습니다. 종료 코드: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print("표준 출력:", file=sys.stderr)
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print("오류 출력:", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("오류: powershell.exe를 찾을 수 없습니다. PATH 설정을 확인해주세요.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    ensure_pk_system_update()
