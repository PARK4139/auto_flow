from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_env_file_setup() -> Path:
    """
    pk_system 환경 파일 설정 및 경로 충돌 해결
    """
    import logging
    import os
    from dotenv import load_dotenv
    import traceback
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_pk_path_selected import ensure_pk_path_resolved
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    func_n = get_caller_name()
    try:
        # 1. 중복 경로 감지 및 해결
        try:

            # 중복 경로가 있으면 사용자 선택
            selected_path = ensure_pk_path_resolved(
                remove_from_sys_path=True,
                interactive=True  # 사용자 선택 활성화
            )

            if selected_path:
                # external_project_root
                # 선택된 경로를 환경변수로 설정
                # os.environ['PK_ROOT'] = str(selected_path)
                os.environ['PK_EXTERNAL_PROJECT_ROOT'] = str(selected_path)
                logging.info(f"pk_system 루트경로 선택됨: {selected_path}")
        except ImportError:
            # 순환 import 방지: ensure_pk_path_selected가 없으면 기본 동작
            pass
        except Exception as e:
            logging.debug(f"경로 선택 중 오류 (무시): {e}")

        # 2. .env 파일 경로 결정
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
        from pk_internal_tools.pk_functions.get_external_project_root_candidates import (
            get_external_project_root_candidates
        )

        # 2-1. 'PK_EXTERNAL_PROJECT_ROOT' 환경 변수 우선 확인
        selected_project_root = os.environ.get('PK_EXTERNAL_PROJECT_ROOT')

        if selected_project_root and Path(selected_project_root).exists():
            logging.info(f"환경 변수 'PK_EXTERNAL_PROJECT_ROOT'를 사용합니다: {selected_project_root}")
        else:
            # 2-2. 환경 변수가 없거나 유효하지 않으면, 기존 로직 (후보 탐색 및 사용자 선택) 수행
            logging.debug("'PK_EXTERNAL_PROJECT_ROOT' 환경 변수가 없어, 프로젝트 루트를 자동으로 탐색합니다.")
            external_project_candidates = get_external_project_root_candidates()

            if external_project_candidates:
                from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
                func_n = get_caller_name()

                if len(external_project_candidates) > 1:
                    # 후보가 여러 개일 경우 사용자에게 선택 요청
                    selected_project_root = ensure_value_completed_2025_11_11(
                        key_name="external_project_root",
                        func_n=func_n,
                        guide_text="사용할 외부 프로젝트 루트를 선택하세요:",
                        options=external_project_candidates
                    )
                else:
                    # 후보가 하나일 경우 바로 사용
                    selected_project_root = external_project_candidates[0]
            else:
                # 외부 프로젝트 후보를 찾을 수 없는 경우, pk_system 자체의 루트를 사용
                project_root_path = d_pk_root.parent
                selected_project_root = str(project_root_path)
                logging.debug(f'외부 프로젝트 후보를 찾을 수 없어, pk_system 자체 모드 경로를 사용합니다: {selected_project_root}')

        # 최종 결정된 외부 프로젝트 루트가 있으면 환경 변수에 설정하여 다른 곳에서도 조회 가능하도록 합니다.
        if selected_project_root:
            os.environ['PK_EXTERNAL_PROJECT_ROOT'] = str(selected_project_root)
            project_root = Path(selected_project_root)
            dotenv_path = project_root.parent / ".env"
            logging.debug(f'.env 파일 경로가 결정되었습니다: {dotenv_path}')
        else:
            # 어떤 방법으로도 프로젝트 루트를 결정할 수 없는 경우의 최종 폴백
            dotenv_path = d_pk_root.parent / ".env"
            logging.warning(f'프로젝트 루트를 결정할 수 없어, 기본 .env 경로를 사용합니다: {dotenv_path}')

        # 3. .env 파일 로드
        load_dotenv(dotenv_path=dotenv_path)
        logging.debug(f'env file is used ({dotenv_path})')
        return dotenv_path
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
