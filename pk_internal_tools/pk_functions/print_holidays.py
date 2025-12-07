

def print_holidays(year, task_name="휴일"):
    from datetime import datetime, timedelta
    # 법정공휴일을 예외처리로 넣을 수 있도록
    # year년의 첫날과 마지막 날
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    # 요일 딕셔너리
    weekday_dict = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}

    # 현재 날짜를 시작 날짜로 설정
    current_date = start_date

    while current_date <= end_date:
        # 요일 계산
        weekday = weekday_dict[current_date.weekday()]

        # 토요일(5)과 일요일(6)만 출력
        if current_date.weekday() >= 5:  # 토요일(5) 또는 일요일(6)
            print(rf'mkr_{current_date.strftime("%Y-%m-%d")} ({weekday}) __:__ "{task_name}"')

        # 다음 날로 이동
        current_date += timedelta(days=1)
