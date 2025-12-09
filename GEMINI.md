# Cursor AI 프로젝트 규칙
# 이 파일은 Cursor AI가 프로젝트에서 따라야 할 규칙들을 정의합니다.

## 🚫 NUL 파일 자동 삭제 규칙

### **NUL 파일 감지 및 삭제**
- **Windows 특수 파일**: `nul`, `con`, `prn`, `aux` 등의 Windows 특수 파일은 즉시 삭제
- **빈 파일**: 내용이 없는 파일이나 0바이트 파일은 프로젝트에서 제거
- **시스템 파일**: `Thumbs.db`, `*.tmp`, `*.temp` 등은 무시

### **NUL 파일 생성 방지**
- **파일 생성 시**: `nul`이라는 이름의 파일이나 디렉토리 생성 금지
- **명령어 실행 시**: `nul`을 출력으로 사용하는 명령어 실행 금지
- **스크립트 작성 시**: `nul` 파일을 참조하는 코드 작성 금지

### **자동 정리 규칙**
- **Git 상태 확인 시**: `nul` 파일이 발견되면 자동으로 `git rm --cached` 실행
- **프로젝트 스캔 시**: `nul` 파일이 발견되면 즉시 삭제 제안
- **커밋 전**: `nul` 파일이 스테이징된 경우 자동으로 제거

## 🔧 프로젝트 품질 관리

### **파일 무결성**
- **Windows 특수 문자**: 파일명에 Windows 예약어 사용 금지
- **경로 처리**: `pathlib.Path` 객체 사용으로 안전한 경로 처리
- **크로스 플랫폼**: Windows, Linux, WSL 환경 모두에서 안전하게 동작

### **코드 품질**
- **함수명 규칙**: `ensure_` 접두사 사용. (단, `is_` 또는 `get_`으로 시작하는 함수는 예외)
- **파일명 규칙**: `.py`, `.sh`, `.cmd`, `.bat`, `.ps1` 파일에 `ensure_` 접두사. (단, `is_` 또는 `get_`으로 시작하는 파일은 예외)
- **테스트 코드**: `test_` 접두사로 테스트 파일 작성

## 🧪 Pytest 테스트 규칙

### **테스트 실행**
- **실행 명령어**: 프로젝트 루트 디렉토리에서 `pytest` 명령어를 사용하여 모든 테스트를 실행합니다.
- **가상 환경**: 테스트는 `.venv` 가상 환경에 설치된 `pytest`를 사용하여 실행해야 합니다. `run.py`를 먼저 실행하여 환경을 설정하는 것을 권장합니다.
- **실행 방법**:
  1. `.venv\Scripts\activate` (Windows) 또는 `source .venv/bin/activate` (Linux/macOS)를 통해 가상 환경을 활성화합니다.
  2. `pytest` 명령어를 실행합니다.

### **테스트 작성**
- **테스트 위치**: 모든 테스트 코드는 `tests/` 디렉토리 안에 위치해야 합니다.
- **파일명 규칙**: 테스트 파일명은 `test_*.py` 또는 `*_test.py` 패턴을 따라야 합니다.
- **함수명 규칙**: 테스트 함수명은 `test_` 접두사로 시작해야 합니다.
- **Assertion**: 테스트의 성공/실패를 명확히 판단하기 위해 `assert` 문을 적극적으로 사용해야 합니다. 로그 확인이나 수동 검증에 의존하는 테스트는 지양합니다.

## 📝 작업 흐름 규칙

### **파일 생성 시**
1. `nul` 파일명 사용 금지
2. Windows 예약어 사용 금지
3. 안전한 파일명 사용

### **명령어 실행 시**
1. `nul` 출력 사용 금지
2. 안전한 리다이렉션 사용
3. 오류 처리 포함

### **Git 작업 시**
1. `nul` 파일 자동 감지
2. 발견 시 즉시 제거
3. `.gitignore`에 적절한 패턴 추가

### **테스트 워크플로우 규칙**
- **수동 테스트**: `ensure_draft_scenario_executed()` 함수를 통해 주요 기능의 시나리오를 수동으로 테스트합니다.
- **자동 테스트**: `test_scenarios.py` 래퍼 파일을 직접 실행하여 자동화된 단위 테스트를 수행합니다.

### **사용자 이해도 규칙**
- **다수 사용자 이해**: 현재 프로젝트는 다수의 사용자가 이해하기 쉽도록 작성되어야 합니다. 코드, 문서, 인터페이스 등 모든 요소는 명확하고 직관적으로 설계되어야 합니다.

## 🎯 목표

**이 프로젝트는 `nul` 파일이 생성되지 않는 깨끗한 환경을 유지합니다.**

- ✅ **NUL 파일 자동 감지 및 삭제**
- ✅ **Windows 특수 파일 생성 방지**
- ✅ **프로젝트 품질 자동 관리**
- ✅ **크로스 플랫폼 호환성 보장**

---

## 🚀 프로젝트 작업규칙

### **프로젝트 규칙 추가**
- **`pk_system` 서브시스템**: `pk_system`은 서브시스템이며 현재 프로젝트 `autoflow` 내에서 특별한 작업 지시를 제외하고 수정하지 않고 호출해서 사용만 합니다.

### **규칙 적용 범위**
- **`autoflow` 프로젝트 규칙**: `autoflow` 프로젝트는 `pk_system`의 기본 규칙을 기반으로 시작되었으나, 향후 `autoflow` 프로젝트의 특성과 요구사항에 맞춰 규칙을 변경하고 발전시킬 수 있습니다. `pk_system` 규칙은 `autoflow` 프로젝트의 독립적인 규칙에 우선하지 않습니다.

### **개발 환경 규칙**
- **파이썬 환경**: `uv` + `pyproject.toml` + `uv.lock` 기반 virtual environment 사용
- **virtual environment 규칙**: `.venv_windows`와 `.venv_linux` 디렉토리는 사용하지 않음, `.venv`만 사용
- **OS별 virtual environment **: Windows, Linux/WSL 모두 `.venv` 사용
- **서비스 환경**: Linux/Docker + docker-compose 기반 환경 구성
- **CLI 래퍼**: `pk_ensure` 접두사로 시작하는 파일들은 CLI 모드 실행 시 래퍼 파일

