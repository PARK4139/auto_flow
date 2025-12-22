from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_seconds_promised_and_alert_message_for_gui(alert_title_message, time_input=None):
    """
        TODO: Write docstring for get_seconds_promised_and_alert_message_for_gui.
    """
    import traceback
    from datetime import timedelta, datetime
    from textwrap import dedent

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_parse_seconds import get_parse_seconds

    try:

        import logging
        try:
            from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
            func_n = get_caller_name()

            if time_input is None:
                time_options = [
                    "1초", "2초", "3초", "5초", "10초",
                    "30초", "1분", "5분", "10분", "15분", "30분",
                    "1시간", "2시간", "3시간", "5시간", "10시간"
                ]
                time_input = ensure_value_completed(
                    key_name="time_input",
                    options=time_options,
                    func_n=func_n,
                )

            if not time_input or not time_input.strip():
                logging.debug("시간을 입력하지 않았습니다.")
                return None, None, None

            seconds, unit = get_parse_seconds(time_input)

            if seconds is None:
                logging.debug("올바른 시간 형식을 입력하세요. (예: 10초, 5분, 1시간)")
                return None, None, None

            # alarm_message_for_gui = ensure_value_completed(
            #     key_name="alarm_message_for_gui",
            #     options=[dedent(f"""
            #         alarm_message_for_gui: {time_input} 알람 시간경과 알람입니다!
            #         알람 설정 완료!
            #         현재 시간: {now.strftime('%H:%M:%S')}
            #         알람 시간: {alarm_time.strftime('%H:%M:%S')}
            #         대기 시간: {seconds}초
            #         알람 내용: {alarm_message_for_gui}
            #     """)],
            #     func_n=func_n,
            # )

            # 현재 시간과 알람 시간 계산
            now = datetime.now()
            alarm_time = now + timedelta(seconds=seconds)

            alarm_message_for_gui = dedent(f"""
                # {alert_title_message}
                현재 시간: {now.strftime('%H:%M:%S')}
                알람 시간: {alarm_time.strftime('%H:%M:%S')}
                대기 시간: {seconds} seconds
            """)
            return alarm_message_for_gui, seconds

        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            return None, None, None, None
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
