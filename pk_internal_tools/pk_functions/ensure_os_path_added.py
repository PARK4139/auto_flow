import os
import inspect
import subprocess
from pathlib import Path


def ensure_os_path_added():
    """
    의존성 문제 없이 안전하게 PATH를 설정합니다.
    """
    # 안전장치: os 모듈이 없으면 자동으로 import
    try:
        if 'os' not in globals():
            import os
            print("[안전장치] os 모듈을 자동으로 import했습니다.")
    except Exception as e:
        print(f"[오류] os 모듈 import 실패: {e}")
        return False
    
    try:
        print("[설정] PATH 설정 시작...")
        
        # pk_system 루트 디렉토리 찾기 (현재 디렉토리가 pk_external_tools인 경우 상위로 이동)
        current_dir = Path.cwd()
        if current_dir.name == "pk_external_tools":
            project_root = current_dir.parent
            print(f"[정보] pk_external_tools 디렉토리에서 실행 중, 상위 디렉토리로 이동: {project_root}")
        else:
            project_root = current_dir
            print(f"[정보] 현재 디렉토리에서 실행 중: {project_root}")
        
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
        
        # 기존 PATH에서 중복 제거 및 정규화
        normalized_current_paths = []
        seen_paths = set()
        
        for path in current_paths:
            if path.strip():  # 빈 문자열 제거
                try:
                    # 절대 경로로 정규화하여 중복 감지 정확도 향상
                    normalized_path = str(Path(path).resolve())
                    if normalized_path not in seen_paths:
                        normalized_current_paths.append(path)  # 원본 경로 유지
                        seen_paths.add(normalized_path)
                    else:
                        print(f"[정리] 중복 PATH 제거: {path}")
                except Exception as e:
                    # 경로 정규화 실패 시 원본 경로 사용
                    if path not in seen_paths:
                        normalized_current_paths.append(path)
                        seen_paths.add(path)
        
        print(f"[정리] 중복 제거 후 PATH 개수: {len(normalized_current_paths)}")
        
        # 새로 추가할 경로들 (존재하지 않는 것만)
        new_paths = []
        for path_to_add in paths_to_add:
            path_obj = Path(path_to_add)
            if path_obj.exists():
                try:
                    normalized_path = str(path_obj.resolve())
                    if normalized_path not in seen_paths:
                        new_paths.append(str(path_obj))
                        seen_paths.add(normalized_path)
                        print(f"[추가] {path_to_add}")
                    else:
                        print(f"[ℹ️정보] 이미 PATH에 존재: {path_to_add}")
                except Exception as e:
                    # 정규화 실패 시 원본 경로로 체크
                    if str(path_obj) not in normalized_current_paths:
                        new_paths.append(str(path_obj))
                        print(f"[추가] {path_to_add}")
                    else:
                        print(f"[ℹ️정보] 이미 PATH에 존재: {path_to_add}")
            else:
                print(f"[️경고] 경로가 존재하지 않음: {path_to_add}")
        
        if new_paths:
            # 새 PATH 구성 (정리된 기존 PATH + 새 경로)
            updated_paths = normalized_current_paths + new_paths
            new_path_str = os.pathsep.join(updated_paths)
            
            print(f"[통계] 최종 PATH: 기존 {len(normalized_current_paths)}개 + 새로 추가 {len(new_paths)}개 = 총 {len(updated_paths)}개")
            
            # 현재 세션의 환경변수 업데이트
            os.environ['PATH'] = new_path_str
            
            print(f"[성공] PATH에 {len(new_paths)}개 경로 추가됨")
            
            # Windows 환경에서는 setx 명령어 사용 (더 안전한 방법)
            if os.name == 'nt':  # Windows
                try:
                    # PATH가 너무 길면 setx가 실패할 수 있으므로 확인
                    if len(new_path_str) > 1024:
                        print("⚠️ PATH가 너무 깁니다. 영구 설정을 건너뜁니다.")
                        print("[ℹ️정보] 현재 세션에는 PATH가 적용되었습니다.")
                    else:
                        # subprocess를 사용하여 더 안전하게 실행
                        result = subprocess.run(
                            ['setx', 'PATH', new_path_str],
                            capture_output=True,
                            text=True,
                            shell=True
                        )
                        if result.returncode == 0:
                            print("[성공] Windows 영구 PATH 설정 완료")
                        else:
                            print(f"⚠️ 영구 PATH 설정 실패: {result.stderr}")
                            print("[ℹ️정보] 현재 세션에는 PATH가 적용되었습니다.")
                except Exception as e:
                    print(f"⚠️ 영구 PATH 설정 실패 (현재 세션에는 적용됨): {e}")
            else:  # Linux/WSL
                print("[성공] Linux/WSL PATH 설정 완료 (현재 세션)")
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