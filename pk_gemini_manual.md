# pk_프롬프트 for AI_HANSTER based on gemini.cli
# 장기 메모리관리
/memory add 나는 항상 한국어로 답변을 받는 것을 선호한다.
/memory add 나는 설명을 단계적으로 해주되, 불필요하게 장황하지 않은 정리된 답변을 선호한다.
/memory add 나는 AI 소프트웨어 개발자이며 Python 기반 자동화와 백엔드 개발을 주로 한다.
/memory add 나는 Windows, WSL, Linux를 모두 사용하며, 세 환경에서 모두 동작하는 솔루션을 원한다.
/memory add 나는 Python 패키지 관리를 uv로 하고, FastAPI와 Django, Docker, PostgreSQL을 자주 사용한다.
/memory add 패키지 추가 시 종속성 관리를 위해 uv add 명령어로 추가하는 것을 선호한다.
/memory add 나는 로컬 개발과 배포 환경에서 Docker 컨테이너를 활용하는 예시와 설명을 선호한다.
/memory add 나는 pk_system이라는 대규모 개인 라이브러리/툴체인을 사용하고 있으며, 이 구조와 호환되는 예시 코드를 선호한다.
/memory add 나는 외부 프로젝트에서 pk_system을 read-only 라이브러리처럼 import 해서 사용하는 패턴을 자주 쓴다.
/memory add 나는 코드와 주석은 영어로 작성하되, 설명과 안내는 한국어로 받는 것을 선호한다.
/memory add 나는 함수 이름을 ensure_로 시작하고 완료형 동사를 접미사로 붙이는 네이밍 규칙을 사용한다.
/memory add 나는 Python 코드에서 가능한 한 lazy import 패턴을 사용하는 예시를 선호한다.
/memory add 나는 로깅은 Python logging 모듈을 사용하고, 표준 포맷(LEVEL, 파일명:라인, 메시지 등)을 따르는 방식을 선호한다.
/memory add 나는 코드를 제시할 때 부분 생략 없이 전체를 한 번에 복사해서 붙여넣기 쉬운 형태로 제공해 주기를 원한다.
/memory add 나는 워드/문서 스타일의 출력에서는 인위적으로 보이는 과한 서식이나 눈에 띄는 AI 티 나는 형식을 피하는 자연스러운 표현을 선호한다.
/memory add QC_MODE가 True인 경우 최신 시스템 로그는 pk_system.log에서 확인해야 한다.


# chat 별 메모리관리 
/chat save pk_chat 
/chat resume pk_chat # bring previous_chat_memory