### **자동 실행 규칙**
- **가상 환경 직접 활성화**: `uv run`을 사용하는 대신, OS에 맞는 가상 환경을 직접 활성화하여 스크립트를 실행합니다. (예: Windows에서는 `.venv_windows\Scripts\activate` 실행 후 `python a.py`)
- **터미널 도구**: `시스템 터미널` 안되면 `커서 내장 터미널` 이나 다른터미널 사용, 안되면 반대순서로도 시도
- **커서 내장 터미널**: 명령어응답이 안오면 `bash -c`, `zsh -c 방식` 으로도 시도, 안되면 반대순서로도 시도
- **그래도 안되면**: Cursor 터미널 재실행
- **Windows PowerShell 인코딩**: PowerShell 환경에서 한글 깨짐 방지를 위해 `chcp 65001` 명령어를 실행하여 UTF-8 인코딩을 설정합니다.
- **Gemini 작업 완료 알림**: Gemini 작업이 완료될 때마다 (반복적으로) `pk_ensure_gemini_cli_worked_done.py`를 실행하여 음성으로 알림.
  - **실행 방법**: `.venv_windows\Scripts\activate`를 실행하여 가상 환경을 활성화한 후, `python C:\Users\wjdgn\Downloads\pk_system\pk_internal_tools\pk_system_wrappers\pk_ensure_gemini_cli_worked_done.py` 명령을 실행합니다.
- **Gemini 작업 완료 알림 예외**: `pk_ensure_gemini_cli_worked_done.py` 스크립트는 사용자의 사전 동의를 얻었으므로, 작업 완료 후 별도의 확인 없이 즉시 실행합니다.

### **규칙 동기화 규칙**
- **규칙 업데이트 동기화**: `GEMINI.md` 파일이 업데이트될 경우, `.cursor/rules` 디렉토리의 관련 규칙도 동일하게 업데이트해야 합니다.

### **파일 및 디렉토리 관리 규칙**
- **레거시 파일**: `deprecated`된 기존 버전 파이썬 파일에는 `# ` 접두사를 붙여서 rename
- **Git Push 금지 파일**: `.env` 파일과 `.pk_system` 파일/디렉토리는 절대 Git에 push 되면 안 됩니다. `.gitignore`에 포함되어 있으며, 실수로 커밋된 경우 `git rm --cached` 명령으로 즉시 제거해야 합니다.

### **파일 정리 규칙**
- **백업 파일**: `# ` 접두사가 붙은 파일들은 **레거시/백업 파일**로 안전하게 삭제 가능
- **임시 파일**: `fix/` 디렉토리의 파일들은 **문제 해결용 임시 파일**로 필요시에만 사용
- **자동 생성 파일**: `run_python_direct.py` 같은 자동 생성 파일은 **필요시 언제든 재생성 가능**

### **프로젝트 구조 이해**
- **메인 함수**: `pk_internal_tools/pk_functions/`이 **메인 함수들**이 위치한 핵심 디렉토리 (functions_split 대신)
- **실행 스크립트**: `pk_system_resources/pk_ensure_*.py` 파일들이 **직접 실행 가능한 스크립트**들
    - **시스템 시작 우선순위**: UV → Shell 스크립트 → Python 직접 실행 → 백업용 순서로 실행

### **코드 작성 규칙**
- **다국어 지원**: 모든 프로그램은 다국어 지원 가능하도록 작성 (PkMessage2025 객체 적극 활용)
- **이모지 제외**: 코드 작성 시 이모지 사용 금지
- **함수명 규칙**: 함수명은 `ensure_` 접두사로 시작. (단, `is_` 또는 `get_`으로 시작하는 함수는 예외)
- **파일명 규칙**: `.py`, `.sh`, `.cmd`, `.bat`, `.ps1` 파일에 `ensure_` 접두사. (단, `is_` 또는 `get_`으로 시작하는 파일은 예외)
- **테스트 코드**: `test_` 접두사로 테스트 파일 작성

### **TTS 캐시 관리 규칙**
- **캐시 위치**: TTS 관련 MP3 캐시 파일은 `D_LOGS/tts_cache/` 디렉토리에 저장
- **캐시 정리**: 테스트 전 기존 TTS 캐시 파일들은 모두 삭제하여 깨끗한 상태 유지
- **캐시 파일명**: `{hash}_{language}_{gender}.mp3` 형태로 성별과 언어 정보 포함
- **캐시 관리**: TTS 테스트 시 새로운 캐시 파일 생성 및 기존 파일과 비교 검증

### **하드코딩 방식 선호 규칙**
- **CLI 인자 vs 하드코딩**: 명령줄 인자를 받는 형식보다는 하드코딩 방식을 선호
- **옵셔널 하드코딩 표기**: 하드코딩된 코드 중 옵셔널한 부분에는 `# pk_option` 주석으로 표기
- **가독성 우선**: 복잡한 argparse보다는 직관적인 하드코딩 값 사용
- **유지보수성**: 옵션 변경이 필요한 부분은 `# pk_option` 주석으로 쉽게 식별 가능

### **경로 처리 규칙**
- **Path 객체 사용**: 모든 파일 경로는 `pathlib.Path` 객체를 사용하여 작성
- **문자열 경로 금지**: 하드코딩된 문자열 경로 사용 금지 (예: `"C:\Users\pk\Downloads"`)
- **동적 경로 감지**: `Path.home()`, `os.environ.get('USERPROFILE')` 등을 사용하여 사용자별 경로 자동 감지
- **크로스 플랫폼**: Windows와 Linux 환경 모두에서 안전하게 동작하도록 Path 객체 활용
- **경로 결합**: `Path(userprofile) / "Downloads" / "pk_system"` 형태로 경로 결합
- **경로 검증**: `Path.exists()`, `Path.is_dir()`, `Path.is_file()` 등으로 경로 유효성 검증

### **테스트 코드 규칙**
- **테스트 파일**: `test_` 접두사를 붙여 명시적으로 작성
- **테스트 위치**: `pk_system_tests` 폴더에서 작성
- **로깅 설정**: 테스트 코드 작성 시, `logging.basicConfig()`를 호출하지 않고 `ensure_pk_system_log_initialized(__file__)`를 호출하여 프로젝트의 표준 로깅을 사용합니다.
- **특정 테스트 래퍼**: `pk_ensure_draft_scenario_executed.py` 파일은 테스트 시나리오 실행을 위한 특정 래퍼 스크립트입니다.

