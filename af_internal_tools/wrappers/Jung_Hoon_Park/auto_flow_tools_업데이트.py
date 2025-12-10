import sys
from pathlib import Path
import traceback
import subprocess # Moved up as it's used in main logic



from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

# 프로젝트 루트 경로를 동적으로 계산합니다. (이제 sys.path에 있으므로 직접 Path를 사용)
# D_PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent # No longer needed, as d_pk_root is project root

def ensure_pk_system_update():
    """
    scripts/install_pk_system.cmd 스크립트를 실행하여 pk_system을 업데이트합니다.
    """
    import logging
    install_script_path = d_pk_root / "scripts" / "install_pk_system.cmd"

    if not install_script_path.is_file():
        logging.error(f"오류: 설치 스크립트를 찾을 수 없습니다: {install_script_path}")
        sys.exit(1)

    logging.info(f"pk_system 업데이트 스크립트를 실행합니다: {install_script_path}")
    logging.info("-" * 50)

    try:
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-Command', f'"{install_script_path}"'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        logging.info("스크립트 실행 결과:")
        logging.info(result.stdout)
        if result.stderr:
            logging.error("오류 출력:")
            logging.error(result.stderr)
        
        logging.info("-" * 50)
        logging.info("pk_system 업데이트 스크립트 실행 완료.")

    except subprocess.CalledProcessError as e:
        logging.error(f"오류: 스크립트 실행 중 문제가 발생했습니다. 종료 코드: {e.returncode}")
        if e.stdout:
            logging.error("표준 출력:")
            logging.error(e.stdout)
        if e.stderr:
            logging.error("오류 출력:")
            logging.error(e.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        logging.error("오류: powershell.exe를 찾을 수 없습니다. PATH 설정을 확인해주세요.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"예상치 못한 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))
        ensure_pk_system_update()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
