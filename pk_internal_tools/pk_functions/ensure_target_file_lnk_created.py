import logging
import os
import sys
import traceback
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_files import F_ENSURE_pk_ENABLED_CMD, F_PK_LAUNCHER_LNK

# ensure_taskbar_pinned_removed는 Windows 전용이므로 지연 import


@ensure_seconds_measured
def ensure_target_file_lnk_created(
    target_file: Optional[Path] = None,
    shortcut_path: Optional[Path] = None,
    working_directory: Optional[Path] = None
) -> None:
    """
    바로가기 생성 함수 - 작업표시줄 제거 기능 포함
    
    Args:
        target_file: 바로가기가 가리킬 대상 파일 (Path 객체). 미지정 시 F_ENSURE_pk_ENABLED_CMD 사용.
        shortcut_path: 생성될 바로가기 파일의 경로 (Path 객체). 미지정 시 F_PK_LAUNCHER_LNK 사용.
        working_directory: 바로가기의 '시작 위치' (Path 객체). 미지정 시 D_PK_ROOT 사용.
    
    에러 발생 시:
    - 상세한 traceback을 콘솔에 출력
    - 에러 로그를 파일로 저장
    - 사용자 입력 대기 (콘솔이 바로 닫히지 않도록)
    """
    
    try:
        # 인자 기본값 설정
        target_file = target_file
        shortcut_path = shortcut_path
        working_directory = working_directory

        # Windows 전용 함수 지연 import
        try:
            from pk_internal_tools.pk_functions.ensure_taskbar_pinned_removed import ensure_taskbar_pinned_removed
        except ImportError:
            ensure_taskbar_pinned_removed = None
        
        # 기존 작업표시줄 고정 제거 (선택 사항)
        if ensure_taskbar_pinned_removed:
            logging.info("____________________________________________")
            logging.info(f"# 작업표시줄에서 기존 {get_nx(shortcut_path)} 제거")
            if ensure_taskbar_pinned_removed(get_nx(shortcut_path)):
                logging.info("작업표시줄 제거 완료")
            else:
                logging.warning("⚠️ 작업표시줄 제거 실패 (계속 진행)")
        
        # 잠시 대기 (작업표시줄 변경사항 반영)
        import time
        time.sleep(1)
        
        try:
            import win32com.client

            # target_file이 존재하는지 확인
            if not target_file.exists():
                logging.warning(f"경고: 대상 파일 '{target_file}'이(가) 존재하지 않습니다. 바로가기 생성을 건너뜁니다.")
                return

            shell = win32com.client.Dispatch("WScript.Shell")

            logging.info("____________________________________________")
            logging.info("# 바로가기 생성")
            shortcut_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 기존 바로가기 파일이 있다면 삭제
            if shortcut_path.exists():
                try:
                    shortcut_path.unlink()
                    logging.info(f"기존 바로가기 파일 삭제 완료: {shortcut_path}")
                except Exception as e:
                    logging.warning(f"⚠️ 기존 바로가기 파일 삭제 실패: {e} (계속 진행)")
            
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_file)
            
            # WorkingDirectory 설정
            # WorkingDirectory는 항상 절대 경로여야 함
            if not working_directory.is_absolute():
                logging.warning(f"경고: 'working_directory'({working_directory})가 절대 경로가 아닙니다. 절대 경로로 변환합니다.")
                working_directory = working_directory.resolve()
            
            # WorkingDirectory가 존재하는지 확인
            if not working_directory.exists() or not working_directory.is_dir():
                logging.warning(f"경고: 'working_directory'({working_directory})가 존재하지 않거나 디렉토리가 아닙니다. 바로가기 생성에 문제가 발생할 수 있습니다.")
            
            shortcut.WorkingDirectory = str(working_directory)
            shortcut.save()
            
            logging.info(f"바로가기 생성 완료: {shortcut_path}")
            logging.info(f"대상: {target_file}")
            logging.info(f"작업 디렉토리: {working_directory}")
            logging.info(f"작업 디렉토리 존재 여부: {working_directory.exists()}")

            # 3작업 디렉토리 바로가기 생성 (현재는 스킵)
            # 4작업표시줄 고정 안내
            logging.info("____________________________________________")
            logging.info("# 작업표시줄 고정 안내")
            logging.info("작업표시줄에 고정하려면:")
            logging.info(f"1. 생성된 바로가기('{shortcut_path}') 우클릭 → '작업 표시줄에 고정'")
            logging.info("2. 또는 바로가기를 작업표시줄로 드래그")
            logging.info("3. 고정 후 Win + 1 단축키로 빠른 실행 가능")
        
        except ImportError as e:
            logging.error(f"____________________________________________")
            logging.error(f"# win32com.client 모듈을 가져올 수 없습니다")
            logging.error(f"오류: {e}")
            logging.error("바로가기 생성은 선택사항이므로 계속 진행합니다.")
        except Exception as e:
            logging.error(f"____________________________________________")
            logging.error(f"# 바로가기 생성 실패")
            logging.error(f"오류: {e}")
            logging.error("바로가기 생성은 선택사항이므로 계속 진행합니다.")
    
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        ensure_debugged_verbose(traceback, e)