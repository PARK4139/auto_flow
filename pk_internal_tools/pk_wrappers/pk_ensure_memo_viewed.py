
import sys
from pathlib import Path

# 프로젝트 루트 경로를 sys.path에 추가하여 모듈을 찾을 수 있도록 합니다.
# 이 코드는 pk_internal_tools가 현재 작업 디렉토리의 하위 디렉토리라고 가정합니다.
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# 이제 pk_internal_tools 내의 모듈을 임포트할 수 있습니다.
from pk_internal_tools.pk_functions.ensure_memo_viewed import 메모_조회, 일정, 관심헤어샵들

def main():
    """메모 조회 기능을 실행하는 메인 함수"""
    print("메모 조회 래퍼 스크립트를 실행합니다.")
    
    # '일정' 함수의 소스 코드를 조회합니다.
    메모_조회(일정)
    
    print("\n" + "="*50 + "\n")
    
    # '관심헤어샵들' 클래스의 소스 코드를 조회합니다.
    메모_조회(관심헤어샵들)

if __name__ == '__main__':
    main()
