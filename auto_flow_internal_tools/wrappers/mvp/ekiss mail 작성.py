
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path to allow imports from other directories
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_root))

from auto_flow_internal_tools.functions.write_ekiss_mail import write_ekiss_mail

def main():
    """
    Wrapper script to run the eKiss mail writing automation.
    This script sets up the environment and calls the main function.
    """
    print("--- eKiss 메일 쓰기 자동화 시작 ---")
    
    # Load environment variables from .env_test file at the project root
    env_path = project_root / '.env_test'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"환경 변수를 '{env_path}' 파일에서 로드했습니다.")
    else:
        print(f"경고: '{env_path}' 파일을 찾을 수 없습니다. 기존 환경 변수에 의존합니다.")

    # Instructions for the user
    print("\n사전 준비 사항:")
    print('1. Chrome 브라우저가 디버깅 모드로 실행되어 있어야 합니다.')
    print('   예: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
    print('2. 스크립트가 eKiss 로그인 페이지를 열면 직접 로그인해주세요.')
    
    # Execute the main function
    try:
        write_ekiss_mail()
        print("\n--- eKiss 메일 쓰기 자동화 완료 ---")
        print("브라우저에서 메일 쓰기 창이 열렸는지 확인해주세요.")
    except Exception as e:
        print(f"\n오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
