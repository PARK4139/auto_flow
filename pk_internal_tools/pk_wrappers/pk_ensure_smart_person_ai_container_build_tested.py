"""
d_pk_system wrapper for smart_person_ai 컨테이너 빌드 테스트
"""
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pk_internal_tools.pk_functions.pk_ensure_smart_person_ai_container_build_tested import pk_functions


def ensure_smart_person_ai_container_builded_at_wsl():
    print("smart_person_ai 컨테이너 빌드 튜토리얼 실행")
    print("=" * 60)

    try:
        # pk_functions 함수 실행
        result = pk_functions()

        if result:
            print("✅ d_pk_system: 테스트 성공적으로 완료!")
            return True
        else:
            print("❌ d_pk_system: 테스트 실패!")
            return False

    except Exception as e:
        print(f"\n❌ d_pk_system: 예상치 못한 오류 발생: {e}")
        return False


if __name__ == "__main__":
    ensure_smart_person_ai_container_builded_at_wsl()