### **테스트 실행 환경 규칙**
- **virtual environment 자동 활성화**: 테스트 실행 시 OS 환경에 따라 자동으로 적절한 virtual environment 활성화
- **Windows 환경**: `.venv_windows` 디렉토리의 virtual environment 사용 (`uv` 또는 `python -m venv`)
- **Linux/WSL 환경**: `.venv_linux` 디렉토리의 virtual environment 사용 (`uv` 우선, 없으면 `python3`)
- **virtual environment 우선순위**: `uv` → `python -m venv` → `python3` → `python` 순서로 시도
- **테스트 실행 전**: 반드시 virtual environment 활성화 상태 확인 및 의존성 설치 (`uv sync --active` 또는 `pip install -r requirements.txt`)
- **크로스 플랫폼 테스트**: Windows, Linux, WSL 환경 모두에서 동일한 테스트 결과 보장
- **자동 테스트 환경**: 자동 테스트는 `uv .venv_windows` 환경에서 수행해야 합니다.

### **LTA (Local Test Activate) 규칙**
- **테스트 모드 플래그**: `LTA` 변수를 통해 테스트 모드와 일반 모드 구분
- **테스트 환경 감지**: `pk_internal_tools/pk_objects/pk_local_test_activate.py`에서 LTA 상태 확인
- **하드 코딩 테스트**: LTA 모드에서만 테스트용 하드 코딩된 값 사용 (URL, 설정 등)
- **일반 모드 보호**: LTA가 False일 때는 사용자 입력이나 동적 값 사용
- **테스트 코드 분리**: LTA 모드와 일반 모드의 로직을 명확하게 분리하여 작성
- **테스트 데이터 관리**: LTA 모드에서 사용하는 테스트 데이터는 별도로 관리 및 주석 처리
- **환경별 동작**: 개발/테스트 환경에서는 LTA=True, 프로덕션 환경에서는 LTA=False로 설정

### **virtual environment 마이그레이션 규칙**
- **기본 virtual environment **: `.venv_windows` 및 `.venv_linux` 디렉토리는 더 이상 사용하지 않음
- **OS별 virtual environment **: `.venv` (Windows, Linux/WSL) 사용
- **uv sync 명령어**: `uv sync --active` 사용하여 현재 활성화된 virtual environment 에 의존성 설치
- **경로 참조 수정**: 프로젝트 내 모든 `.venv` 경로를 OS별 virtual environment 경로로 수정
- **virtual environment 활성화**: OS 감지 후 자동으로 적절한 virtual environment 활성화

### **경로 처리 규칙**
- **Path 객체 활용**: 파이썬에서 파일 및 디렉토리 경로 처리 시 Path 객체 사용
- **레거시 변환**: str path 사용 시 Path 객체로 변환 (예: `D_PKG_WINDOWS` → `Path(D_PKG_WINDOWS)`)

### **코드 구조 규칙**
- **클래스 작성**: `pk_internal_tools/pk_objects`에 작성
- **함수 작성**: `pk_internal_tools/pk_functions`에 작성 (function_split 대신)
- **래퍼 패턴**: pk_internal_tools에 래퍼 작성 시 주변 래퍼의 패턴을 비교하여 재생성

### **함수 저장 위치 규칙**
- **기본 저장 위치**: 모든 함수는 `pk_internal_tools/pk_functions/` 디렉토리에 저장
- **function_split 대체**: 기존 `pk_system_resources/function_split/` 대신 `pk_internal_tools/pk_functions/` 사용
- **일관성 유지**: 프로젝트 전체에서 함수 저장 위치 통일
- **파일명 규칙**: 함수 파일명은 `ensure_` 접두사 사용 (예: `ensure_cmd_exe_killed.py`). (단, `is_` 또는 `get_`으로 시작하는 파일은 예외)
- **디렉토리 구조**: 함수별로 독립적인 파일로 분리하여 유지보수성 향상

### 객체 저장 위치 규칙
- **기본 저장 위치**: 모든 클래스와 객체는 `pk_internal_tools/pk_objects/` 디렉토리에 저장
- **객체 분류**: State, Event, Handler, System, Machine 등 객체 관련 클래스는 pk_objects에 저장
- **일관성 유지**: 프로젝트 전체에서 객체 저장 위치 통일
- **파일명 규칙**: 객체 파일명은 기능별로 명확하게 구분 (예: `jarvis_state.py`, `losslesscut_pk_system_event.py`)
- **디렉토리 구조**: 객체별로 독립적인 파일로 분리하여 유지보수성 향상

### 객체 직렬화 규칙 (to_json)
- **`to_json()` 메서드 구현**: `pk_internal_tools/pk_objects/`에 작성되는 모든 시스템 객체(데이터 클래스 등)는 `to_json()` 메서드를 반드시 포함해야 합니다.
- **역할**: 이 메서드는 객체의 데이터를 외부 시스템과 연동하기 위한 표준 JSON 문자열로 변환하는 책임을 집니다.
- **구현 방식**: `dataclasses.asdict()`나 유사한 방법을 통해 객체를 딕셔너리로 변환한 후, `json.dumps(..., ensure_ascii=False, indent=4)`를 사용하여 JSON 문자열을 생성합니다.

### **보안 규칙**
- **민감정보 경고**: 비밀번호, API 키 등 민감한 개인정보가 포함된 컨텐츠에 대해 경고 요청
- **Git Push 금지 파일**: `.env` 파일과 `.pk_system` 파일/디렉토리는 절대 Git에 push 되면 안 됩니다. 이 파일들은 `.gitignore`에 포함되어 있으며, 실수로 커밋된 경우 즉시 제거해야 합니다.

