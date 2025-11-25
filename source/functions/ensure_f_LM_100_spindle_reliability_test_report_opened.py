import sys
import traceback
from pathlib import Path

from pk_system.pk_sources.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_sources.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_system.pk_sources.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_system.pk_sources.pk_functions.get_windows_opened import get_windows_opened
from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept
from pk_system.pk_sources.pk_functions.get_nx import get_nx


def ensure_f_LM_100_spindle_reliability_test_report_opened(file_path=None):
    """
    LM-100 스핀들 신뢰성 시험 시험기록 Excel 파일을 엽니다.
    
    Args:
        file_path: Excel 파일 경로. None이면 기본 경로에서 검색
    """
    try:
        from source.constants.directory_paths import D_PROJECT_ROOT_PATH
        
        # 파일 경로가 제공되지 않으면 기본 경로에서 검색
        if file_path is None:
            # etc/archived 디렉토리에서 최신 파일 찾기
            etc_dir = D_PROJECT_ROOT_PATH / "etc" / "archived"
            excel_files = []
            
            if etc_dir.exists():
                # .xlsx 파일 검색
                excel_files = list(etc_dir.rglob("LM-100*.xlsx"))
                # 수정 시간 기준으로 정렬 (최신순)
                excel_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            
            if excel_files:
                file_path = excel_files[0]
            else:
                print("오류: LM-100 스핀들 신뢰성 시험 시험기록 파일을 찾을 수 없습니다.")
                return False
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"오류: 파일을 찾을 수 없습니다: {file_path}")
            return False
        
        # Excel 파일 열기 (pk_system 기능 활용)
        ensure_pnx_opened_by_ext(file_path)
        ensure_slept(milliseconds=1000)  # 파일이 열릴 때까지 대기
        
        # Excel 창에 포커스
        file_name = get_nx(file_path)
        windows = get_windows_opened()
        for window in windows:
            if file_name in window or "excel" in window.lower():
                ensure_window_to_front(window)
                break
        
        return True
        
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return False



