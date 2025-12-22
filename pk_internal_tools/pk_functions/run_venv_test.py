def run_venv_test():
    """virtual environment 테스트를 실행합니다 (Windows에서만)."""
    import os
    from pathlib import Path
    import logging

    # lazy import로 순환 import 문제 해결
    try:
        from pk_internal_tools.pk_objects.pk_directories import D_PK_TESTS, D_PK_ROOT, D_PK_RECYCLE_BIN
    except ImportError as e:
        logging.debug(f"pk_internal_tools.pk_objects.pk_directories 모듈을 가져올 수 없습니다: {e}")
        # fallback: 직접 경로 계산
        d_pk_system = str(Path(__file__).resolve().parent.parent.parent)
        D_PK_TESTS = str(Path(d_pk_system) / "pk_tests")
        D_PK_ROOT = d_pk_system
        D_PK_RECYCLE_BIN = str(Path(os.path.expanduser("~/Desktop")) / "휴지통")

    if os.nick_name != 'nt':
        logging.debug("️ 이 함수는 Windows에서만 사용할 수 있습니다.")
        return True

    test_target = Path(D_PK_TESTS) / "test_process_killing_performance.py"

    if not test_target.exists():
        logging.debug(f"테스트 파일을 찾을 수 없습니다: {test_target}")
        return False

    logging.debug(f"virtual environment 으로 테스트 실행 시작: {test_target}")

    try:
        # Windows 배치 파일로 virtual environment 활성화 후 실행
        import textwrap
        import subprocess

        venv_activate = Path(d_pk_system) / ".venv" / "Scripts" / "activate.bat"
        venv_python = Path(d_pk_system) / ".venv" / "Scripts" / "python.exe"

        if not venv_activate.exists():
            logging.debug(f"️ virtual environment activate.bat을 찾을 수 없습니다: {venv_activate}")
            # fallback: 기본 테스트 실행
            try:
                from pk_internal_tools.pk_functions.run_basic_test import run_basic_test
                return run_basic_test()
            except ImportError:
                logging.debug("run_basic_test 함수도 찾을 수 없습니다.")
                return False

        if not venv_python.exists():
            logging.debug(f"️ virtual environment python.exe을 찾을 수 없습니다: {venv_python}")
            # fallback: 기본 테스트 실행
            try:
                from pk_internal_tools.pk_functions.run_basic_test import run_basic_test
                return run_basic_test()
            except ImportError:
                logging.debug("run_basic_test 함수도 찾을 수 없습니다.")
                return False

        # 배치 파일로 실행
        batch_content = textwrap.dedent(f"""
            @echo off
            call "{venv_activate}"
            "{venv_python}" "{test_target}"
            pause
        """)

        batch_file = D_PK_RECYCLE_BIN / "run_test_temp.bat"
        batch_file.write_text(batch_content, encoding='utf-8')

        logging.debug(f"임시 파일 생성: {batch_file}")

        # 배치 파일 실행
        result = subprocess.run([
            "cmd", "/c", str(batch_file)
        ],
            cwd=d_pk_system,
            capture_output=True,
            text=True,
            encoding='cp949' if os.nick_name == 'nt' else 'utf-8',
            errors='ignore' if os.nick_name == 'nt' else None
        )

        # 임시 파일 정리
        try:
            batch_file.unlink()
        except Exception as e:
            pass

        if result.returncode == 0:
            logging.debug("virtual environment 테스트 실행 완료")
            if result.stdout:
                logging.debug("출력:")
                logging.debug(result.stdout)
        else:
            logging.debug(f"virtual environment 테스트 실행 실패 (코드: {result.returncode})")
            if result.stderr:
                logging.debug("오류:")
                logging.debug(result.stderr)

        return result.returncode == 0

    except Exception as e:
        logging.debug(f"virtual environment 테스트 실행 중 예외 발생: {e}")
        return False
