import sys
from pathlib import Path
import traceback

try:
    current_file_path = Path(__file__).resolve()
    project_root_path = current_file_path.parent
    pk_system_path =   project_root_path / "resource" / "pk_system"
    pk_system_sources_path = pk_system_path / "pk_system_sources"

    if str(pk_system_path) not in sys.path:
        sys.path.insert(0, str(pk_system_path))
        
    if str(pk_system_sources_path) not in sys.path:
        sys.path.insert(0, str(pk_system_sources_path))

    from pk_system_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_system_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
    from pk_system_sources.pk_system_functions.ensure_pk_system_wrapper_started import ensure_pk_system_wrapper_started
    from pk_system_functions.ensure_slept import ensure_slept
    
    from source.functions.ensure_wrapper_started import ensure_wrapper_started

    if __name__ == '__main__':
        try:
            while True:
                ensure_wrapper_started()
                ensure_slept(milliseconds=50)

        except KeyboardInterrupt:
            print("\n업무자동화 래퍼가 사용자에 의해 중지되었습니다.")
        except Exception:
            # Log any other exceptions using the pk_system's logging function
            ensure_debug_loged_verbose(traceback)
            print("오류가 발생했습니다. 로그 파일을 확인해주세요.")

except ImportError as e:
    print(f"오류: pk_system 모듈을 가져오는 데 실패했습니다. 경로 설정을 확인해주세요.")
    print(f"sys.path: {sys.path}")
    print(f"Import Error: {e}")
    traceback.print_exc()
