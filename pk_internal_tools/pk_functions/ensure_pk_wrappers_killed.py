from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_wrappers_killed():
    import inspect
    import psutil
    import os
    import win32gui
    import win32con
    
    import logging
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    pk_files = get_excutable_pk_wrappers()
    
    # 통계 변수들
    total_attempted = 0
    window_killed = 0
    process_killed = 0
    not_found = 0
    
    logging.debug(f"총 {len(pk_files)}개 pk_* -> 파일 검사 시작")

    # 한번에 모든 python 프로세스 정보 수집 (성능 최적화)
    python_processes = {}
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python.exe' and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    python_processes[proc.pid] = (proc, cmdline)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        if QC_MODE:
            logging.debug(f"️ 프로세스 목록 수집 중 오류: {e}")

    for pk_file in pk_files:
        try:
            process_name = get_nx(pk_file)  # 파일명만 추출 (확장자 제외)

            total_attempted += 1
            
            # 1단계: 창 제목으로 찾아서 모든 창 종료
            window_found = False
            try:
                from pk_internal_tools.pk_functions.get_window_titles_matches import get_window_titles_matches
                window_matches = get_window_titles_matches(window_title=process_name)
                
                if window_matches:
                    # 로그 최소화: 창 개수만 표시
                    logging.debug(f"{process_name}: {len(window_matches)}개 창 종료")
                    # 모든 창을 한번에 종료
                    for hwnd, title, similarity in window_matches:
                        try:
                            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                            window_killed += 1
                        except Exception as e:
                            if QC_MODE:
                                logging.debug(f"창 종료 실패 HWND={hwnd}: {e}")
                    window_found = True
                    
            except Exception as e:
                if QC_MODE:
                    logging.debug(f"️ 창 검색 중 오류: {e}")
            
            # 2단계: 창을 찾지 못했다면 미리 수집한 프로세스 목록에서 검색
            if not window_found:
                matching_processes = []
                for pid, (proc, cmdline) in python_processes.items():
                    if process_name in cmdline:
                        matching_processes.append(proc)
                
                if matching_processes:
                    logging.debug(f"{process_name}: {len(matching_processes)}개 프로세스 직접 종료")
                    for proc in matching_processes:
                        try:
                            proc.kill()
                            process_killed += 1
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            if QC_MODE:
                                logging.debug(f"프로세스 종료 실패 PID={proc.pid}: {e}")
                else:
                    not_found += 1

        except Exception as e:
            if QC_MODE:
                logging.debug(f"{process_name} 처리 중 오류: {e}")
            not_found += 1

    # 최종 통계 출력
    logging.debug(f"종료 통계:")
    logging.debug(f"• 총 검사: {total_attempted}개")
    logging.debug(f"• 창으로 종료: {window_killed}개")
    logging.debug(f"• 프로세스 직접 종료: {process_killed}개")
    logging.debug(f"• 실행 중이지 않음: {not_found}개")
    logging.debug(f"총 {window_killed + process_killed}개 프로세스 종료 완료")

