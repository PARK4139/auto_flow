from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_modules_printed():
    # TODO : 검증필요
    import inspect
    import logging
    import os  # 추가된 import
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f  # 추가된 import
    from pk_internal_tools.pk_functions.ensure_modules_saved_from_file import ensure_modules_saved_from_file
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_modules_from_file import get_modules_from_file  # 추가된 import
    from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
    from pk_internal_tools.pk_functions.is_d import is_d
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools, d_pk_root_hidden  # d_pk_root_hidden 추가

    if QC_MODE:
        decision = "d_working_mode"
        # decision = "f_working_mode"
        # decision = ensure_value_completed_2025_10_12_0000(key_hint=rf"{PkTexts.MODE}=", values=["d_working_mode", "f_working_mode"])
    else:
        decision = ensure_value_completed_2025_10_12_0000(key_name=rf"{PkTexts.MODE}", options=["d_working_mode", "f_working_mode"])
    if decision == "d_working_mode":
        all_modules = set()  # 전체 모듈을 저장할 set
        from pk_internal_tools.pk_objects.pk_directories import d_pk_config
        save_file = d_pk_config / "pk_modules_collected.txt"

        init_options = [
            Path(directory)
            for directory in get_pnxs_from_d_working(d_pk_external_tools, with_walking=True, only_dirs=True)
            if ".venv" not in directory
            if "__pycache__" not in directory
        ]

        # 모든 파일에서 모듈 수집
        for pnx in init_options:
            if is_d(pnx):
                logging.debug(f'''디렉토리 처리: {pnx} ''')
                python_files = [
                    Path(file)
                    for file in get_pnxs_from_d_working(pnx, with_walking=True, only_files=True)
                    if file.endswith('.py')
                ]

                for python_file in python_files:
                    modules = get_modules_from_file(python_file)  # 직접 호출로 변경
                    all_modules.update(modules)  # set의 update로 빠른 중복제거

        # 한 번에 모든 모듈을 정렬하고 파일에 저장
        if all_modules:
            final_modules = sorted(all_modules, reverse=True)
            ensure_list_written_to_f(final_modules, save_file, mode='w')  # w 모드로 덮어쓰기
            logging.debug(f'''총 {len(final_modules)}개 고유 모듈 저장됨 ''')
            ensure_pnx_opened_by_ext(save_file)
        else:
            logging.debug("처리할 파일이 없습니다.")
    elif decision == "f_working_mode":
        key_name = 'f_working'
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        editable = False
        # editable = True
        init_options = [
            Path(file)
            for file in get_pnxs_from_d_working(d_pk_external_tools, with_walking=True, only_files=True)
            if ".venv" not in directory  # 수정: not in으로 변경
            if "__pycache__" not in directory  # 수정: not in으로 변경
            if file.endswith(".py")
        ]

        key_name = "f_working"
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=init_options, editable=editable)
        value = selected

        f_working = value
        save_file = ensure_modules_saved_from_file(f_working=f_working, func_n=f_working)
        ensure_pnx_opened_by_ext(save_file)