### **세부 요청 유형**
- **코드 리뷰 및 개선**: 기존 코드의 품질 향상 및 최적화
- **버그 해결**: 발생한 문제점의 원인 분석 및 해결 방안
- **아이디어 브레인스토밍**: 새로운 기능이나 개선 방안에 대한 아이디어 논의
- **콘텐츠 작성 보조**: 문서나 설명서 작성에 대한 도움
- **창작 방향 설정**: 프로젝트의 방향성이나 구조에 대한 튜토리얼
- **개념 설명 요청**: 특정 기술이나 개념에 대한 이해 도움
- **자료 정리 및 요약**: 복잡한 정보의 정리 및 핵심 요약
- **연구 방향 설정**: 기술 조사나 연구 주제 설정에 대한 튜토리얼

### **프로젝트 설계기획 규칙**
- **설계달성목표**: SEO 성능 우수, 멀티플랫폼(PC/스마트폰/웹) 지원, 유지보수용의, 뛰어난 UX
- **적용 디자인패턴**: DDD 아키텍처 적용, MSA 적용, Docker-container는 MSA 단위로 구성
- **환경구성요소**: 서버운영환경(AWS EC2), 도커환경(docker-compose, docker-compose.dev, docker-compose.prod), 파이썬virtual environment (python1.13 이상, uv.lock, pyproject.toml)
- **서버구조**: vercel/page 서버(Next.js + TypeScript + Tailwind CSS + Zustand + NextAuth.js / React Native OAuth), AWS EC2/api서버(fastapi), AWS EC2/DB서버(postrege, Database 테이블 개수는 최소화하여 운영)
- **함수 저장 표준**: 모든 함수는 `pk_internal_tools/pk_functions/` 디렉토리에 저장하여 일관성 유지

### **프로젝트 구조 규칙**
- **트리구조**:
  - `af_internal_tools/`: **autoflow** 프로젝트의 핵심 비즈니스 로직을 포함하는 디렉토리. `login_ehr.py`와 같이 autoflow에 특화된 기능들이 여기에 위치합니다.
  - `pk_system_resources/`: 정적 파일 및 외부 소스 리소스 디렉토리.
  - `pk_internal_tools/`: `pk_system`의 핵심 기능을 담고 있는 공유 가능한 파이썬 소스 코드의 최상위 루트 디렉토리.
  - `pk_system_tests/`: 테스트용 스크립트, 파일명에 `test_` prefix 패턴적용.
  - `pk_system_prompts/`: AI 기반 코드생성 명령용 프롬프트 모음.
  - `pk_system_logs/`: 프로그램 실행 결과를 저장하는 로그 디렉토리.
  - `pk_system_docs/`: 프로젝트 관련 문서.
  - `pk_system_cache/`: 시스템 캐시 파일.
  - `pk_system_sensitive/`: 민감한 정보 및 사용자별 설정 파일.
- **함수 저장 위치**:
  - **autoflow 전용 함수**: `af_internal_tools/functions/`에 저장.
  - **공용 함수**: `pk_internal_tools/pk_functions/` 디렉토리에 저장.
- **객체 저장 위치**: 모든 클래스는 `pk_internal_tools/pk_objects/` 디렉토리에 저장.

### **URLs 패턴 규칙**
- **page 서버, api 서버 url 라우터에 적용**:
  - `heal_base_hospital_worker/v1/api/ensure/login/`: 로그인 api
  - `heal_base_hospital_worker/v1/page/ensure/login/`: 로그인 (메인화면)
  - `heal_base_hospital_worker/v1/page/ensure/login-guide/`: 로그인 (튜토리얼)
  - `heal_base_hospital_worker/v1/page/ensure/login-via-google`: 로그인 (구글)
  - `heal_base_hospital_worker/v1/page/ensure/signup/`: 회원가입
  - `heal_base_hospital_worker/v1/page/ensure/signup-form-submit/`: 회원가입 폼 작성 및 제출
  - `heal_base_hospital_worker/v1/page/ensure/signup-complete/`: 회원가입 완료 페이지
  - `heal_base_hospital_worker/v1/page/ensure/logined/and/hospital-location-guided/{실}`: 실별위치튜토리얼 + 광고

---

## 🎯 **Event 기반 시스템 설계 규칙**

### **Event 시스템 아키텍처**
- **Observer Pattern + Event Queue 하이브리드**: 즉시 반응과 비동기 처리를 모두 지원
- **State Machine 기반**: 명확한 상태 관리와 전환 로직
- **Event Handler 분리**: 각 기능별로 독립적인 핸들러 구현

### **Event 시스템 구조**
- **핵심 클래스**: `pk_internal_tools/pk_objects/pk_system_event.py`에 기본 Event 시스템 클래스들 배치
- **실행 스크립트**: `pk_internal_tools/pk_functions/`에 Event 기반 실행 스크립트 배치 (functions_split 대신)

### **Event 타입 정의**
- **기본 이벤트**: `STATE_CHANGED`, `VIDEO_LOADED`, `EXPORT_STARTED`, `EXPORT_COMPLETED`
- **LosslessCut 이벤트**: `LOSSLESSCUT_CLOSED`, `LOSSLESSCUT_RESTARTED`
- **클립보드 이벤트**: `CLIPBOARD_CHANGED`, `WINDOW_STATE_CHANGED`
- **파일 이벤트**: `FILE_SELECTED`, `VIDEO_PLAY_STARTED`, `VIDEO_PLAY_COMPLETED`

### **Event Handler 설계 원칙**
- **단일 책임**: 각 핸들러는 하나의 주요 기능만 수행
- **이벤트 기반**: 모든 동작은 Event 발생으로 시작
- **상태 동기화**: State Machine과 Event Handler 간 상태 일관성 유지
- **오류 처리**: 각 핸들러에서 발생하는 오류를 적절히 처리하고 로깅

### **State Machine 설계**
- **상태 정의**: `UNKNOWN`, `IDLE`, `FILE_LOADED`, `EXPORTING`, `EXPORT_COMPLETED`
- **상태 전환**: 명확한 전환 조건과 핸들러 등록
- **상태 히스토리**: 최근 100개 상태 변경 기록 유지
- **상태 검증**: 상태 변경 시 유효성 검사 및 로깅

### **Observer Pattern 구현**
- **상태 변경 감지**: State Machine의 상태 변경을 즉시 감지
- **이벤트 발생**: 상태 변경 시 적절한 Event 자동 발생
- **Observer 등록/해제**: 동적으로 Observer 추가/제거 가능
- **이벤트 알림**: 모든 Observer에게 이벤트 전파

