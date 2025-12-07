from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_script_file_created import ensure_script_file_created
from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

from pk_internal_tools.pk_objects.pk_files import F_QC_MODE_TOML


@ensure_seconds_measured
def ensure_pk_qc_mode_toml_setup() -> Optional[Path]:
    """
    pk_qc_mode.toml 파일 설정 및 자동 생성
    
    ensure_pk_env_file_setup()와 동등하게 독립적으로 동작합니다.
    
    차이점:
    - .env: 외부 프로젝트의 부모 경로에 사용/생성
    - pk_qc_mode.toml: 외부 프로젝트 루트의 .pk_system/ 디렉토리에 사용/생성
    
    동작:
    - 외부 프로젝트 루트를 찾을 수 있으면 자동으로 .pk_system/pk_qc_mode.toml 생성
    - 외부 프로젝트 루트를 찾을 수 없으면 현재 작업 디렉토리에 .pk_system/pk_qc_mode.toml 생성
    - 사용자 선택 없이 자동으로 생성 (안내 메시지 없음)
    - 파일이 이미 존재하면 그대로 사용
    
    Returns:
        Optional[Path]: pk_qc_mode.toml 파일 경로 (없으면 None, 기본값 False 사용)
    """
    import logging
    try:
        if Path(F_QC_MODE_TOML).exists():
            return F_QC_MODE_TOML
        else:
            # ensure_pnx_made(F_QC_MODE_TOML, mode='f')
            ensure_script_file_created(script_file= F_QC_MODE_TOML, script_content="LOCAL_TEST_ACTIVATE = 0\n")

    except Exception as e:
        logging.debug(f"ensure_pk_qc_mode_toml_setup 오류: {e}")
        return None
