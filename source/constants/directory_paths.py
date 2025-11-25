"""
프로젝트 내 주요 디렉토리들의 절대 경로를 정의합니다.

이 모듈은 다양한 환경에서 일관된 경로 참조를 제공하며,
Pathlib를 사용하여 크로스 플랫폼 호환성을 보장합니다.

Note: pk_system is now installed as a library via pip/uv.
To get pk_system paths, use:
    from pk_system.pk_sources.pk_objects.pk_system_directories import get_pk_system_root
"""
from pathlib import Path
import os

D_PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent.parent # 프로젝트의 최상위 루트 디렉토리
# D_PK_SYSTEM_PATH and D_pk_sources_PATH are deprecated.
# pk_system is now installed as a library. Use get_pk_system_root() from pk_system.pk_sources instead.

D_SOURCE_PATH =  Path(__file__).parent.parent # 현재 파일이 속한 'source' 디렉토리
D_FUNCTIONS_PATH = D_SOURCE_PATH / "functions" # 'source' 디렉토리 내 'functions' 디렉토리
D_WRAPPERS_PATH = D_SOURCE_PATH / "wrappers" # 'source' 디렉토리 내 'wrappers' 디렉토리
D_HUVITS_WRAPPERS_PATH = D_WRAPPERS_PATH / "Huvitz" # Huvitz 관련 래퍼 파일들이 위치한 디렉토리
D_JUNG_HOON_PARK_WRAPPERS_PATH = D_WRAPPERS_PATH / "Jung_Hoon_Park" # 박정훈 관련 래퍼 파일들이 위치한 디렉토리


# Define D_DOWNLOADS_PATH based on user's home directory
# 사용자의 다운로드 디렉토리를 정의합니다. 환경 변수를 우선 사용하고, 없을 경우 기본 홈 디렉토리를 사용합니다.
D_USER_PROFILE_PATH = os.environ.get('USERPROFILE')
if D_USER_PROFILE_PATH:
    D_DOWNLOADS_PATH = Path(D_USER_PROFILE_PATH) / 'Downloads'
else:
    # Fallback to a default, though this is unlikely to be correct
    D_DOWNLOADS_PATH = Path.home() / 'Downloads'