### **Event Queue 관리**
- **큐 크기 제한**: 기본 1000개 이벤트로 메모리 사용량 제한
- **이벤트 처리**: 최대 10개씩 배치 처리로 성능 최적화
- **통계 수집**: 처리된 이벤트 수, 드롭된 이벤트 수, 핸들러 오류 수 추적
- **오류 복구**: 이벤트 처리 실패 시 적절한 오류 처리 및 로깅

### **성능 최적화**
- **체크 간격 조절**: LosslessCut 모니터링은 0.5초, 클립보드는 0.1초 간격
- **배치 처리**: 이벤트를 모아서 일괄 처리로 CPU 사용량 최소화
- **메모리 관리**: 상태 히스토리 제한, 이벤트 큐 크기 제한
- **스레드 안전**: Lock을 사용한 동시성 제어

### **클립보드 안전성**
- **안전 모드**: 클립보드 변경 감지 시 자동 보호 모드 활성화
- **윈도우 상태 모니터링**: 윈도우 변경 시 클립보드 보호
- **주기적 검사**: 정기적인 클립보드 안전성 검사
- **오류 복구**: 클립보드 오류 발생 시 자동 복구 시도

### **확장성 고려**
- **새로운 이벤트 타입**: `EventType` Enum에 새로운 타입 쉽게 추가
- **새로운 핸들러**: `EventHandler` 상속으로 새로운 기능 쉽게 구현
- **새로운 상태**: `StateMachine` 상속으로 새로운 상태 머신 구현
- **설정 변경**: 런타임에 핸들러 활성화/비활성화 가능

---

**규칙 위반 시 자동으로 수정 제안 및 실행을 진행합니다! 🚀**

---

## 📝 메모 DB 관리 정책

### **메모 마이그레이션 규칙**
- **중복 제거**: 마이그레이션 후 내용 및 제목 중복 자동 감지 및 제거

### **메모 DB 구조 규칙**
- **테이블 구조**: `pk_memos` 테이블에 메모 저장 (id, title, content, tags, category, created_at, updated_at)
- **FTS 지원**: `pk_memos_fts*` 테이블로 전문 검색 지원
- **태그 시스템**: `#태그` 형태의 메타데이터 자동 추출 및 저장
- **카테고리 분류**: 메모 자동 분류 체계 구축

### **중복 제거 정책**
- **내용 중복**: 해시 기반 정규화 후 중복 내용 자동 제거 (더 오래된 메모 우선 제거)
- **제목 중복**: 동일 제목 메모 중 첫 번째만 유지하고 나머지 자동 제거
- **데이터 품질**: 중복 제거 후 DB 상태 자동 확인 및 보고

### **메모 샘플 출력 규칙**
- **랜덤 샘플링**: 실제 존재하는 메모 ID 기반으로 랜덤 3개 선택
- **상세 정보**: ID, 제목, 태그, 카테고리, 생성/수정일, 내용 길이, 내용 미리보기 출력
- **내용 제한**: 긴 내용은 최대 10줄까지만 표시하고 총 줄 수 안내

### **메모 DB 상태 모니터링**
- **정기 점검**: 메모 개수, DB 크기, 테이블 상태 자동 확인
- **백업 관리**: 정기적인 DB 백업 및 압축 자동화
- **성능 최적화**: FTS 인덱스 자동 생성 및 유지보수

### **메모 검색 및 관리**
- **키워드 검색**: 다중 키워드 동시 검색 지원
- **태그 기반 분류**: 태그별 메모 자동 분류 및 필터링
- **내용 편집**: 검색 결과 기반 메모 내용 편집 및 업데이트

### **데이터 무결성 보장**
- **트랜잭션 처리**: 중복 제거 시 트랜잭션 기반 안전한 데이터 처리
- **오류 복구**: 마이그레이션 실패 시 자동 롤백 및 복구
- **데이터 검증**: 마이그레이션 완료 후 데이터 품질 자동 검증

---

**메모 DB는 중복 없는 깨끗한 데이터로 유지되며, 효율적인 검색과 관리를 지원합니다! 📚✨**

---

## 🔧 **Python 코드 작성 규칙**

### **로깅 통일 규칙**
- **F_PK_LOG 사용**: 모든 로깅은 `F_PK_LOG` 파일로 통일하여 작성
- **로깅 위치**: `pk_internal_tools/pk_objects/pk_system_files.py`에 정의된 `F_PK_LOG` 경로 사용
- **로깅 초기화**: `ensure_pk_system_log_initialized()` 함수로 로깅 시스템 초기화
- ensure_pk_system_log_initialized(__file__) 이걸 호출하고 테스트하면 로깅이 될거
- **일관성 유지**: 프로젝트 전체에서 동일한 로그 파일 사용으로 로그 통합 관리
- **로그 레벨**: `logging.debug`, `logging.info`, `logging.warning`, `logging.error` 적절히 사용
- **print문 금지**: 모든 `print()` 문은 `logging.debug()` 로 대체하여 작성
- **디버그 출력**: 디버깅용 출력은 반드시 `logging.debug()` 사용하여 로그 파일에 기록

### **PEP 최신 규칙 준수**
- **PEP 최신 규칙 준수**: 프로젝트 규칙을 최우선으로 하며, 그 다음으로 PEP 8(스타일 가이드) 및 PEP 20(The Zen of Python)을 포함한 최신 PEP 가이드라인을 준수합니다. 모든 Python 코드는 가독성, 유지보수성, 일관성을 최우선으로 작성합니다.

### **Lazy Import 규칙**
- **최대한 lazy import 적용**: 모든 import 문을 가능한 한 lazy import로 작성
- **docstring 하단에 import 작성**: 함수의 docstring 바로 아래에 해당 함수에서 사용하는 모든 import 문을 모아서 작성
- **순환 import 방지**: 모듈 간 순환 import 문제를 lazy import로 해결
- **성능 최적화**: 필요한 시점에만 import하여 초기 로딩 시간 단축
- **에러 격리**: 한 모듈의 import 실패가 다른 모듈에 영향을 주지 않도록 격리

