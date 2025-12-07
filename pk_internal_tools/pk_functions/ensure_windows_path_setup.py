import logging
import os
from pathlib import Path

from pk_internal_tools.pk_objects.pk_directories import d_pk_root


def ensure_windows_path_setup():
    """
    Windows 환경에서 PK 시스템에 필요한 PATH들을 자동으로 설정합니다.
    """
    try:
        logging.debug("[설정] Windows PATH 설정 시작...")

        # 프로젝트 루트 디렉토리
        project_root = Path(d_pk_root)

        # 추가할 경로들
        paths_to_add = [
            str(project_root / "pk_os_layer_resources"),  # UV/FZF 경로
            str(project_root / ".venv" / "Scripts"),  # Windows virtual environment Scripts
            str(project_root / "pk_external_tools"),  # PK_PY 경로
        ]

        # 현재 PATH 가져오기
        current_path = os.environ.get('PATH', '')
        current_paths = current_path.split(os.pathsep) if current_path else []

        # 새로 추가할 경로들 (존재하지 않는 것만)
        new_paths = []
        for path_to_add in paths_to_add:
            path_obj = Path(path_to_add)
            if path_obj.exists() and str(path_obj) not in current_paths:
                new_paths.append(str(path_obj))
                logging.debug(f"[추가] {path_to_add}")
            elif not path_obj.exists():
                logging.debug(f"[️경고] 경로가 존재하지 않음: {path_to_add}")
            else:
                logging.debug(f"[ℹ️정보] 이미 PATH에 존재: {path_to_add}")

        if new_paths:
            # 새 PATH 구성
            updated_paths = current_paths + new_paths
            new_path_str = os.pathsep.join(updated_paths)

            # Windows 환경변수 업데이트 (현재 세션)
            os.environ['PATH'] = new_path_str

            # 영구적으로 설정하려면 setx 사용 (관리자 권한 필요할 수 있음)
            try:
                os.system(f'setx PATH "{new_path_str}"')
                logging.debug(f"[성공] Windows PATH에 {len(new_paths)}개 경로 추가됨")
            except Exception as e:
                logging.debug(f"⚠️ 영구 PATH 설정 실패 (현재 세션에는 적용됨): {e}")
        else:
            logging.debug("[ℹ️정보] 추가할 새로운 PATH가 없습니다.")

        # 현재 PATH 출력
        logging.debug("[현재] PATH 설정:")
        for i, path in enumerate(os.environ.get('PATH', '').split(os.pathsep)):
            if path:
                logging.debug(f"{i + 1:2d}. {path}")

        return True

    except Exception as e:
        logging.error("Windows PATH 설정 실패: {e}")
        return False


if __name__ == "__main__":
    ensure_windows_path_setup()
