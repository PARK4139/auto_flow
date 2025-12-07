"""
Xavier에서 P110M 대시보드 서버를 시작하는 래퍼
"""

if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_p110m_pk_dashboard_server_started_on_xavier import ensure_pk_p110m_pk_dashboard_server_started_on_xavier

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # 기본 설정으로 서버 시작
        ensure_pk_p110m_pk_dashboard_server_started_on_xavier(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        import logging
        logging.info("서버가 사용자 요청으로 중지되었습니다.")
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