### **Lazy Import 작성 패턴**
```python
def ensure_example_function():
    """함수 설명"""
    # lazy import로 순환 import 문제 해결
    try:
        from assets.pk_system.pk_internal_tools.pk_objects.pk_system_directories import D_PROJECT, D_PK_SYSTEM_TESTS
    except ImportError:
        # fallback: 직접 경로 계산
        from pathlib import Path
        D_PROJECT = str(Path(__file__).resolve().parent.parent.parent)
        D_PK_SYSTEM_TESTS = str(Path(D_PROJECT) / "tests")
    
    # 함수 로직 시작
    test_target = Path(D_PK_SYSTEM_TESTS) / "test_file.py"
    # ... 나머지 로직
```

### **Lazy Import 적용 원칙**
- **함수 시작 부분**: 함수의 docstring 바로 아래에 필요한 모듈들을 먼저 import
- **사용 시점 import**: 실제로 사용하는 시점에 import (예: subprocess 사용 시점에 import)
- **fallback 제공**: import 실패 시 대안 방법 제공 (경로 직접 계산, 기본값 사용 등)
- **에러 처리**: try-except 블록으로 import 실패 시 적절한 처리

### **Lazy Import 장점**
- **순환 import 완전 방지**: 모듈이 실제로 사용될 때까지 import를 지연
- **에러 격리**: 한 모듈의 import 실패가 다른 모듈에 영향을 주지 않음
- **성능 최적화**: 필요한 시점에만 import하므로 초기 로딩 시간 단축
- **유연성**: import 실패 시에도 fallback으로 계속 실행 가능

### **f-string 스크립트/텍스트 파일 작성 규칙**
- **dedent 필수**: Python에서 f-string으로 모든 종류의 스크립트나 텍스트 파일 내용을 작성할 때는 반드시 `textwrap.dedent()` 사용
- **가독성 향상**: 들여쓰기된 Python 코드에서 올바른 스크립트/텍스트 형식 생성
- **오류 방지**: 스크립트 실행 시 들여쓰기로 인한 오류 방지
- **일관성 유지**: Python 코드와 생성되는 파일 내용 모두 가독성 높게 작성

### **주석 작성 규칙**
- **중복 주석 금지**: 함수명과 주석이 동등한 수준의 정보를 제공하는 경우 주석 작성 금지
- **함수명 자체가 설명**: 함수명이 이미 충분히 명확한 경우 추가 주석 불필요
- **중복 정보 제거**: 함수명과 동일한 의미의 주석은 중복으로 간주하여 제거
- **가독성 향상**: 불필요한 주석 제거로 코드 가독성 향상
- **유지보수성**: 중복 주석 제거로 코드 유지보수성 향상

### **주석 작성 예시**
```python
# ❌ 잘못된 예시 (중복)
def ensure_user_logged_in():
    """사용자 로그인 확인 함수"""  # 함수명과 동일한 의미
    # ... 함수 로직

# ✅ 올바른 예시 (중복 없음)
def ensure_user_logged_in():
    # ... 함수 로직

# ✅ 올바른 예시 (추가 정보 제공)
def ensure_user_logged_in():
    """사용자 로그인 상태를 확인하고, 로그인되지 않은 경우 로그인 페이지로 리다이렉트"""
    # ... 함수 로직
```

### **함수 파일 작성 규칙**
- **`if __name__ == '__main__'` 금지**: `pk_internal_tools/pk_functions/` 디렉토리에 생성되는 개별 함수 파일에는 `if __name__ == '__main__':` 블록을 작성하지 않습니다. 함수는 다른 모듈에서 호출하여 사용하는 것을 전제로 합니다.

### **예외 처리 규칙**
- **`try...except` 구조**: 모든 주요 로직은 `try...except` 블록으로 감싸 예외 발생에 대비합니다.
- **예외 로깅**: 예외 발생 시, `except Exception:` 블록 내에서 `ensure_debug_loged_verbose(traceback)` 함수를 호출하여 오류 정보를 상세히 로깅합니다.
- **래퍼 스크립트 예외 처리**: 최상위 래퍼 스크립트에서는 `ensure_exception_routine_done`을 사용하여 예외를 처리할 수 있습니다.
- **세분화된 예외 처리**: `FileNotFoundError`나 `TypeError`처럼 특정 예외를 예상할 수 있는 경우, `except SpecificError as e:` 형태로 명시적으로 처리할 수 있습니다. 하지만 일반적인 오류 포착을 위해 포괄적인 `except Exception:` 블록과 `ensure_debug_loged_verbose` 사용을 권장합니다.

### 변수명 규칙 (Variable Naming Rules)
- **경로 변수명 규칙**:
  - 디렉토리 경로를 나타내는 변수는 `D_` 접두사와 `_PATH` 접미사를 함께 사용합니다 (예: `D_PROJECT_ROOT_PATH`).
  - 파일 경로를 나타내는 변수는 `F_` 접두사와 `_PATH` 접미사를 함께 사용합니다 (예: `F_LOG_FILE_PATH`).



### **사용자 입력 처리 규칙**
- **표준 함수 사용**: 사용자로부터 대화형 입력을 받을 때는 `input()` 함수 대신 `ensure_value_completed_2025_10_13_0000` (또는 유사한 `ensure_value~` 패턴의 함수)를 사용합니다.
- **목적**: 이 함수들은 `fzf` 통합, 히스토리 관리, 옵션 제공 등 고급 사용자 경험을 제공하며, 프로젝트의 표준화된 입력 방식을 따릅니다.
- **활용**: `key_name`, `func_n`, `guide_text`, `options` 인자를 활용하여 입력의 목적과 가이드를 명확히 제공합니다。

### **dedent 사용 예시**
```python
import textwrap

# 올바른 방법 (dedent 사용)
script_content = textwrap.dedent(f"""
            #!/bin/bash
            echo \"Hello World\"
            python {script_path}
        """)

# 잘못된 방법 (dedent 미사용)
script_content = f"#!/bin/bash
echo \"Hello World\"
python {script_path}
"
```

