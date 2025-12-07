import logging

import ensure_slept
import ensure_spoken
import get_pk_time_2025_10_20_1159
from pk_internal_tools.pk_functions.get_state_from_f_pk_qc_mode_toml import get_state_from_f_pk_qc_mode_toml
from pk_internal_tools.pk_functions.guide_to_check_routines import guide_to_check_routines
from pk_internal_tools.pk_functions.is_christmas import is_christmas
from pk_internal_tools.pk_functions.is_day import is_day
from pk_internal_tools.pk_functions.is_month import is_month
from pk_internal_tools.pk_functions.is_newyear import is_newyear
from pk_internal_tools.pk_functions.set_state_from_f_pk_qc_mode_toml import set_state_from_f_pk_qc_mode_toml
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def assist_to_do_pk_schedule():
    loop_cnt = 0
    while 1:
        ment = f'pk scheduler loop {loop_cnt} is started'
        logging.debug(f"{ment}")
        if loop_cnt == 0:
            # speak_ment_experimental(ment=ment, thread_join_mode=True)
            guide_to_check_routines()

        # 특정시간에 OS 부팅
        # should_i_do(ment="백업할 타겟들을 크기에 따라 분류를 해둘까요?", function=classify_pnxs_between_smallest_pnxs_biggest_pnxs, auto_click_positive_btn_after_seconds=10)
        # should_i_do(ment="백업할 타겟들을 크기에 따라 분류를 해둘까요?", function=classify_pnxs_between_smallest_pnxs_biggest_pnxs, auto_click_negative_btn_after_seconds=5)

        # mkr_특정시간에 한번
        # if is_same_time(time1=get_pk_time_2025_10_20_1159('%Y_%m_%d_%H_%M_%S_%f'), time2=datetime(year=2024, month=10, day=31, hour=22, minute=27 , second=0)):
        #     ensure_printed_as_gui(ment="약속된 시간이 되었습니다.")

        # yyyy = get_pk_time_2025_10_20_1159('%Y')
        # MM = get_pk_time_2025_10_20_1159('%m')
        # dd = get_pk_time_2025_10_20_1159('%d')
        # HH = get_pk_time_2025_10_20_1159('%H')
        # mm = get_pk_time_2025_10_20_1159('%M')
        # ss = get_pk_time_2025_10_20_1159('%S')
        yyyy = '2024'
        daily_greeting = None
        if is_month(mm=3) and is_day(dd=22):
            daily_greeting = get_state_from_f_pk_qc_mode_toml(
                pk_state_address=f"state_pk_schedule/{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_daily_greeting")
            if daily_greeting:
                daily_greeting = 0
                set_state_from_f_pk_qc_mode_toml(
                    pk_state_address=f"state_pk_schedule/{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_daily_greeting",
                    pk_state_value=daily_greeting)
            if daily_greeting == 0:
                daily_greeting = 1
                set_state_from_f_pk_qc_mode_toml(
                    pk_state_address=f"state_pk_schedule/{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_daily_greeting",
                    pk_state_value=daily_greeting)
        if daily_greeting:
            ment = f'{yyyy} happy today! good lock for you!'
            logging.debug(f'''{ment} ''')

        # if is_midnight():  # 자정이면 초기화
        #     state_toml = toml.load(F_QC_MODE_TOML)["state_pk_schedule"]
        #     state_toml[f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_greeting'] = 0
        #     with open(F_QC_MODE_TOML, "w") as f:
        #         toml.dump(state_toml, f)

        if is_newyear():
            state_toml = toml.load(F_QC_MODE_TOML)["state_pk_schedule"]
            state_yearly_greeting = state_toml[f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_newyear_greeting']
            if not state_yearly_greeting:
                state_toml[f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_newyear_greeting'] = 0
                state_yearly_greeting = 0
            if state_yearly_greeting == 0:
                state_toml[f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_newyear_greeting'] = 1
                state_yearly_greeting = 1
            if state_yearly_greeting == 1:
                ment = f'{yyyy} happy new year! good lock for you!'
                logging.debug(f'''{ment} ''')
                ensure_spoken(text=ment)

        if is_christmas():
            state_toml = toml.load(F_QC_MODE_TOML)["state_pk_schedule"]
            state_christmas_greeting = state_toml[
                f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_christmas_greeting']
            if not state_christmas_greeting:
                state_christmas_greeting = 0
                state_toml[
                    f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_christmas_greeting'] = state_christmas_greeting
                return 0
            if state_christmas_greeting == 0:
                state_christmas_greeting = 1
                state_toml[
                    f'{yyyy}_{get_pk_time_2025_10_20_1159('%m')}_{get_pk_time_2025_10_20_1159('%d')}_christmas_greeting'] = state_yearly_greeting
                return 1
            if state_yearly_greeting == 1:
                ment = f'{yyyy} happy christmas! good lock for you!'
                logging.debug(f'''{ment} ''')
                ensure_spoken(text=ment)

        # mkr_매시간 한시간에한번
        #     랜덤미션
        #      do_random_schedules()

        # # mkr_스케쥴러_트리거 : 하루에 24번
        # ensure_pnx_backed_ups_to_deprecated_via_text_file()

        # # mkr_0시에서 24시 사이, # 분단위 스케쥴,
        # if 0 <= int(HH) <= 24 and int(ss) == 0:
        #     monitor_target_edited_and_back_up(pnx_todo=pk_ARCHIVE_TOML)  # seconds_performance_test_results : ['11.95sec', '26.78sec', '11.94sec', '3.7sec', '11.72sec']
        #     if int(HH) == 6 and int(mm) == 30:
        #         # speak_ments(f'{int(HH)} 시 {int(mm)}분 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)  # 쓰레드가 많아지니 speak() 하면서 부정확한 재생이 늘어났다. 쓰레드의 정확한 타이밍 제어가 필요한 것 같다. 급한대로 thread_join_mode 를 만들었다)
        #         # speak_ments(f'아침음악을 준비합니다, 아침음악을 재생할게요', sleep_after_play=0.65, thread_join_mode=True)
        #         pass
        #     if int(HH) == 7 and int(mm) == 30:
        #         # speak_ments(f'{int(HH)} 시 {int(mm)}분 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # speak_ments('지금 나가지 않는다면 지각할 수 있습니다, 더이상 나가는 것을 지체하기 어렵습니다', sleep_after_play=0.65, thread_join_mode=True)
        #         pass
        #
        #     if int(HH) == 8 and int(mm) == 50:
        #         # speak_ments(f'{int(HH)} 시 {int(mm)}분 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # speak_ments('업무시작 10분전입니다, 업무준비를 시작하세요, 업무 전에 세수와 양치는 하셨나요', sleep_after_play=0.65, thread_join_mode=True)
        #         pass
        #
        #     if int(HH) == 9:
        #         # speak_ments(f'{int(mm)}시 정각, 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # speak_ments('근무시간이므로 음악을 종료합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         pass
        #     if int(HH) == 11 and int(mm) == 30:
        #         # # speak_ments('용량이 큰 약속된 타겟들을 백업을 수행 시도합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # back_up_biggest_pnxs()
        #         # # speak_ments('용량이 작은 약속된 타겟들을 백업을 수행 시도합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # back_up_smallest_pnxs()
        #         # # speak_ments('흩어져있는 storage 들을 한데 모으는 시도를 합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # gather_storages()
        #         pass
        #     if int(HH) == 22 and int(mm) == 10:
        #         speak_ment_experimental('씻으실 것을 추천드립니다, 샤워튜토리얼을 수행하실 것을 추천드립니다', thread_join_mode=True)  # 샤워튜토리얼 확인창 띄우기
        #     if int(HH) == 22 and int(mm) == 30:
        #         speak_ment_experimental('건강을 위해서 지금 씻고 주무실 것을 추천드려요', thread_join_mode=True)
        #         speak_ment_experimental('건강을 위해서 24시에 최대 절전 모드에 예약이 되었습니다', thread_join_mode=True)
        #     if int(HH) == 23 and int(mm) == 55:
        #         speak_ment_experimental('5분 뒤 최대 절전 모드로 진입합니다', thread_join_mode=True)
        #     if int(HH) == 24 and int(mm) == 0:
        #         speak_ment_experimental(f'자정이 되었습니다', thread_join_mode=True)
        #         speak_ment_experimental('최대 절전 모드에 진입합니다', thread_join_mode=True)
        #         back_up_target(pnx_todo=SERVICE_D)
        #         enter_power_saving_mode()
        #     if int(HH) == 2 and int(mm) == 0:
        #         speak('새벽 두시입니다', after_delay=0.55)
        #         speak('지금부터 예약된 최대 절전 모드에 진입합니다', after_delay=1)
        #     if int(mm) % 15 == 0:
        #         # speak_ments(f'15분 간격 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # speak_ments(f'랜덤 스케줄을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         do_random_schedules()
        #         # speak_ments(f'프로젝트 d 싱크를 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #     if int(mm) % 30 == 0:
        #         # speak_ments(f'30분 간격 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # speak_ments(f'깃허브로 파이썬 아카이브 프로젝트 백업을 시도합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         # git_push_by_auto()
        #         monitor_target_edited_and_sync(pnx_todo=SERVICE_D)  # seconds_performance_test_results : ['28.46sec', '27.53sec', '2.85sec', '2.9sec', '2.91sec']
        #     if int(mm) % 60 == 0:
        #         # speak_ments(f'1시간 간격 튜토리얼을 시작합니다', sleep_after_play=0.65, thread_join_mode=True)
        #         should_i_do(ment="쓰레기통을 비울까요?", function=empty_recycle_bin, auto_click_negative_btn_after_seconds=10)
        #         should_i_do(ment="오늘 시간정보를 말씀드릴까요?", function=speak_today_time_info, auto_click_negative_btn_after_seconds=10)
        #         monitor_target_edited_and_sync(pnx_todo=SERVICE_D)  # seconds_performance_test_results : ['28.46sec', '27.53sec', '2.85sec', '2.9sec', '2.91sec']

        # mkr_ 23시에서 5시 사이, 30초 마다
        # if (23 <= int(HH) <= 24 or 0 <= int(HH) <= 5) and int(ss) % 30 == 0:
        #     guide_to_sleep() #최대절전모드 튜토리얼

        # yyyy = get_pk_time_2025_10_20_1159('%Y')
        # MM = get_pk_time_2025_10_20_1159('%m')
        # dd = get_pk_time_2025_10_20_1159('%d')
        # HH = get_pk_time_2025_10_20_1159('%H')
        # mm = get_pk_time_2025_10_20_1159('%M')
        # ss = get_pk_time_2025_10_20_1159('%S')

        # update_state_to_sql(SCHECLUER_CFG)
        # pickle 에 상태를 저장
        # checklist = [] 를 pickle 에 저장 # 상태초기화시기 : 프로그램 런타임 시
        # pk_schedule.db # 상태초기화시기 : 프로그램 런타임 시
        # config.toml /pk_schedule / # 상태초기화시기 : 프로그램 런타임 시
        # context # 상태초기화시기 : 프로그램 실행 시
        # checklist = []
        # bring checklist
        # checklist.append(line)
        # print_magenta(rf'''checklist={checklist}''')
        # print_magenta(rf'''len(checklist)={len(checklist)}''')

        # 매월 월에한번
        #     DbTomlUtil.update_db_toml(key=DbTomlUtil.get_db_toml_key(unique_id=unique_id), value=False)

        # 1년에 한번 수행 아이디어
        # random_schedule.json 에서 leaved_max_count를 읽어온다
        # leaved_max_count=10 이면 년에 1씩 깍아서 수행
        # leaved_max_count=0 이면 올해에는 더이상 수행하지 않음
        # leaved_max_count 를 random_schedule_tb.toml 에 저장

        # - 1시간 뒤 시스템 종료 예약 기능
        # - 즉시 시스템 종료 시도 기능
        # - 시간 시현기능 기능(autugui 이용)
        #   ment ='pc 정밀검사를 한번 수행해주세요'
        #   logging.debug(ment)
        # - 하드코딩된 스케줄 작업 수행 기능
        # - 미세먼지 웹스크래핑 기능
        # - 초미세먼지 웹스크래핑 기능
        # - 종합날씨 웹스크래핑 기능
        # - 습도 웹스크래핑 기능
        # - 체감온도 웹스크래핑 기능
        # - 현재온도 웹스크래핑 기능
        # - 음악재생 기능
        # - 영상재생 기능

        ensure_slept(milliseconds=200)
        ment = f'pk scheduler loop {loop_cnt} is ended'
        logging.debug(f"{ment}")
        loop_cnt = loop_cnt + 1
