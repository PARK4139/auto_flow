
import sys

try:
    from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept
    print("✅✅✅ 성공! 'from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept' 임포트가 정상 작동합니다.")
    
    # 함수가 실제 작동하는지 간단히 테스트
    print("⏳ ensure_slept 함수를 100밀리초 동안 호출하여 테스트합니다...")
    ensure_slept(milliseconds=100)
    print("✅ ensure_slept 함수가 성공적으로 실행되었습니다.")

except ImportError as e:
    print(f"❌ 임포트 실패: {e}", file=sys.stderr)
    print("pk_system.pk_sources.pk_functions.ensure_slept 모듈을 찾을 수 없습니다.", file=sys.stderr)
except Exception as e:
    print(f"❌ 예상치 못한 오류 발생: {e}", file=sys.stderr)