### **dedent 사용 시 들여쓰기 규칙**
- **Python 코드 내 들여쓰기**: f-string 내부의 모든 줄은 Python 코드의 현재 들여쓰기 레벨에 맞춰 들여쓰기
- **일관된 들여쓰기**: f-string 내부의 모든 줄은 동일한 들여쓰기 레벨 유지
- **가독성 우선**: Python 코드의 가독성을 위해 적절한 들여쓰기 사용
- **자동 정렬**: `textwrap.dedent()`가 Python 코드의 들여쓰기를 자동으로 제거하여 올바른 스크립트 형식 생성

### **스크립트/텍스트 파일 생성 시 규칙**
- **Python 들여쓰기**: Python 코드의 들여쓰기 레벨에 관계없이 생성되는 파일 내용은 올바른 형식으로 생성
- **가독성 유지**: Python 코드와 생성되는 파일 내용 모두 가독성 높게 작성
- **크로스 플랫폼**: Windows, Linux, macOS 환경 모두에서 올바르게 동작

### **적용 대상**
- **Windows 스크립트**: `.bat`, `.cmd`, `.ps1` 파일 생성
- **Linux/Unix 스크립트**: `.sh`, `.bash`, `.zsh` 파일 생성
- **설정 파일**: `.conf`, `.ini`, `.yaml`, `.json` 파일 생성
- **템플릿 파일**: HTML, CSS, JavaScript, SQL 등 모든 텍스트 기반 파일
- **문서 파일**: `.md`, `.txt`, `.rst` 등 마크다운 및 텍스트 파일
- **기타 스크립트**: 실행 가능한 모든 텍스트 기반 스크립트 및 설정 파일
- **스크립트 파일 임베딩**: `.cmd`, `.sh`, `.ps1`, `.bat` 등 외부 스크립트 파일의 내용은 별도 파일로 생성하는 대신, `textwrap.dedent()`를 사용하여 파이썬 코드 내부에 f-string으로 임베딩하고, `ensure_embeded_script_created` 및 `ensure_command_executed_to_os_like_human`과 같은 함수를 통해 실행합니다.

---

**f-string으로 모든 종류의 스크립트나 텍스트 파일 내용을 작성할 때는 반드시 `textwrap.dedent()`를 사용하여 올바른 형식으로 생성합니다! 🔧✨**

---

## 🚀 **함수 작성 성능 최적화 규칙**

### **성능 우선순위**
- **1순위: 성능(Performance)**: 실행 속도, 메모리 사용량, CPU 효율성 최적화
- **2순위: 재활용성(Reusability)**: 코드 재사용, 모듈화, 확장성
- **3순위: 가독성(Readability)**: 코드 이해, 유지보수성

### **성능 최적화 원칙**
- **알고리즘 최적화**: 시간복잡도 O(n²) → O(n log n) → O(n) 순으로 최적화
- **메모리 효율성**: 불필요한 객체 생성 최소화, 제너레이터 패턴 활용
- **지연 평가(Lazy Evaluation)**: 필요할 때만 계산, 메모리 절약
- **캐싱 전략**: 반복 계산 결과 캐싱, LRU 캐시 활용
- **배치 처리**: 개별 처리보다 일괄 처리로 I/O 최소화

### **성능 최적화 기법**
```python
# ❌ 비효율적 (매번 계산)
def process_items(items):
    for item in items:
        result = expensive_calculation(item)  # 매번 계산
        process(result)

# ✅ 효율적 (캐싱 활용)
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_calculation(item):
    return complex_math(item)

def process_items(items):
    for item in items:
        result = expensive_calculation(item)  # 캐시된 결과 사용
        process(result)
```

### **재활용성 설계 원칙**
- **단일 책임 원칙**: 하나의 함수는 하나의 명확한 기능만 수행
- **의존성 주입**: 외부 의존성을 파라미터로 받아 유연성 확보
- **인터페이스 분리**: 클라이언트가 사용하지 않는 메서드에 의존하지 않음
- **확장에 열려있고 수정에 닫혀있음**: Open-Closed Principle 준수

### **재활용성 구현 패턴**
```python
# ❌ 하드코딩 (재사용 불가)
def process_images_in_downloads():
    downloads_path = "C:/Users/username/Downloads"
    # ... 하드코딩된 로직

# ✅ 파라미터화 (재사용 가능)
def process_images_in_directory(directory_path, allowed_extensions=None):
    """지정된 디렉토리의 이미지 파일을 처리"""
    if allowed_extensions is None:
        from assets.pk_system.pk_internal_tools.pk_objects.pk_file_extensions import IMAGE_EXTENSIONS
        allowed_extensions = IMAGE_EXTENSIONS
    
    # ... 유연한 로직
```

### **성능 vs 재활용성 균형**
- **핵심 로직**: 성능 최적화 우선 (알고리즘, 데이터 구조)
- **인터페이스**: 재활용성 우선 (파라미터, 설정, 확장점)
- **설정 옵션**: 성능에 영향 없는 범위에서 재활용성 확보
- **기본값**: 성능 최적화된 기본값 제공, 필요시 커스터마이징 가능

### **성능 측정 및 모니터링**
- **프로파일링**: cProfile, line_profiler로 병목 지점 식별
- **메모리 사용량**: memory_profiler로 메모리 사용량 추적
- **벤치마크**: timeit, pytest-benchmark로 성능 측정
- **실시간 모니터링**: 실행 시간, 메모리 사용량 실시간 추적

### **성능 최적화 체크리스트**
- [ ] 알고리즘 시간복잡도 최적화
- [ ] 불필요한 객체 생성 제거
- [ ] 캐싱 전략 적용
- [ ] 배치 처리 구현
- [ ] 지연 평가 활용
- [ ] 메모리 효율성 검토
- [ ] I/O 최소화
- [ ] 병렬 처리 고려

### **재활용성 체크리스트**
- [ ] 단일 책임 원칙 준수
- [ ] 파라미터화 완료
- [ ] 의존성 주입 구현
- [ ] 인터페이스 분리
- [ ] 확장점 제공
- [ ] 설정 가능한 기본값
- [ ] 에러 처리 격리
- [ ] 문서화 완료

