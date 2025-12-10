
import pytest
from af_internal_tools.functions.write_ekiss_mail import write_ekiss_mail
from dotenv import load_dotenv
from pathlib import Path
import os

def test_write_ekiss_mail():
    """
    write_ekiss_mail 함수를 테스트합니다.
    
    **사전 준비:**
    1. Chrome 브라우저가 디버깅 모드로 실행되어 있어야 합니다.
       cmd에서 다음 명령어 실행: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"
    2. eKiss 사이트에 미리 로그인되어 있어야 합니다.
    3. .env_test 파일에 EKISS_URL이 정의되어 있어야 합니다.
    """
    # .env_test 파일 로드
    env_path = Path(__file__).resolve().parent.parent / '.env_test'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        print(f"Warning: '{env_path}' not found. Relying on existing environment variables.")

    if not os.getenv("EKISS_URL"):
        pytest.fail("EKISS_URL 환경 변수가 설정되지 않았습니다.")

    print("--- eKiss 메일 쓰기 자동화 테스트 시작 ---")
    print("사전 준비 사항을 확인해주세요:")
    print('1. Chrome 디버깅 모드 실행 (port 9222)')
    print('2. eKiss 사이트 로그인 완료')
    
    # 함수 실행
    write_ekiss_mail()
    
    print("--- 테스트 완료 ---")
    print("브라우저에서 메일 쓰기 창이 열렸는지 확인해주세요.")
    # 실제 클릭이 일어나는지, 페이지 이동이 정상적인지는 수동으로 확인해야 함
    # 자동화된 UI 테스트로는 한계가 있음

if __name__ == '__main__':
    pytest.main([__file__])
