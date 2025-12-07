"""
대시보드 서버를 백그라운드로 실행하는 래퍼 (Windows/Linux 호환).
"""
if __name__ == "__main__":
    import traceback
    import logging
    import sys
    import subprocess
    import os
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # 서버 실행 스크립트 경로
        server_wrapper = Path(__file__).parent / "pk_ensure_pk_dashboard_server_started.py"
        
        if not server_wrapper.exists():
            logging.error(f"서버 래퍼 파일을 찾을 수 없습니다: {server_wrapper}")
            sys.exit(1)
        
        logging.info("대시보드 서버를 백그라운드로 시작합니다...")
        
        if is_os_windows():
            # Windows: DETACHED_PROCESS로 백그라운드 실행
            creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            process = subprocess.Popen(
                [str(F_UV_PYTHON_EXE), str(server_wrapper)],
                creationflags=creationflags,
                close_fds=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logging.info(f"서버가 백그라운드에서 시작되었습니다. PID: {process.pid}")
            logging.info("서버를 중지하려면 작업 관리자에서 프로세스를 종료하거나 다음 명령을 사용하세요:")
            logging.info(f"  taskkill /PID {process.pid} /F")
        elif is_os_wsl_linux():
            # Linux/WSL: nohup으로 백그라운드 실행
            process = subprocess.Popen(
                [str(F_UV_PYTHON_EXE), str(server_wrapper)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp,
                start_new_session=True
            )
            logging.info(f"서버가 백그라운드에서 시작되었습니다. PID: {process.pid}")
            logging.info("서버를 중지하려면 다음 명령을 사용하세요:")
            logging.info(f"  kill {process.pid}")
        else:
            # 기타 Linux
            process = subprocess.Popen(
                [str(F_UV_PYTHON_EXE), str(server_wrapper)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp,
                start_new_session=True
            )
            logging.info(f"서버가 백그라운드에서 시작되었습니다. PID: {process.pid}")
            logging.info("서버를 중지하려면 다음 명령을 사용하세요:")
            logging.info(f"  kill {process.pid}")
        
        logging.info("서버가 정상적으로 시작되었습니다.")
        logging.info("로그를 확인하려면 서버 래퍼를 직접 실행하세요.")
        
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