### **성능 최적화 예시**
```python
# 고성능 + 재사용 가능한 함수 설계
def ensure_target_files_classified_by_ngram(
    d_working, 
    token_splitter_pattern, 
    min_support, 
    max_n, 
    f_to_organize_list, 
    allowed_extension_tuple=None,
    batch_size=1000,  # 성능 튜닝 옵션
    enable_cache=True  # 캐싱 옵션
):
    """ngram 기반 파일 분류 및 정리 (고성능 + 재사용 가능)"""
    
    # 성능 최적화: 배치 처리
    if batch_size > 1:
        return _process_in_batches(
            f_to_organize_list, 
            batch_size, 
            d_working, 
            token_splitter_pattern, 
            min_support, 
            max_n, 
            allowed_extension_tuple,
            enable_cache
        )
    
    # 단일 배치 처리
    return _process_single_batch(
        f_to_organize_list,
        d_working,
        token_splitter_pattern,
        min_support,
        max_n,
        allowed_extension_tuple,
        enable_cache
    )
```

---

**모든 함수는 성능을 1순위로, 재활용성을 2순위로 하여 작성합니다! 🚀⚡**

---

### **디렉토리 구조 및 명명 규칙**

### **핵심 디렉토리 구조**
- **`pk_system_resources/`**: 정적 파일 및 외부 소스 리소스 디렉토리입니다.
- **`pk_internal_tools/`**: 파이썬 소스 코드의 최상위 루트 디렉토리입니다.
- **`pk_internal_tools/pk_objects/`**: 시스템 객체, 클래스, 상태 관리 등 공유 객체를 저장합니다.
- **`pk_internal_tools/pk_functions/`**: 프로젝트의 핵심 기능 함수들을 저장합니다.
- **`pk_system_tests/`**: 테스트 코드를 저장하며, 파일명에 `test_` 접두사를 사용합니다.

### **명명 규칙 원칙**
- **`pk_system_resources/`**: 역사적인 이유로 사용되는 핵심 소스 디렉토리입니다.
- **`pk_system_*`**: `pk_system_resources` 하위에서 시스템 레벨의 공유 기능을 담당하는 디렉토리는 `pk_` 접두사를 사용하여 명확히 구분합니다.
- **`pkg_*` 접두사 사용 지양**: `pk_system_resources` 외에 새로운 디렉토리를 생성할 때는 `pkg_` 접두사 사용을 지양하고, 기능에 맞는 명확한 이름을 부여합니다.

### **디렉토리명 패턴**
- **`pk_`**: 프로젝트 접두사 (pk_system)
- **`system_`**: 시스템 레벨 구분
- **`pk_objects/`**: 객체, 클래스, 상태 관리
- **`pk_system_wrappers/`**: 실행 래퍼, CLI 인터페이스
- **`pk_functions/`**: 핵심 함수들

### **디렉토리 구조 정리 규칙**
- **중복 디렉토리 감지**: `pkg_`와 `pk_` 접두사가 혼재된 디렉토리 자동 감지
- **자동 정리**: 잘못된 `pkg_` 접두사 디렉토리를 올바른 `pk_` 접두사로 자동 변경
- **파일 이동**: 잘못된 디렉토리의 파일들을 올바른 디렉토리로 자동 이동
- **중복 제거**: 빈 디렉토리 자동 정리

### **적용 대상**
- **새 디렉토리 생성**: 항상 `pk_` 접두사 사용
- **기존 디렉토리 정리**: `pkg_` 접두사 디렉토리를 `pk_` 접두사로 변경
- **import 경로 수정**: 모든 import 문에서 올바른 디렉토리 경로 사용
- **파일 참조 수정**: 모든 파일 참조에서 올바른 디렉토리 경로 사용

### **디렉토리 정리 체크리스트**
- [ ] `pkg_` 접두사 디렉토리 감지
- [ ] `pk_` 접두사로 디렉토리명 변경
- [ ] 파일들을 올바른 디렉토리로 이동
- [ ] import 경로 수정
- [ ] 파일 참조 경로 수정
- [ ] 빈 디렉토리 정리
- [ ] 중복 디렉토리 제거

## 📝 **커뮤니케이션 및 언어 규칙**

### **한글 답변 의무화**
- **항상 한글로 답변**: 모든 응답은 반드시 한국어로 작성해야 합니다
- **언어 일관성**: 프로젝트 내 모든 커뮤니케이션은 한국어로 통일
- **코드 주석**: 코드 내 주석도 한국어로 작성하는 것을 권장
- **문서화**: 일반 문서는 한국어로 작성 (단, 기술문서는 예외)

### **기술문서 영문 작성 규칙**
- **기술문서는 영문 작성**: README.md, API 문서, 아키텍처 문서 등 모든 기술문서는 영어로 작성해야 합니다
- **국제 표준 준수**: 오픈소스 프로젝트 표준에 맞춰 영문으로 작성하여 국제적 접근성 확보
- **영문 작성 대상**:
  - `README.md`: 프로젝트 소개 및 사용법
  - API 문서: 함수/클래스 문서화
  - 아키텍처 문서: 시스템 설계 문서
  - 설치 가이드: 설치 및 설정 방법
  - 기여 가이드: 기여 방법 안내
- **한글 작성 대상** (예외):
  - `GEMINI.md`: Cursor AI 규칙 문서 (한글 유지)
  - 코드 주석: 개발자 간 소통용 (한글 권장)
  - 커밋 메시지: 팀 내 소통용 (한글 가능)

### **한글 답변 적용 대상**
- **일반 질문 응답**: 사용자의 모든 질문에 한국어로 답변
- **코드 설명**: 코드 작성 시 한국어로 설명
- **에러 메시지**: 오류 발생 시 한국어로 안내
- **진행 상황 보고**: 작업 진행 상황을 한국어로 보고

### **언어 품질 기준**
- **명확성**: 한국어 표현이 명확하고 이해하기 쉬어야 함
- **정확성**: 기술 용어는 정확하게 사용
- **일관성**: 용어 사용이 프로젝트 전체에서 일관되어야 함
- **가독성**: 문장 구조가 자연스럽고 읽기 편해야 함

---

**기술문서는 영문으로, 커뮤니케이션은 한국어로 진행하여 국제적 접근성과 팀 내 소통을 모두 확보합니다! 🌍📝**

---

**모든 디렉토리는 `pk_` 접두사를 사용하여 일관성 있게 명명합니다! 📁✨**