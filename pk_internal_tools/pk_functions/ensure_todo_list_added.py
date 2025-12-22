from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pathlib import Path

from pk_internal_tools.pk_functions.print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt import print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN


def ensure_todo_list_added():
    from datetime import datetime

    # import pk_external_tools.pk_objects.static_logic as system_object.static_logic

    now = datetime.now()
    weekday_dict = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
    weekday = weekday_dict[now.weekday()]
    yyyy = now.year
    MM = str(now.month).zfill(2)
    dd = str(now.day).zfill(2)
    HH = str(now.hour).zfill(2)
    mm = str(now.minute).zfill(2)
    # print(UNDERLINE)
    # print_schedule_template_lines(yyyy=yyyy, MM=MM, dd=dd, weekday=weekday, HH=HH, mm=mm, task_name=task_name)
    # print(UNDERLINE)
    # print_schedule_template_lines(yyyy=yyyy, MM=MM, dd="dd", weekday="weekday", HH="HH", mm="mm", task_name=task_name)
    # print(UNDERLINE)
    # print_schedule_template_lines(yyyy=yyyy, MM=MM, dd="__", weekday="_", HH="__", mm="__", task_name=task_name)
    # print(UNDERLINE)
    # print_schedule_template_lines(yyyy=yyyy, MM="__", dd="__", weekday="_", HH="__", mm="__", task_name=task_name)
    # print(UNDERLINE)
    # print_schedule_template_lines(yyyy=yyyy, MM="__", dd="__", weekday="_", HH="__", mm="__", task_name='_______')
    # print(UNDERLINE)
    # print_schedule_template_lines_as_simple(yyyy=yyyy, task_name=task_name)
    # print(UNDERLINE)
    # print_working_days_for_2025(task_name=task_name)
    # print(UNDERLINE)
    # print_holidays_for_2025(task_name=task_name)
    # print(UNDERLINE)

    memo_todo_txt = rf"{D_PK_ROOT_HIDDEN}/memo_todo.txt" # memo_todo.txt is deprecated
    memo_todo_txt = Path(memo_todo_txt)
    memo_trash_bin_txt = rf'{D_PK_ROOT_HIDDEN}/memo_trash_bin.txt'
    memo_trash_bin_txt = Path(memo_trash_bin_txt)
    memo_done_txt = rf'{D_PK_ROOT_HIDDEN}/memo_done.txt'
    memo_done_txt = Path(memo_done_txt)

    # make_pnx(pnx=memo_done_txt, mode='f')
    # make_pnx(pnx=memo_trash_bin_txt, mode='f')

    # start_date = datetime(2025, 1, 1)
    # end_date = datetime(2025, 12, 31)

    start_date = datetime(year=int(yyyy), month=int(MM), day=int(dd))
    end_date = datetime(year=int(yyyy), month=12, day=31)

    # 주기 # 매시간
    # 백업

    # 주기 # 매일
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='웃긴거보기', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='기분리프레쉬 게임', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='최대절전모드', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='발씻기', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='wake up', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='powersave mode', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='엄마 잔소리에 소리로 강하게 대응하지 않기', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="daily", stamp_custom='[매일]')

    # 주기 # 매주
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=0, stamp_custom='[매주 월요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=1, stamp_custom='[매주 화요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=2, stamp_custom='[매주 수요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=3, stamp_custom='[매주 목요일]')
    print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='치실', start_date=start_date,
                                                                end_date=end_date, f_txt=memo_todo_txt, period="weekly",
                                                                specific_weekday=3, stamp_custom='[매주 목요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=4, stamp_custom=rf'[매주 금요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=5, stamp_custom=rf'[매주 토요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="weekly", specific_weekday=6, stamp_custom=rf'[매주 일요일]')

    # 주기 # 매월
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="biweekly", specific_weekday=4, stamp_custom=rf'[매월 2주 금요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="monthly", specific_week=3, specific_weekday=5, stamp_custom=rf'[매월 3주 토요일]')
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="last_day_of_month", stamp_custom=rf'[매월 말일]')

    # 주기 # 2개월 # success
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str="헤어샾 예약 리프컷+일반펌 or 시스루댄디컷", start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="bimonthly", specific_day=11,stamp_custom="[매2개월 11일]")

    # 주기 # 매년
    # end_date = datetime(2045, 12, 31)
    # print_and_write_schedule_template_cyclic_to_f_memo_todo_txt(todo_task_name_str='_________', start_date=start_date, end_date=end_date, f_txt=memo_todo_txt, period="yearly", specific_month=1, specific_day=15, stamp_custom=rf'[매년 1월 15일]')

    # 주기 # 2년마다 #biyearly
    # mkr_2026-12-__(1-0) "2026 건강검진 [2년주기]"

    # 비주기
    # print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='________', specific_year=2025, f_txt=memo_todo_txt, specific_month=1, specific_day=13, stamp_custom=rf'[비주기]')
    # print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='모니터 악세서리확인', specific_year=2025, f_txt=memo_todo_txt, specific_month=1, specific_day=12, stamp_custom=rf'[비주기]')
    # print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='향수구매', specific_year=2025, f_txt=memo_todo_txt, specific_month=1, specific_day=14, stamp_custom=rf'[비주기]')
    # print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='점빼기', specific_year=2025, f_txt=memo_todo_txt, specific_month=12, specific_day=1, stamp_custom=rf'[비주기]')
    # print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='칫솔구매', specific_year=2025, f_txt=memo_todo_txt, specific_month=1, specific_day=13, stamp_custom=rf'[비주기]')
    # print_and_write_schedule_template_cyclic_non_to_f_memo_todo_txt(todo_task_name_str='신진영/신수영/강주형 연락 및 안부전화', specific_year=2025, f_txt=memo_todo_txt, specific_month=3, specific_day=5, stamp_custom=rf'[비주기]')

    # ensure_command_executed(cmd=rf'explorer "{memo_done_txt}" ')
    ensure_command_executed(cmd=rf'explorer "{memo_todo_txt}" ')
