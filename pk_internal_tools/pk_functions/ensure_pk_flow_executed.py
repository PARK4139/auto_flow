from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_flow_executed():
    import logging
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForEnsureSlept
    from pk_internal_tools.pk_objects.pk_flow_assistance import get_pk_flow_assistance
    try:
        pk_flow_assistance = get_pk_flow_assistance()
        pk_flow_assistance.start()
        while True:
            import time
            # ensure_slept(seconds=1)
            ensure_slept(seconds=30, setup_op=SetupOpsForEnsureSlept.SILENT)

    except KeyboardInterrupt:
        # Ctrl+C로 종료 시 스케줄러 중지
        get_pk_flow_assistance().stop()
        logging.debug("스케줄러가 사용자 요청으로 중지되었습니다.")
