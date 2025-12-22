import os
import sys
from pathlib import Path


def ensure_simple_path_setup():
    """
    의존성 문제 없이 간단하게 PATH를 설정합니다.
    """
    try:
        print("[설정] 간단한 PATH 설정 시작...")
        
        # 현재 작업 디렉토리를 기준으로 프로젝트 루트 찾기
        current_dir = Path.cwd()
        project_root = current_dir
        
        # 추가할 경로들
        paths_to_add = [
            str(project_root / "pk_os_layer_resources"),  # UV/FZF 경로
            str(project_root / ".venv" / "Scripts"),  # Windows virtual environment Scripts
            str(project_root / "pk_external_tools"),  # PK_PY 경로
        ]
        
        print(f"[프로젝트] 루트 디렉토리: {project_root}")
        
        # 현재 PATH 가져오기
        current_path = os.environ.get('PATH', '')
        current_paths = current_path.split(os.pathsep) if current_path else []
        
        print(f"[현재] PATH 개수: {len(current_paths)}")
        
        # 새로 추가할 경로들 (존재하지 않는 것만)
        new_paths = []
        for path_to_add in paths_to_add:
            path_obj = Path(path_to_add)
            if path_obj.exists():
                if str(path_obj) not in current_paths:
                    new_paths.append(str(path_obj))
                    print(f"[추가] {path_to_add}")
                else:
                    print(f"[ℹ️정보] 이미 PATH에 존재: {path_to_add}")
            else:
                print(f"[️경고] 경로가 존재하지 않음: {path_to_add}")
        
        if new_paths:
            # 새 PATH 구성
            updated_paths = current_paths + new_paths
            new_path_str = os.pathsep.join(updated_paths)
            
            # 현재 세션의 환경변수 업데이트
            os.environ['PATH'] = new_path_str
            
            print(f"[성공] PATH에 {len(new_paths)}개 경로 추가됨")
            
            # Windows 환경에서는 setx 명령어 사용 (관리자 권한 필요할 수 있음)
            if os.name == 'nt':  # Windows
                try:
                    os.system(f'setx PATH "{new_path_str}"')
                    print("[성공] Windows 영구 PATH 설정 완료")
                except Exception as e:
                    print(f"⚠️ 영구 PATH 설정 실패 (현재 세션에는 적용됨): {e}")
        else:
            print("[ℹ️정보] 추가할 새로운 PATH가 없습니다.")
        
        # 현재 PATH 출력 (처음 10개만)
        print("[현재] PATH 설정 (처음 10개):")
        current_paths = os.environ.get('PATH', '').split(os.pathsep)
        for i, path in enumerate(current_paths[:10]):
            if path:
                print(f"  {i+1:2d}. {path}")
        
        if len(current_paths) > 10:
            print(f"  ... 그리고 {len(current_paths) - 10}개 더")
        
        return True
        
    except Exception as e:
        print(f"[오류] PATH 설정 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    ensure_simple_path_setup()
