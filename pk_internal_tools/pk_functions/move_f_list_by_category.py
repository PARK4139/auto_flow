def move_f_list_by_category(categorized, base_p="."):
    import os
    import shutil
    import logging
    import logging
    from pathlib import Path
    
    logging.debug(f"파일 이동 시작")
    logging.debug(f"기본 경로: {base_p}")
    logging.debug(f"카테고리 수: {len(categorized)}")
    
    total_files = sum(len(files) for category, files in categorized.items() if category != "기타")
    moved_count = 0
    error_count = 0
    
    for category, file_nxs in categorized.items():
        if category == "기타":
            logging.debug(f"카테고리 '기타' 건너뛰기")
            continue
            
        logging.debug(f"카테고리 '{category}' 처리 시작 - {len(file_nxs)}개 파일")
        
        # 카테고리 디렉토리 생성
        d_n = category.replace(" ", "_")
        category_d = os.path.join(base_p, d_n)
        
        try:
            # 디렉토리 존재 여부 확인
            if os.path.exists(category_d):
                if os.path.isdir(category_d):
                    logging.debug(f"카테고리 디렉토리가 이미 존재함: {category_d}")
                    # 기존 디렉토리 내용 확인
                    existing_files = [f for f in os.listdir(category_d) if os.path.isfile(os.path.join(category_d, f))]
                    if existing_files:
                        logging.info(f"기존 디렉토리 '{category}'에 {len(existing_files)}개 파일이 있습니다")
                        logging.debug(f"기존 파일들: {existing_files[:5]}{'...' if len(existing_files) > 5 else ''}")
                else:
                    logging.warning(f"경로이 존재하지만 디렉토리가 아님: {category_d}")
                    # 파일이 있다면 백업 후 디렉토리 생성
                    backup_path = f"{category_d}.backup"
                    if os.path.exists(backup_path):
                        counter = 1
                        while os.path.exists(backup_path):
                            backup_path = f"{category_d}.backup_{counter}"
                            counter += 1
                    try:
                        shutil.move(category_d, backup_path)
                        logging.info(f"기존 파일을 백업으로 이동: {category_d} → {backup_path}")
                        # 백업 후 디렉토리 생성
                        os.makedirs(category_d, exist_ok=True)
                        logging.debug(f"백업 후 새로운 디렉토리 생성: {category_d}")
                    except Exception as e:
                        logging.error(f"백업 생성 실패: {e}")
                        continue
            else:
                logging.debug(f"새로운 카테고리 디렉토리 생성: {category_d}")
                # 새 디렉토리만 생성
                os.makedirs(category_d, exist_ok=True)
            
            logging.debug(f"카테고리 디렉토리 준비 완료: {category_d}")
            
        except Exception as e:
            logging.error(f"카테고리 디렉토리 준비 실패: {category_d} - {e}")
            continue
        
        # 각 파일 이동
        for f_nx in file_nxs:
            src = os.path.join(base_p, f_nx)
            
            try:
                # 원본 파일 존재 확인
                if not os.path.exists(src):
                    logging.warning(f"원본 파일이 존재하지 않음: {src}")
                    error_count += 1
                    continue
                
                # 파일명 중복 해결을 위한 새로운 파일명 생성
                from pk_internal_tools.pk_functions.get_new_pnx_deduplicatd_with_suffix_number import get_new_pnx_deduplicatd_with_suffix_number_v3
                
                try:
                    result = get_new_pnx_deduplicatd_with_suffix_number_v3(f_nx, category_d)
                    final_file_name = result['file_name']
                    dst = result['target_path']
                    was_renamed = result['was_renamed']
                    attempts = result['attempts']
                    
                    if was_renamed:
                        logging.debug(f"파일명 중복 해결 완료: {f_nx} → {final_file_name} ({attempts}번 시도)")
                    else:
                        logging.debug(f"기본 파일명 사용: {f_nx}")
                        
                except ValueError as e:
                    logging.error(f"파일명 중복 해결 실패: {f_nx} - {e}")
                    error_count += 1
                    continue
                
                # 파일 이동 실행
                shutil.move(src, dst)
                moved_count += 1
                
                if was_renamed:
                    logging.info(f"파일 이동 성공 (이름 변경): {f_nx} → {final_file_name}")
                else:
                    logging.debug(f"파일 이동 성공: {f_nx} → {final_file_name}")
                
            except Exception as e:
                logging.error(f"파일 이동 실패: {f_nx} - {e}")
                error_count += 1
    
    logging.debug(f"파일 이동 완료")
    logging.debug(f"총 파일 수: {total_files}")
    logging.debug(f"성공적으로 이동된 파일: {moved_count}개")
    logging.debug(f"이동 실패한 파일: {error_count}개")
    
    return {
        'total_files': total_files,
        'moved_count': moved_count,
        'error_count': error_count
    }
