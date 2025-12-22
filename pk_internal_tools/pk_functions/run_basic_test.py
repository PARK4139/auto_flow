def run_basic_test():
    """기본 테스트를 실행합니다."""
    # lazy import로 순환 import 문제 해결
    try:
        from pk_internal_tools.pk_objects.pk_directories import D_PK_TESTS, D_PK_ROOT
    except ImportError:
        # fallback: 직접 경로 계산
        from pathlib import Path
        d_pk_system = str(Path(__file__).resolve().parent.parent.parent)
        D_PK_TESTS = str(Path(d_pk_system) / "tests")

    # 필요한 모듈들 lazy import
    try:
        import logging
        from pathlib import Path
        import os
        import subprocess
        import sys
    except ImportError as e:
        print(f" 필요한 모듈을 가져올 수 없습니다: {e}")
        return False

    test_target = Path(D_PK_TESTS) / "test_process_killing_performance.py"

    if not test_target.exists():
        logging.debug(f"테스트 파일을 찾을 수 없습니다: {test_target}")
        return False

    logging.debug(f"테스트 실행 시작: {test_target}")

    try:
        # Windows에서 인코딩 문제 해결
        if os.name == 'nt':
            # Windows: cp949 또는 utf-8 with errors='ignore'
            try:
                result = subprocess.run([
                    sys.executable,  # 현재 실행 중인 Python
                    str(test_target)
                ],
                    cwd=D_PK_ROOT,  # 프로젝트 루트에서 실행
                    capture_output=True,
                    text=True,
                    encoding='cp949',
                    errors='ignore'
                )
            except UnicodeDecodeError:
                # cp949 실패 시 utf-8 with errors='ignore' 시도
                result = subprocess.run([
                    sys.executable,  # 현재 실행 중인 Python
                    str(test_target)
                ],
                    cwd=D_PK_ROOT,  # 프로젝트 루트에서 실행
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
        else:
            # Linux/macOS: utf-8
            result = subprocess.run([
                sys.executable,  # 현재 실행 중인 Python
                str(test_target)
            ],
                cwd=D_PK_ROOT,  # 프로젝트 루트에서 실행
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

        if result.returncode == 0:
            logging.debug("테스트 실행 완료")
            if result.stdout:
                logging.debug("출력:")
                logging.debug(result.stdout)
        else:
            logging.debug(f"테스트 실행 실패 (코드: {result.returncode})")
            if result.stderr:
                logging.debug("오류:")
                logging.debug(result.stderr)

        return result.returncode == 0

    except Exception as e:
        logging.debug(f"테스트 실행 중 예외 발생: {e}")
        return False
