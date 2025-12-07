"""
대시보드 서버를 포트 선택 옵션과 함께 실행하는 래퍼.
"""
if __name__ == "__main__":
    import traceback
    import logging

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_dashboard_server_started import ensure_pk_dashboard_server_started
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # 포트 선택
        port_options = ["8000 (기본)", "8080", "3000", "5000", "9000", "사용자 지정"]
        port_choice = ensure_value_completed_2025_10_12_0000(
            key_name="pk_dashboard_server_port",
            options=port_options,
            guide_text="서버 포트를 선택하세요:"
        )
        
        # 포트 파싱
        if port_choice == "사용자 지정":
            import sys
            try:
                custom_port = input("포트 번호를 입력하세요 (1-65535): ").strip()
                port = int(custom_port)
                if not (1 <= port <= 65535):
                    logging.warning("잘못된 포트 번호입니다. 기본 포트 8000을 사용합니다.")
                    port = 8000
            except (ValueError, KeyboardInterrupt):
                logging.warning("포트 입력이 취소되었거나 잘못되었습니다. 기본 포트 8000을 사용합니다.")
                port = 8000
        else:
            port = int(port_choice.split()[0])
        
        logging.info(f"선택된 포트: {port}")
        
        # 서버 시작
        ensure_pk_dashboard_server_started(host="0.0.0.0", port=port, reload=False)
    except KeyboardInterrupt:
        logging.info("서버가 사용자 요청으로 중지되었습니다.")
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

