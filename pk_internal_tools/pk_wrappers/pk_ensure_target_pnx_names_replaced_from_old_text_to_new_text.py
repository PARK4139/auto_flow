from pathlib import Path

from sympy.codegen.ast import continue_

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000

if __name__ == "__main__":
    try:
        import traceback

        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.get_no_blank_working_str_validated import get_no_blank_text_working_validated
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
        from pk_internal_tools.pk_functions.replace_file_nxs_from_old_text_to_new_text import replace_file_nxs_from_old_text_to_new_text

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)

        func_n = get_caller_name()
        history_reset = ensure_value_completed_2025_10_13_0000(key_name=rf'history_reset', func_n=func_n, options=[False, True])
        history_reset = bool(history_reset)
        loop_cnt = 1
        while 1:
            if loop_cnt != 1 :
                history_reset = False
            d_working = ensure_value_completed_2025_10_13_0000(key_name=rf'd_working', func_n=func_n, options=[], history_reset=history_reset)
            if not Path(d_working).exists():
                continue
            target_types = ['files', 'both', 'directories', 'both']
            target_type = ensure_value_completed_2025_10_13_0000(key_name="target_type", func_n=func_n, options=target_types)
            walking_option = ensure_value_completed_2025_10_13_0000(key_name="walking_option", func_n=func_n, options=['with_walking', 'without_walking'])
            with_walking = True if walking_option == 'with_walking' else False
            old_text = ensure_value_completed_2025_10_13_0000(key_name="old_text", func_n=func_n, options=[])
            old_text = get_no_blank_text_working_validated(old_text)
            new_text = ensure_value_completed_2025_10_13_0000(key_name="new_text", func_n=func_n, options=[])
            new_text = get_no_blank_text_working_validated(new_text)
            replace_file_nxs_from_old_text_to_new_text(d_working=d_working, old_text=old_text, new_text=new_text, target_type=target_type, with_walking=with_walking)
            loop_cnt += 1
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
