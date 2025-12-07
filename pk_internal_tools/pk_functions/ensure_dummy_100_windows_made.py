from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_dummy_100_windows_made():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed, ensure_slept
    import psutil

    # 현재 cmd.exe 프로세스 개수 확인
    initial_cmd_count = len([p for p in psutil.process_iter(['name']) if p.info['name'] == 'cmd.exe'])
    target_count = initial_cmd_count + 10

    print(f"시작: cmd.exe {initial_cmd_count}개")
    print(f"목표: cmd.exe {target_count}개")

    # 10개 창 생성 (각 창마다 100ms 여유 시간)
    for i in range(10):
        print(f"창 {i + 1}/10 생성 중...")
        ensure_command_executed(cmd="start "" cmd", mode="a")
        ensure_slept(milliseconds=100)  # 각 창마다 100ms 여유 시간!
        print(f"  창 {i + 1}/10 생성 완료, 100ms 대기 중...")

    # 이벤트 기반 프로세스 감지 (열림 + 닫힘 모두 감지)
    print("더미 창 생성 완료, 프로세스 상태 실시간 감지 중...")
    max_wait_time = 10000  # 10초
    check_interval = 100  # 100ms마다 체크
    waited_time = 0

    # 프로세스 상태 변화 추적
    last_count = initial_cmd_count
    stable_count = 0  # 안정화된 상태 카운트

    while waited_time < max_wait_time:
        current_cmd_count = len([p for p in psutil.process_iter(['name']) if p.info['name'] == 'cmd.exe'])

        # 목표 달성 확인
        if current_cmd_count >= target_count:
            print(f" 목표 달성: cmd.exe {current_cmd_count}개 (목표: {target_count}개)")
            print(f" 더미 창 생성 완료! 총 {current_cmd_count}개")
            return

        # 프로세스 상태 변화 감지
        if current_cmd_count != last_count:
            if current_cmd_count > last_count:
                print(f" 프로세스 증가: {last_count}개 → {current_cmd_count}개")
            else:
                print(f" 프로세스 감소: {last_count}개 → {current_cmd_count}개")
            last_count = current_cmd_count
            stable_count = 0  # 상태 변화 시 안정화 카운트 리셋
        else:
            stable_count += 1
            if stable_count >= 5:  # 500ms 동안 상태가 안정적이면
                print(f" 상태 안정화: {current_cmd_count}개 (안정화 시간: {stable_count * check_interval}ms)")

        print(f" 실시간 감지: {current_cmd_count}개 → {target_count}개")
        ensure_slept(milliseconds=check_interval)
        waited_time += check_interval

    # 시간 초과 시 현재 상태 반환
    final_count = len([p for p in psutil.process_iter(['name']) if p.info['name'] == 'cmd.exe'])
    print(f"️ 시간 초과: cmd.exe {final_count}개 (목표: {target_count}개)")
    print(f" 현재 상태로 진행: {final_count}개")
