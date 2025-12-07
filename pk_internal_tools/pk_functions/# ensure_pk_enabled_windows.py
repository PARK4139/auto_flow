import logging
from pathlib import Path

try:
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
except ImportError as e:
    import platform

    logging.debug(f"모듈을 찾을 수 없음: {e}")
    logging.debug("Windows 환경에서 안전한 색상 코드 사용합니다")
    if platform.system().lower() == "windows":
        try:
            import colorama

            colorama.init(autoreset=True, convert=True)
            PK_ANSI_COLOR_MAP = {
                'GREEN': '\033[32m', 'RED': '\033[31m', 'YELLOW': '\033[33m',
                'BLUE': '\033[34m', 'MAGENTA': '\033[35m', 'CYAN': '\033[36m',
                'RESET': '\033[0m'
            }
        except (ImportError, Exception):
            # colorama 실패 시 색상 없이
            PK_ANSI_COLOR_MAP = {
                'GREEN': '', 'RED': '', 'YELLOW': '', 'BLUE': '',
                'MAGENTA': '', 'CYAN': '', 'RESET': ''
            }
    else:
        # Linux/Mac에서는 기본 ANSI 색상 코드
        PK_ANSI_COLOR_MAP = {
            'GREEN': '\033[32m', 'RED': '\033[31m', 'YELLOW': '\033[33m',
            'BLUE': '\033[34m', 'MAGENTA': '\033[35m', 'CYAN': '\033[36m',
            'RESET': '\033[0m'
        }
try:
    from pk_internal_tools.pk_objects.pk_urls import URL_FZF_API, URL_CHATGPT_PK_WORKING
except ImportError as e:
    import os

    logging.debug(f"모듈을 찾을 수 없음: {e}")
    logging.debug("기본 경로를 사용합니다.")

    # 기본 경로 설정 (USERPROFILE 동적 사용)

    userprofile = os.environ.get('USERPROFILE', os.path.expanduser('~'))

    d_pk_system = Path(userprofile) / "Downloads" / "pk_system"
    d_pk_external_tools = Path(userprofile) / "Downloads" / "pk_system" / "pk_external_tools"
    d_pk_external_tools = d_pk_external_tools  # 하위 호환성
    d_pk_external_tools = d_pk_external_tools  # 통합됨
    D_PK_HIDDEN = Path(userprofile) / "Downloads" / "pk_system" / ".pk_system"
    D_PK_WORKING = Path(userprofile) / "Downloads" / "pk_working"
    D_PK_MEMO = Path(userprofile) / "Downloads" / "pk_memo"
    D_BUSINESS_FLOW_REPO = Path(userprofile) / "Downloads" / "business_flow"
    D_DOWNLOADS = Path(userprofile) / "Downloads"

    # 기본 파일 경로
    F_UV = None
    F_FZF = None
    F_UV_ZIP = None
    F_FZF_ZIP = None
    F_VSCODE = None
    F_CURSOR = None
    F_CLAUDE = None
    F_PYCHARM = None

    # 기본 URL
    URL_FZF_API = "https://api.github.com/repos/junegunn/fzf/releases/latest"
    URL_CHATGPT_PK_WORKING = "https://chat.openai.com"

if platform.system().lower() == "windows":
    pass

print = None

PkTextsFallBack = type('PkTexts', (), {
    'VENV_PYTHON_TEST': 'virtual environment Python 테스트',
    'VENV_PYTHON_NOT_FOUND': 'virtual environment Python을 찾을 수 없음',
    'VENV_PYTHON_VERSION': 'virtual environment Python 버전',
    'VENV_MODULE_TEST': '모듈 사용 가능',
    'VENV_TEST_SUCCESS': '테스트 성공',
    'UV_INSTALLATION': 'UV 설치',
    'PERMISSION_ERROR': '권한 오류',
    'BACKUP_CREATED': '백업 생성됨',
    'BACKUP_FAILED': '백업 실패',
    'FILE_NOT_FOUND': '파일을 찾을 수 없음',
    'DIRECTORY_CREATED': '디렉토리 생성됨',
    'DIRECTORY_CREATION_FAILED': '디렉토리 생성 실패',
    'FILE_COPY_SUCCESS': '파일 복사 성공',
    'FILE_COPY_FAILED': '파일 복사 실패',
    'ALTERNATIVE_INSTALLATION': '대안 설치',
    'TEMP_CLEANUP_FAILED': '임시 파일 정리 실패',
    'INSTALLATION_SUCCESS': '설치 완료',
    'INSTALLATION_FAILED': '설치 실패',
    'PATH_SETUP': 'Windows PATH 설정',
    'ALIAS_SETUP': 'Windows 별칭 설정',
    'REGISTRY_SETUP_SUCCESS': '레지스트리 설정 완료',
    'REGISTRY_SETUP_FAILED': '레지스트리 설정 실패',
    'WINDOWS_REGISTRY_SETUP_SUCCESS': 'Windows 레지스트리 설정 완료',
    'WINDOWS_REGISTRY_SETUP_FAILED': 'Windows 레지스트리 설정 실패',
    'PACKAGE_SYNC': 'uv 패키지 동기화',
    'VENV_SETUP': 'virtual environment Python으로 패키지 설치',
    'VENV_PYTHON_FOUND': 'virtual environment Python 사용',
    'PACKAGE_INSTALLING': '설치 중',
    'PACKAGE_INSTALL_SUCCESS': '설치 완료',
    'PACKAGE_INSTALL_FAILED': '설치 실패',
    'PACKAGE_INSTALL_ERROR': '설치 오류',
    'VENV_PACKAGE_INSTALL_COMPLETE': 'virtual environment 패키지 설치 완료',
    'FZF_INSTALLATION': 'FZF 설치',
    'OPERATION_SUCCESS': '동기화 완료',
    'OPERATION_FAILED': '동기화 실패',
    'VENV_TEST_FAILED': '테스트 실패'
})()
# Lazy import to avoid circular dependency
try:
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    print = logging.debug
except ImportError:
    import builtins

    print = builtins.print
    PkTexts = PkTextsFallBack
