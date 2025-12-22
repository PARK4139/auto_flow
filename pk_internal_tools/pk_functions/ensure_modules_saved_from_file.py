from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_modules_saved_from_file(f_working, func_n):
    from pk_internal_tools.pk_functions.get_modules_from_file import get_modules_from_file
    from pathlib import Path
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
    import logging
    from pk_internal_tools.pk_objects.pk_directories import D_PK_CONFIG
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    import os

    save_file = D_PK_CONFIG / "pk_modules_collected.txt"
    ensure_pnx_made(pnx=save_file, mode="f")

    f_working = Path(f_working)
    modules = get_modules_from_file(f_working)
    
    if modules:  # 빈 리스트 체크로 성능 향상
        logging.debug(f'''{len(modules)}개 모듈 수집: {f_working} ''')
        # 각 파일마다 append 하지 말고 리턴만 - 전체 중복제거는 ensure_modules_printed에서
        return modules, save_file
    
    return [], save_file
