if __name__ == "__main__":
    import traceback
    import logging

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.collect_temperature_periodically import collect_temperature_periodically
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # fzf로 실행 모드 선택
        mode_options = [
            "1회만 실행",
            "5분마다 주기적 실행"
        ]
        
        selected_mode = ensure_value_completed_2025_10_12_0000(
            key_name="기온 수집 모드",
            options=mode_options
        )
        
        if selected_mode == "1회만 실행":
            logging.info("기온 수집을 1회만 실행합니다.")
            collect_temperature_periodically()
        elif selected_mode == "5분마다 주기적 실행":
            logging.info("기온 수집을 5분마다 주기적으로 실행합니다. (Ctrl+C로 중지)")
            try:
                while True:
                    collect_temperature_periodically()
                    logging.debug("다음 수집까지 5분 대기 중...")
                    ensure_slept(minutes=5)
            except KeyboardInterrupt:
                logging.info("사용자에 의해 주기적 실행이 중지되었습니다.")
        else:
            logging.warning(f"알 수 없는 모드: {selected_mode}")
            
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

