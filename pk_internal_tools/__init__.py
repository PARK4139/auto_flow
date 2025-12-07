"""
pk_system 패키지 (pk_internal_tools 디렉토리)

외부 레포에서 import pk_system 또는 from pk_internal_tools.pk_functions.xxx import yyy 형태로 사용하기 위한 패키지입니다.

이 파일은 package-dir 설정에 의해 pk_system 패키지의 __init__.py로 매핑됩니다.
실제 디렉토리는 pk_internal_tools/ 이지만, 패키지 이름은 pk_system입니다.
"""

__version__ = "0.0.0"  # setuptools-scm에 의해 자동으로 업데이트됨

# 패키지 메타데이터
__author__ = "junghoon.park"
__email__ = "park4139@google.com"



__all__ = [
    'pk_functions',
]