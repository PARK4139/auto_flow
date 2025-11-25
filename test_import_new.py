
import sys
import os

try:
    # 새로운 임포트 경로를 테스트합니다.
    from pk_system.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    
    # 함수가 실제로 호출되는지 간단히 확인 (실행은 하지 않음)
    print("✅ Successfully imported ensure_debug_loged_verbose from pk_system.pk_functions.")

except ImportError as e:
    print(f"❌ ImportError: {e}")
    print("pk_system을 새로운 경로로 임포트하는 데 실패했습니다.")
    print("현재 sys.path:", sys.path)
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")

