from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForEnsureSlept


def _ensure_executed_by_following_setup(setup_ops: "SetupOpsForEnsureSlept", msg_to_print) -> None:
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    import logging
    if setup_ops & SetupOpsForEnsureSlept.NORMAL:
        logging.debug(f"[{PkTexts.TIME_LEFT}] {msg_to_print}")
    if setup_ops & SetupOpsForEnsureSlept.SILENT:
        pass

def ensure_slept(milliseconds=None, seconds=None, minutes=None, hours=None, mode_countdown=1, setup_op: "SetupOpsForEnsureSlept" = SetupOpsForEnsureSlept.NORMAL):
    import logging
    import time
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 인자 유효성 검사
    time_units = {"milliseconds": milliseconds, "seconds": seconds, "minutes": minutes, "hours": hours}
    provided_units = {k: v for k, v in time_units.items() if v is not None}
    if len(provided_units) != 1:
        logging.debug(f"{func_n}() 함수는 {list(time_units.keys())} 중 하나만 정의되어야 합니다.")
        return
    unit, value = next(iter(provided_units.items()))

    # milliseconds 인자의 정밀도를 유지
    if unit == "milliseconds":
        value = float(value)  # milliseconds는 float으로 처리하여 정밀도 유지
    else:
        value = int(value)  # 다른 단위는 정수로 처리

    # 시간을 초 단위로 변환
    time_value = None
    if unit == "milliseconds":
        time_value = value / 1000
    elif unit == "seconds":
        time_value = value
    elif unit == "minutes":
        time_value = value * 60
    elif unit == "hours":
        time_value = value * 3600
    if mode_countdown:
        remaining = int(time_value)

        # 시간, 분, 초로 변환
        def get_msg_to_print_with_time_formatted(seconds_left):
            hours = seconds_left // 3600
            minutes = (seconds_left % 3600) // 60
            seconds = seconds_left % 60

            msg_to_print = ""
            if not f"{hours:02}" == "00":
                msg_to_print += rf"{hours:02} hours "
            if not f"{minutes:02}" == "00":
                msg_to_print += rf"{minutes:02} minutes "
            if not f"{seconds:02}" == "00":
                msg_to_print += rf"{seconds:02} seconds "
            return msg_to_print

        # 카운트다운
        for i in range(remaining, 0, -1):
            msg_to_print = get_msg_to_print_with_time_formatted(i)
            _ensure_executed_by_following_setup(setup_op, msg_to_print)
            time.sleep(1)

        # 남은 시간이 소수점으로 딱 맞지 않는 경우, 잉여 시간 처리
        leftover = time_value - remaining
        if leftover > 0:
            time.sleep(leftover)
        else:
            # logging.debug("count down complete")
            pass
    else:
        logging.debug(f"Sleeping for {time_value:.3f} seconds ({value} {unit}).")  # 이 줄을 추가
        time.sleep(time_value)
