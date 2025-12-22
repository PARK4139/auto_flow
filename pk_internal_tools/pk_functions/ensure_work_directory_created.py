from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_objects.pk_directories import D_TODO, D_TODO_EMERGENCY, D_DONE


def ensure_work_directory_created():
    import textwrap
    import traceback

    from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
    from pk_internal_tools.pk_functions.ensure_script_file_created import ensure_script_file_created
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    import logging

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

    try:
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        loop_cnt = 1
        while 1:
            # if loop_cnt == 1:

            # pk_* -> 진행여부
            # key_name = "진행여부"
            # selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=[PkTexts.YES, PkTexts.NO])
            # ok = selected
            # if not ok == PkTexts.YES:
            #     return

            d_todo = D_TODO
            d_todo_emergency = D_TODO_EMERGENCY
            d_done = D_DONE

            key_name = "업무종류"
            options = [get_nx(d_todo), get_nx(d_todo_emergency), get_nx(d_done), get_nx(d_todo)]
            selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
            work_type = selected

            key_name = "업무명"
            from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
            func_n = get_caller_name()
            selected = ensure_value_completed(key_name=key_name, func_n=func_n)
            work_name = selected

            # key_name = "생성경로"
            # from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
            # selected = ensure_value_completed(key_name=key_name, func_n=func_n)
            # d_destination = selected

            # 생성경로
            d_destination = None
            if work_type == get_nx(d_todo):
                d_destination = d_todo
            elif work_type == get_nx(d_todo_emergency):
                d_destination = d_todo_emergency
            elif work_type == get_nx(d_done):
                d_destination = d_done
            elif work_type == get_nx(d_todo):
                d_destination = d_todo

            # timestamp = get_pk_time_2025_10_20_1159("yyyy MM dd weekday HHmm")
            timestamp = get_pk_time_2025_10_20_1159("yyyy MM dd weekday")
            d_working_destinaion_with_time_stamp = None
            try:
                work_name = work_name.strip()

                if not d_destination.exists():
                    d_destination.mkdir()
                d_work_directory_destination = d_destination / rf"{timestamp}_{work_name}"
                logging.info(f"work_name={work_name}")
                logging.info(f"d_work_directory_destination={d_work_directory_destination}")
                if d_work_directory_destination.exists():
                    d_working_destinaion_with_time_stamp = d_work_directory_destination
                else:
                    d_work_directory_destination.mkdir()

                d_working_destinaion_with_time_stamp = d_work_directory_destination
            except Exception as e:
                ensure_debugged_verbose(traceback, e)

            if d_working_destinaion_with_time_stamp.exists():
                ensure_pnx_opened_by_ext(d_working_destinaion_with_time_stamp)

            key_name = "메모파일생성여부"
            selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=[PkTexts.YES, PkTexts.NO])
            ok = selected
            if not ok == PkTexts.YES:
                break

            f_work_memo = None
            if d_working_destinaion_with_time_stamp is not None:
                if d_working_destinaion_with_time_stamp.exists():
                    f_work_memo = d_working_destinaion_with_time_stamp / f"{work_type}.md"
                else:
                    f_work_memo = d_destination / f"{work_type}.md"
            file_contents_template = textwrap.dedent(f'''
                 # 할일
                 n. 
                 n. 
                 n. 
            ''').lstrip()
            ensure_script_file_created(script_file=f_work_memo, script_content=file_contents_template)
            if f_work_memo.exists():
                ensure_pnx_opened_by_ext(f_work_memo)

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
