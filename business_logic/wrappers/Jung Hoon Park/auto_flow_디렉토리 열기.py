import os
import platform
import subprocess
import sys
import traceback

from business_logic.functions.get_auto_flow_path import get_auto_flow_path
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

try:
    if __name__ == '__main__':
        try:
            auto_flow_repo = get_auto_flow_path()
            system = platform.system()
            if system == "Windows":
                os.startfile(auto_flow_repo)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(auto_flow_repo)])
            else:  # Linux
                subprocess.run(["xdg-open", str(auto_flow_repo)])
        except KeyboardInterrupt:
            print("업무자동화 래퍼가 사용자에 의해 중지되었습니다.")
        except Exception:
            ensure_debug_loged_verbose(traceback)
            print("오류가 발생했습니다. 로그 파일을 확인해주세요.")

except ImportError as e:
    print(f"오류: pk_system 모듈을 가져오는 데 실패했습니다. 경로 설정을 확인해주세요.")
    print(f"sys.path: {sys.path}")
    traceback.print_exc()
