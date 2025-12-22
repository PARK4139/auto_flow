# !/usr/bin/env python   # shebang
# -*- coding: utf-8 -*-  # encoding declaration
from textwrap import dedent


def _2025_12_07_design_code_done():
    # _________________________________________________
    # REQUEST: 기능대체요청
    # REQUEST DETAIL:
    # 기존 코드베이스에 ensure_local_backed_up 호출이 있었다면
    # 적절한 매개변수와 함께 ensure_pnx_backed_up를 호출하도록 변경
    # _________________________________________________
    # REQUEST: ANALIZ
    # REQUEST DETAIL:
    # ensure_pk_system_cli_executed.py 의 fzf interactive 창에서는 terminal text 드래그하여 붙여넣기가 가능.
    # ensure_values_completed.py 의 fzf interactive 창에서는 terminal text 드래그하여 붙여넣기 불가능.
    # 가능하게 하기 위한 요소 분석
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # 프로젝트 랩퍼의 logging format을 QC_MODE 에서는 단순화하자
    # ensure_pk_log_initialized 를 손보면 될거야.
    # QC_MODE 아닌경우는 지금처럼 출력 유지
    # QC_MODE에서는 [timestamp] 내용은 나오지 않도록,
    # REQUEST은 콘솔출력부분에만 적용
    # _________________________________________________
    # REQUEST: CREATE
    # ensure_pnx_backed_up, ensure_local_backed_up 의 기능비교 요청
    # ensure_pnx_backed_up 하나로 통합하고, ensure_local_backed_up 호출부도 반드시 변경필요.
    # 수동방식(user interactive)과 자동방식(only code)으로 모두 사용하기 위해서 아래의 작업을 요청.
    # back_up_mode = local_back_up | git_hub_back_up 옵션인자 필요.
    # 인자 default 는 None
    # back_up_mode 변수는 ensure_value~함수로 사용자선택
    # git_hub_back_up 는 ensure_git_repo_pushed 를 호출하도록 구현
    pass


def design_code_request_template():
    request(
        type=RequestType.FUNCTION_CREATE,
        name_to_hope=dedent(""""""),
        call_example_to_hope=dedent(""""""),
        request_detail_to_hope=dedent(""""""),
    )
    request(
        type=RequestType.DEBUG,
        name_to_hope=dedent(""""""),
        call_example_to_hope=dedent(""""""),
        request_detail_to_hope=dedent(""""""),
    )
    request(
        type=RequestType.SUGGEST,
        name_to_hope=dedent(""""""),
        call_example_to_hope=dedent(""""""),
        request_detail_to_hope=dedent("""
            pk_one_data_database.py 처럼 state 하나만을 위한 파일 DB 를 만드는 것에 대해서 어떻게 생각해?
        """),
    )
    # _________________________________________________
    # REQUEST: 프로젝트 규칙추가
    # _________________________________________________
    # REQUEST: RequestType.REFACTORING
    # _________________________________________________
    # REQUEST: docs 업데이트 요청
    # REQUEST DETAIL:
    # 수동방식(user interactive)과 자동방식(only code)으로 모두 사용하기 위해서 아래의 작업을 요청.
    # 인자로 title_to_deduplicate 받도록 수정
    # if title_to_deduplicate is None, 중복창 감지되면
    # title_to_deduplicate 변수는 ensure_value~함수로 ensure_value~함수로 사용자선택
    # 함수구현 시, 에러처리는 ensure_debugged_verbose(traceback=traceback, e=e) 호출하도록 규칙추가
    # _________________________________________________
    pass


def _2025_12_08_design_code_done():
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # PkTester 객체 기능추가
    # 더미파일 생성, 더미디렉토리 생성, 더미트리 생성, 트리 파일수/파일크기/디렉토리크기 비교기능
    # pytest 로 테스트 코드 선택 실행
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # pk_ensure_gemini_cli_initial_prompt_loaded.py
    # YOLO MODE ON 기능동작 검증
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # ensure_pnx_backed_up
    # Traceback (most recent call last):
    #   File "C:\Users\wjdgn\Downloads\pk_system\pk_internal_tools\pk_functions\ensure_tree_copied_except_blacklist_and_including_whitelist.py", line 71, in ensure_tree_copied_except_blacklist_and_including_whitelist
    #     if '*' in p.name or '?' in p.name or '*' in p.stem or '?' in p.stem:
    #               ^^^^^^
    # AttributeError: 'str' object has no attribute 'name'
    # _________________________________________________
    # REQUEST: 프로젝트 규칙추가
    # REQUEST DETAIL:
    # 함수구현 시, 에러처리는 ensure_debugged_verbose(traceback=traceback, e=e) 호출하도록 규칙추가
    pass


def _2025_12_09_design_code_done():
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # pk_kiria 구현
    # voice 기반 음성인식 비서로 할거야 pk_kiria 라는 이름으로 정의를 하고.
    # 산발되어 있는 pk_kiria 기능들을 하나로 합치려고해.
    # pk_internal_tools\pk_kiria 로 랩퍼를 제외한 모든기능을 옮겨줘.
    # 그리고 마이그레이션을 시작하자. 이미 마이그레이션 된 기능은 중복되지 않게 삭제하고
    # 실행하기위한 랩퍼가 필요하고. 기존 기능은 대부분 유지했으면해.
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETA
    # pk_web_server
    # 메모 조회생성 기능추가 from 스마트폰 to 서버
    # _________________________________________________
    # REQUEST: 기능검토
    # REQUEST DETAIL:
    # ensure_tested_all_via_pytest
    # _________________________________________________
    # REQUEST: INSPECT
    # REQUEST DETAIL:
    # ensure_tested_all_via_pytest
    # _________________________________________________
    # REQUEST: 프로젝트 규칙추가
    # REQUEST DETAIL:
    # 테스트코드 생성 시, 테스트대상 함수는 대화형(developer interactive)이 아니게 자동동작모드로 작성하여야 함. 규칙추가
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # pk_ensure_recycle_bin_empty_parmanently.py 생성요청.
    # D_RECYCLE_BIN 의 디렉토리들의 용량, 파일의 용량을 ensure_value_completed() 로 출력
    # 선택받은 것을 완전히 remove 하도록
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # pk_wrapper_starter(fzf interactive tool) 본따서 PkTester 를 만들고
    # pk_ensure_pk_tester_executed
    # tests/ 하위 코드들을 PkTester 통해서
    # multi-select 해서 테스트 되도록 하고싶어.
    # fzf interactive 기능에는 전체선택 단축키 alt+a(꼭 이거 아니여도 됨) 설정도 해줘
    # 테스트결과는 간단보기 | 상세보기 옵션을 통해서
    # 간단보기의 경우 PASS FAIL 을 함수명과 함께 표기를 하도록해줘.
    # 표기방식은 rich 라이브러리의 TABLE 을 활용해서 표기하도록해줘.
    # PASS 는 가능하면 녹색 FAIL 을 빨간색
    # 함수명, 테이블제목, 테이블선은 흰색으로 표기해줘.
    # _________________________________________________
    # pk_ensure_pk_system_version_updated.py 를 실행해도
    # "C:\Users\wjdgn\Downloads\pk_system\pk_internal_tools\pk_info\_version.py" 의
    # __version__ 은 업데이트 되지 않는지 검토요청.
    pass


def _2025_12_10_design_code_done():
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # ensure_target_files_gathered.py 실행 시 파일중복이 있으면 처리 어떻게 하는지
    # 실제로 파일이 이동되지 않음.
    pass


def _2025_12_12_design_code_done():
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # pk_ensure_target_video_files_played.py 에서는
    # fzf footer 의 들여쓰기가 잘나오는데.
    #  # 사용자 입력 튜토리얼
    #   파일선택
    #
    #   # 단축키 튜토리얼
    #   CTRL-K: remove 커서의 뒤
    #   CTRL-U: remove 커서의 앞
    #   CTRL-A: move cursor to forward of line
    #   CTRL-E: move cursor to backword of line
    #   ALT-B: move cursor to forward by word
    #   ALT-F: move cursor to backword by word
    # pk_ensure_pk_system_cli_executed.py 에서는
    #  # 사용자 입력 튜토리얼
    #               wrapper_mode
    #
    #               # 단축키 튜토리얼
    #               CTRL-K: remove 커서의 뒤
    #   CTRL-U: remove 커서의 앞
    #   CTRL-A: move cursor to forward of line
    #   CTRL-E: move cursor to backword of line
    #   ALT-B: move cursor to forward by word
    #   ALT-F: move cursor to backword by word 로 들여쓰기가 망가짐.
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # alert_as_gui(title_="title_", ment="ment", auto_click_positive_btn_after_milliseconds=5, input_text_default="input_text_default")
    pass


def _2025_12_13_design_code_done():
    # _________________________________________________
    # REQUEST: SUGGEST
    # 요청배경 : window space 입력방법 이 "한영입력"에서 "영문입력"으로
    # 요청목적 : lock(고정)하여 변경이 되지 않도록 유지하고 싶음.
    # 자꾸 변경이 되어서 불편함.
    # REQUEST DETAIL:
    # window space 입력방법 전환을 lock 하는 방법제안요청
    # 기존해결기능 .cmd or .bat 으로 작성한 스크립트 있으나 불안정.
    # 해당 파일(pk_ensure_us_keyboard_killed.py) 찾아서 분석하고
    # 더 나은 방향으로 제안요청
    # _________________________________________________
    # REQUEST: ANALIZ
    # REQUEST DETAIL:
    # ensure_targets_controlled(operation_option="스캔")
    # ensure_target_files_controlled_2025_12_13(operation_option="스캔")
    # 두 기능을 비교해줘
    # 스캔이 되면, DB 목록에서 실제경로가 존재하지 않는 경로는 제거하는 로직이 있는지 확인해줘.
    # _________________________________________________
    # REQUEST: ANALIZ
    # REQUEST DETAIL:
    # pk_ensure_target_files_controlled.py 에서 검색어 입력 또는 히스토리 선택 (다중) 라고 된부분에서는 DB 로 부터 가져온 경로에서
    # fzf interactive 사용자검색기능 으로 검색을 할수 있어야하는데, 현재 fzf 창에 아무경로도 나오지 않은 문제가 있음.
    # _________________________________________________
    # REQUEST: REFACTORING
    # REQUEST DETAIL:
    # pk_ensure_korean_ime_activated_in_loop.py 의 rich 로 구현한 print 스타일을
    # ensure_pk_interesting_infos_printed.py 의 출력스타일에 적용하고
    # rich 로 구현한 print 스타일의 session 단위로 pk_interesting_info 를 한개씩 갖도록 하고
    # session 단위로 비동기적으로 데이터를 업데이트했으면 좋겠어.
    # 비동기적으로 먼저 업데이트 된것은 먼저 출력되도록해줘.
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # ensure_alert_after_at_hh_mm()
    # 사용자 입력은 hh_mm 로 받을거야.
    # _________________________________________________
    # REQUEST: REFACTORING
    # REQUEST DETAIL:
    # ensure_pk_api_server_executed.py 와
    # ensure_pk_web_server_executed_on_remote_target_on_remote_target.py 의 중복기능을 제거하고, 함수들을 파일단위로 모듈화하고
    # ensure_pk_web_server_executed_on_remote_target.py 로 통합해줘.
    # _________________________________________________
    # REQUEST: ANALYZE
    # REQUEST DETAIL:
    # ensure_pk_api_server_executed.py ANALIZ 요청
    # _________________________________________________
    # REQUEST: REFACTORING
    # REQUEST DETAIL:
    # ensure_target_files_controlled.py 와
    # ensure_target_files_controlled_2025_12_13.py 의 중복기능을 제거하고, 함수들을 파일단위로 모듈화하고
    # ensure_target_files_controlled.py 로 통합해줘.
    pass


def _2025_12_14_design_code_done():
    # _________________________________________________
    # REQUEST: SUGGEST
    # REQUEST DETAIL:
    # pk_one_data_database.py 처럼 state 하나만을 위한 파일 DB 를 만드는 것에 대해서 어떻게 생각해?
    pass


def _2025_12_17_design_code_done():
    # _________________________________________________
    # REQUEST: INSPECT
    # REQUEST DETAIL:
    # ensure_git_repo_pushed.py 의 3가지 커밋 모드 정상여부 동작검증용 테스트 코드생성요청. 3개 테스트파일 별도로
    pass


def _2025_12_18_design_code_done():
    # _________________________________________________
    # REQUEST: pk_ensure_pk_ai_hamster_executed_via_gemini_cli CREATE
    # REQUEST DETAIL:
    # pk_ensure_pk_ai_hamster_executed_via_gemini_cli
    # gemini cli headless mode 사용을 위해 내부적으로 gemini -p 옵션 으로 호출방식 구현
    # return 은 json 형태로 받고 json 을 gemini_headless_communication_data 객체에 init
    # is_result_usable 초기화 코드구현
    # 디버깅이 용이하도록 중간에 출력을 많이 주입.
    pass


def _2025_12_19_design_code_done():
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # ensure_pk_system_environment_reset
    # pk_system을 관련 의존성 환경변수 초기화하는 기능. 시스템 환경변수 D_PK_ROOT 삭제, 랩퍼함수도 생성요청
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # "C:\Users\wjdgn\Downloads\pk_system\pk_internal_tools\pk_objects\pk_files.py" 에서
    # F_PYCHARM64_EXE 경로를 동적으로 설정하도록. 수정요청.
    # F_PYCHARM64_EXE = D_C_DRIVE / "Program Files" / "JetBrains" / "PyCharm 2025.2.1" / "bin" / "pycharm64.exe"
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # pk_ensure_target_files_scanned.py
    pass


def _2025_12_20_design_code_done():
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # ensure_pk_cicd_executed_based_on_pk_system
    # n. auto_flow 가 D_PK_ROOT에 이미 있다면 auto_flow 완전삭제
    # n. auto_flow 를 D_PK_ROOT 에 git clone 해서 .git 제외하고 empty
    # n. pk_system 내부의 모든 것을 blacklist 제외하고 copy
    # n. copy된 auto_flow root 의 특정문자열들을 모두 치환(pk_system->auto_flow
    # n. auto_flow/run.cmd 로 실행테스트
    # n. auto_flow 에서 git push
    # _________________________________________________
    request(
        type=RequestType.FUNCTION_CREATE,
        name_to_hope=dedent("""
                    pk_ensure_pk_web_server_deployed_to_remote_target.py                                        
                    pk_ensure_pk_web_server_executed_on_remote_target.py                                        
                    pk_ensure_pk_web_server_status_checked_on_remote_target.py                                  
                    pk_ensure_pk_web_server_stopped_on_remote_target.py
                """),
        call_example_to_hope=dedent("""
                    None
                """),
        request_detail_to_hope=dedent("""
                    새로운 ensure_pk_web_server_deployed_to_remote_target.py                                        
                    ensure_pk_web_server_executed_on_remote_target.py                                        
                    ensure_pk_web_server_status_checked_on_remote_target.py                                  
                    ensure_pk_web_server_stopped_on_remote_target.py
                    에 맞게 랩퍼함수들 업데이트요청     
                """),
    )
    # _________________________________________________
    request(
        type=RequestType.FUNCTION_CREATE,
        name_to_hope=dedent("""
            ensure_pk_web_server_deployed_to_remote_target.py                                        
            ensure_pk_web_server_executed_on_remote_target.py                                        
            ensure_pk_web_server_status_checked_on_remote_target.py                                  
            ensure_pk_web_server_stopped_on_remote_target.py
        """),
        call_example_to_hope=dedent("""
            None
        """),
        request_detail_to_hope=dedent("""
            ensure_pk_web_server_deployed_to_remote_target.py에서  remote_target 에 전송할 script   
            대신  %USERPROFILE%\Downloads\pk_system\pk_internal_tools\pk_web_server 를 프로젝트 변수화 하고              
            remote_target 에서 deply | execute ... 하도록 마이그래이션 요청.     
        """),
    )
    # _________________________________________________
    request(
        type=RequestType.FUNCTION_CREATE,
        name_to_hope="ensure_env_var_saved",
        call_example_to_hope=dedent("""
            ensure_env_var_saved(key_name = "PK_WEB_SERVER_URL", value = f'http://{remote_target_ip}:{port}')
        """),
        request_detail_to_hope=dedent("""
            ensure_env_var_completed 처럼 .env 파일에 저장하는데. 값이 있어도 강제로 저장.  
        """),
    )
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # compare_auto_flow_versions_between_local_and_remote_branch_of_git_hub
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # get_auto_flow_version_from_git_hub
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # get_animation_titles_from_nyaa_si()
    # base_url = https://nyaa.si/?f=0&c=0_0&q=subsPlease+1080+
    # samples in bellow
    # [SubsPlease] Dragon Raja S2 (JP) - 10 (1080p) [D60BF52F].mkv	 	1.3 GiB	2025-12-11 02:01	146	10	971
    # [SubsPlease] Let's Play - Quest-darake no My Life - 11 (1080p) [24C5C463].mkv	 	1.3 GiB	2025-12-11 01:58	288	12	1823
    # [SubsPlease] Tensei Akujo no Kuro Rekishi - 10 (1080p) [8845E4C3].mkv	 	1.4 GiB	2025-12-11 01:02	474	18	2994
    # [SubsPlease] Kakuriyo no Yadomeshi Ni - 11 (1080p) [E6161671].mkv	 	1.4 GiB	2025-12-11 00:31	335	9	2097
    # [SubsPlease] Mushoku no Eiyuu - 12 (1080p) [6CA47A29].mkv	 	915.3 MiB	2025-12-10 22:02	1004	26	8326
    # [SubsPlease] Yano-kun no Futsuu no Hibi - 11 (1080p) [09F55A05].mkv	 	1.3 GiB	2025-12-10 02:36	317	9	2909
    # [SubsPlease] Chitose-kun wa Ramune Bin no Naka - 07 (1080p) [37B7F4F3].mkv	 	1.4 GiB	2025-12-10 01:31	364	9	3558
    # [SubsPlease] Tondemo Skill de Isekai Hourou Meshi S2 - 10 (1080p) [98FF9D8C].m
    # "] " 와 " - " 사이의 내용이 title 이야 이것들을 수집하면된다.
    # DB에 수집정보 저장(축적), 중복 제거
    pass


class RequestType:
    SUGGEST = None
    DEBUG = None
    FUNCTION_CREATE = None
    REFACTORING = None


def request(type, name_to_hope, call_example_to_hope, request_detail_to_hope):
    pass


def design_code_plan_done():
    _2025_12_20_design_code_done()
    _2025_12_19_design_code_done()
    _2025_12_18_design_code_done()
    _2025_12_17_design_code_done()
    _2025_12_14_design_code_done()
    _2025_12_13_design_code_done()
    _2025_12_12_design_code_done()
    _2025_12_10_design_code_done()
    _2025_12_09_design_code_done()
    _2025_12_08_design_code_done()
    _2025_12_07_design_code_done()


def design_code_plan_todo():
    # _________________________________________________
    # REQUEST: DEBUG
    # REQUEST DETAIL:
    # pk_web_server MVP 제작
    # PC > chrome > http api request > remote_target > pk_web_server > memo_조회() from pk_database > api response > app > dashboard(그래프) > rendering
    # smart_phone > app > api request > remote_target > pk_web_server > memo_조회() from pk_database > api response > app > dashboard(그래프) > rendering
    # smart_phone > app > api request > remote_target > pk_web_server > memo_조회() from pk_database > api response > app > dashboard(그래프) > rendering
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # pk_app -> request web source to pk_web_server
    # 메모 조회생성 기능제작 from 스마트폰 to 서버
    # smart_phone / flutter / app
    # app test 자동화 appium
    # _________________________________________________
    # TODO: 휴대폰으로 알림앱, 정해진 시간에 특정텍스트를 전송.
    # 알림 = [
    #   시간 = '17:20',
    #   특정텍스트 = '
    #     if get_HH_mm() == "17:20":
    #         세안()
    #         로션바르기()
    #   ',
    # ]
    # _________________________________________________
    # nexguard feeding 예정일 #매월 # PROJECT_FAMILY_DASHBOARD
    # _________________________________________________
    # 레시피 랜덤으로 겹치지 않게 돌리도록 "전체 레시피 수", "하루 레시피 수"  #(진영이형 Needs)
    # _________________________________________________
    # vscode 익스텐션 제작 'routine in selection'   'replace blank to underbar in selection'
    # _________________________________________________
    # pk_ensure_jamo_reassembled  # 파일명 자모음 재조합
    # _________________________________________________
    request(
        type=RequestType.SUGGEST,
        name_to_hope=dedent("""
                    ensure_pk_cicd_executed_based_on_pk_system
            """),
        call_example_to_hope=dedent(""""""),
        request_detail_to_hope=dedent("""
                    커스텀 cicd 구현을 하고자해. 현재 기능분석 후 제안요청
                      Deploy pipeline 설계
            """),
    )
    # setup update for demo run.  anyone usable
    # setup update for mvp run.   membership usable
    # _________________________________________________
    # # wireless action
    # target: arduino nano esp32 with headers
    # ## target: ESP32 개발보드 + ESP-IDF OTA
    # _________________________________________________
    # # wired action
    # # ISP 기반 프로그래밍 development_environment 구축
    # AVR의 경우,  부트로더 업로드는 ISP 프로그래밍 에 의존한다.
    # # programmer: ARDUINO NANO AS ISP
    # _________________________________________________
    # execute pk_family server on remote target  추가요청
    # 각종파일을 가족들과 공유
    # 스마트TV 에서 영상보기 연동
    # web dashboard 통해서 메모텍스트파일 조회/수정
    # 파일 다운로드/업로드 다른 PC에서 파일 조회/수정
    # web dashboard 통해서 메모텍스트파일 조회/수정
    # web dashboard 통해서 하늘이 구충제 급여관리 급여완료 조회/수정
    # web dashboard 통해서 하늘이 몸무게 관리 조회/수정
    # > remote_target_ip:9911 == pk_family / video / 폭삭속았수다.mp4
    # > remote_target_ip:9911 == pk_family / video / 우주메리미.mp4
    # > remote_target_ip:9911 == pk_family / board / memo.txt
    # 9911 은 일종의 예시
    # _________________________________________________
    # execute pk_flow server on remote target 추가요청
    # 웹 대시보드 기반 일정관리
    # request remote_target to pk_asus
    # CLI 기반 일정관리
    # _________________________________________________
    # pk_ensure_pk_interested_info_printed()
    # # 언제데이터 기준인지 도 출력되는게 좋겠는데.
    # # 데이터출처의 기준시간에 따라서 "현재기온" "oo시 데이터 기준 기온" 이런식으로
    # # 기온_c = get_current_temperature_degree_celcious()
    # # if 기온_c is not None:
    # #     if 기온_c < 0:
    # #         ensure_spoken(f"영하 기온 {기온_c}도")
    # #     else:
    # #         ensure_spoken(f"영상 기온 {기온_c}도")
    # # else:
    # #     ensure_spoken("ooo 크롤링 출처로부터 기온 정보를 가져올 수 없습니다.")
    # # TODO :  _________________________________________________
    # # create 파일정리 해쉬형태로 정리하는기능
    # # test 파일정리 해쉬형태로 정리하는기능
    # # fix 파일정리 해쉬형태로 정리하는기능
    # # TODO :  _________________________________________________
    # # ensure_pk_sync_server_executed_on_remote_target ANALIZ
    # # 그리고 지금 client 쪽에서 최초 server 로 부터 동기화를 수행후 , client
    # # 파일 변경이 되면 server 로 sync 하도록 되어있는지 검토해줘.
    # # 이제 특정파일에 메모작성을 하면 실시간으로 client 간에 동기화 되며, 두 client 가 작업할 수 있겠지?
    # # port forwarding 필요해, 외부망 client 에서도 접속하고자 해.
    # # 접속조건은 까다롭게 할거야.
    # # server 와 client 간에 token 이 일치 && allowed_MAC_addressed
    # # (시도해볼 방식) 휴대폰 + 키보드 + chrome remote app
    # # (시도해볼 방식) 휴대폰 + 키보드 + 텔레그램  #마지막수단
    # "별도 코드작성 시간" 을 줄이기 위함.

    # test_testcases_of_get_pk_interesting_infos()

    # test_testcases_of_get_pk_interesting_info()

    # while not gemini_cli_flash_model_daily_limit_allowed():

    # pk_* -> pk_❤  pk_🩵  pk_🤍

    # key_name = '테스트'
    # get_pk_macro_code(key_name, func_n, history_reset=True)
    # get_pk_macro_code(key_name, func_n)

    # pk_* -> 모든 테스트 시나리오 테스트
    # ensure_test_scenarios_executed()

    # pk_* -> 삽입형 테스트 코드(환경변수)
    # from pk_tests.test_ensure_pnx_backed_up import test_scenario_ensure_pnx_backed_up
    # test_scenario_ensure_pnx_backed_up()

    # pk_* -> 삽입형 테스트 코드(환경변수)
    # PYTHONPATH = os.getenv("PYTHONPATH")
    # logging.debug(rf'PYTHONPATH = "{PYTHONPATH}"')

    # pk_* -> 삽입형 테스트 코드(트리)
    # ensure_console_cleared()
    # ensure_police_block_printed("삽입형 테스트 코드 start")
    # ensure_tree_printed(d_checkout, max_depth=2)
    # ensure_police_block_printed("삽입형 테스트 코드 end")
    # ensure_paused()

    # pk_* -> 삽입형 테스트 코드(파일존재여부)
    # ensure_console_cleared()
    # ensure_police_block_printed("삽입형 테스트 코드 start")
    # test_file = f_git_auto_push_script_to_publish
    # if test_file.exists():
    #     logging.debug(f'삽입형 테스트 성공')
    # else:
    #     logging.debug(f'삽입형 테스트 실패')
    # ensure_police_block_printed("삽입형 테스트 코드 end")
    # ensure_paused()

    # # pk_* -> 사용자 응답확인
    # question = f'깃 허브로 퍼블리싱을 진행할까요'
    # ensure_spoken(get_easy_speakable_text(question))
    # ok = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
    # if ok != PkTexts.YES:
    #     ensure_pk_wrapper_suicided(__file__)

    # f 찾기 #재귀적으로 via find command
    # sudo find -type f -name "flash.sh"
    # sudo find . -type f -name "flash.sh"

    # pk_* -> foo -> marking id (marking hash ?)
    # {'%%%FOO%%%' if LTA else ''}

    # # ensure_text_seperators_synced
    # text 를 인자로 받음.
    # 아래는 default 값들
    # seperators_to_replace = []
    # seperator_promised = ","
    # text 에 여러 개의 seperator 가 섞여 있어도 하나의 seperator 로 고정해서
    # 콘솔에 print
    # 클립보드로 복사
    # return text

    # # ensure_max_and_min_value_printed_by_text_seperator
    # ensure_text_seperators_synced 를 활용.

    # URL 공유 via QR코드()
    # VSCode Extension QR Code Generator
    # ctrl shift p
    # Generate QR Code from Clipboard
    # https://prod.liveshare.vsengsaas.visualstudio.com/join?020B982C111DB5ACB5A6BA6D3ECF84D0578E

    # # pk_life update
    # # 아침 tutorial 추가
    # 출퇴근 #헤드셋_착용() + 음악재생()
    # 청소 # 마스크 -> 헤드셋 -> 음악재생 -> 비닐장갑 -> GOOD
    # ->헤진 배변봉투 -> 일반쓰레기 분리수거
    # ->헤진 의류 -> `청소용 걸레` -> 락스희석액 제조 -> 물걸레질 -> 일반쓰레기 분리수거
    # # 저녁 tutorial 추가
    # rest 할때마다 백그라운드에서 백업
    # 자세교정 운동모음집 에 따라
    # 운동시간에 tutorial되도록 코드작성
    # 밥먹기()
    # 그루밍()
    # 정리정돈 #자주쓰는 자주쓰지않을 물건 분류 및 재배치 #아침에 나갈때 쓰레기 한 종류 버리기
    # 식사 #저녁먹기 #근무일정 #물먹기 #저녁도시락

    # # 게임처럼 BGM 재생
    #
    # 스스로가 마음에 안드시나요?
    # 사람은 고쳐쓸 수 있어요.
    # 이는 어렵지만 전략이 중요합니다.
    # 실패경험의 수보다 성공경험의 개수를 뇌 트래이닝이 필요해요.
    # 실패경험의 수를 넘어서는 방법은 작은 쉬운 성공경험의 개수를 늘리는 것이다.
    # 이는 우스운 전략이 아니에요.
    # 크고 복잡하고 어려운 일들은 작은 일들로 구성이 되어 있을 가능성이 매우 높습니다.
    # 매일 양치하세요.
    # 매일 씻으세요.
    # 매일 집안일(설겆이/빨래) 하세요.
    # 이불은 개지 않아도 좋아요. 하지만 지저분함이 보이지 않을 정도로 정리는 하세요. 쉬운 방법으로는 이불통을 추천해요.
    # 스스로에게도 예쁘게 말하세요.
    # 언어습관은 뇌를 바꿉니다.
    # 나쁜언어습관은 뇌를 부정적으로
    #
    # 세요→하는건 어떨까요
    #
    # 회는 하지 않은 것에서 부터 생각이 피어날 가능성이 매우 옾다.
    # 하지 않은 것을 후회한다.
    #
    # 제 10시 이후로 야식참기 잘수행하셨나요?, 결과는 묻지않겠습니다. 괜찮습니다.
    #
    # 침식사 시작 시간입니다. 블루베리 + 그릭요거트 + 견과류 추천드립니다.
    # 식사제한 시간 시작되었습니다. 물 외에는 섭취를 하시지 않는 것을 추천드립니다.
    #
    # 림프순환을 위한", 120ml 물한잔 추천드립니다.
    #
    # 지마세요, 자산보다 건강이 먼저입니다.
    #
    # 동루틴을 tutorial합니다.
    # "림프순환을 위한", 등운동 100회 진행
    # 진행했어
    #
    # 파이더 푸쉬업, 10회 진행
    # 진행했어
    #
    # 이슨 푸쉬업, 10회 진행
    # 진행했어
    #
    #  증량을 위한 추가 팁
    # 열량은 약 +300 kcal/일(가벼운 과잉)로 설정 → 지방 과증가 최소화
    # 거칠게: 단백질 2.0 g/kg(≈115 g), 지방 0.8 g/kg(≈45 g), 나머지 탄수화물로 채우기
    # 크레아틴 3–5 g/일(수화 잘 하기)
    # 주 3–5회 무산소 훈련 + 점진적 과부하
    #
    # # 음식 단백질 빠른 참고(대략)
    # 닭가슴살 100 g: ~31 g
    # 참치캔 100 g: ~23 g
    # 달걀 1개: ~6–7 g
    # 그릭요거트 200 g: ~20 g
    # 두부 100 g: ~8–10 g
    # 우유 250 ml: ~8 g
    # 유청단백 1스쿱: ~20–25 g
    #
    # # 식단
    # 예시 식단(약 115 g 단백질)
    # 아침: 달걀 3개(≈20 g) + 그릭요거트 200 g(≈20 g) → ~40 g
    # 점심: 닭가슴살 120 g(조리 후, ≈36 g) + 밥 + 채소 → ~36 g
    # 간식/운동 후: 유청단백 1스쿱(단백질 25 g) + 바나나 → ~25 g
    # 저녁: 두부 200 g(≈16 g) + 참치 반 캔 70 g(≈16 g) → ~32 g
    # ※ 하루 합계 ~133 g → 필요시 양 조금 줄여 115–125 g로 맞추세요.
    #
    # # 식단(운동직후)
    # 운동직후에 대한, 식단루틴을 tutorial합니다.
    # 혈당스파이크는 좋지 않다고 생각이드므로,
    # 단백질 섭취 이후 텀을 둔뒤 탄수화물 섭취를 합니다.
    # 이때 탄수화물은
    # 닭수프 + 삶은계란
    #
    # # 식단(도시락) 준비
    # 서리태 물
    # 서리태 간식
    # 물컵
    #
    # # 자산관리 루틴 tutorial
    # 박정훈 님의 자산은 오늘기준 xxxx 입니다.
    #
    # 요일 아침 산책할 시간입니다.
    # 토요일 저녁 산책할 시간입니다.
    #
    # 요일 아침 산책할 시간입니다.
    # 일요일 저녁 산책할 시간입니다.
    # _________________________________________________
    # # ensure_업무관리_서버_executed()
    # 허용한 인원들에게만 진행현황을 웹 대시보드 형태로 공유 하고싶어.
    #
    # 2025 vpc 출고일정 수립 및 공유.(웹 대시보드 형태)
    # # 개요
    #
    # 조차 의 2025_ vpc(NX) 출고물량산정
    # # 4월 7일 주(DEAD LINE주) : 1대분 / 경주_KGC090_1호 (NX #17 이관완료)
    # 5월 12일 주(DEAD LINE주) : 3대분 / 오송&조치원_EU_1/2/3호
    # 5월 19일 주(DEAD LINE주) : 2대분 / 수원_EU_1/2호
    # 7월 14일 주(DEAD LINE주) : 2대분 / 성남_EU_1/2호 (현재 일정 조정 중)
    # 7월 28일 주(DEAD LINE주) : 2대분 / 울산_GYEV_1/2호 (일렉시티타운)
    # 8월 4일 주(DEAD LINE주) : 1대분 / 경주_PV5_1호
    # 8월 11일 주(DEAD LINE주) : 총 7대분 / 해남_NE_1/2/3/4호, 해남_PV5_1/2/3호 (변경될 수 있음)
    # 9월 8일 주(DEAD LINE주) : 1대분 / 익산_A900_1호
    # 9월 22일 주(DEAD LINE주) : 2대분 / 목포_A900_1/2호
    # 처: @2025_ 3월 26일 deprecated_person팀 정화현 메일 공지
    # # 5-9월 합산
    # # 5월 5 NX
    # # 7월 4 NX
    # # 8월 8 NX
    # # 9월 3 NX
    # # 합산결론 20 NX 출고예정
    #
    # oii 의 2025_ vpc(NO) 출고물량산정
    # # 3월 10일(DEAD LINE일) : ROii 5 (NO #15 이관완료)
    # 4월 22일(DEAD LINE일) : NO 2 대 → ROII 6 , ROII 7
    # 5월 12일(DEAD LINE일) : NO 2 대 → ROII 8 , ROII 9
    # 7월 15일(DEAD LINE일) : NO 1 대 → ROII 10
    # 처: @2025_ 4월 9일 플랫폼개발1팀 deprecated_personT 메일 공지
    # # 합산결론 5 NO 출고예정
    #
    # 2025_ vpc(NX+NO) 출고상태 현황
    # # 박정훈일정 (→팀일정)
    # # 개조차 + Roii
    # 상태 정의
    # 회수 : vpc 회수완료
    # 준비 : vpc 준비완료
    # 탑재 : vpc 차량탑재완료
    # 목적        상태         위치        deadline     deadline출처   중간목적지지     최종목적지
    # 수요일 오전   deprecated_person팀 이관예정
    #
    # master board : 테스트 및 지원업무 대응용
    # nx master board : 모두 출고해야 함
    # no master board : 테스트 및 지원업무 대응용
    # _________________________________________________
    # REQUEST: 프로젝트 규칙추가
    # REQUEST DETAIL:
    # wjdgn 문자열은 security 에 위배됨.
    # 문서에 wjdgn 가 있는 경우. {user_name} 로 대체요청
    # _________________________________________________
    # REQUEST: docs 업데이트 요청.
    # REQUEST DETAIL:
    # wjdgn 문자열은 security 에 위배됨.
    # 문서에 wjdgn 가 있는 경우. {user_name} 로 대체요청
    # _________________________________________________
    # REQUEST: docs 업데이트 요청
    # REQUEST DETAIL:
    # pk_internal_tools 를 순회하며 docs가 작성되지 않은 함수들에게 docs 작성요청.
    # docs string 작성스타일은 Google style docs를 따라서 작성
    # _________________________________________________
    # REQUEST: CREATE
    # REQUEST DETAIL:
    # current working branch
    # 모든 local branch 출력
    # 모든 remote branch 출력
    # _______________________________________________ python file meta info
    # !/usr/bin/env python   # shebang
    # encoding declaration
    # _______________________________________________
    # 특정시간대 내에서 몇 기가 넘어가면 모니터링하다가 말해주도록
    # question = "휴지통을 비울까요"
    # ensure_spoken(question)
    # ok = ensure_value_completed(key_hint=rf"{question}=", values=[PkTexts.YES, PkTexts.NO])
    # if ok == PkTexts.YES:
    #     logging.info("휴지통 비우기 실행")
    #     ensure_trash_bin_emptied()
    # else:
    #     logging.info("휴지통 비우기 취소")
    # _______________________________________________
    # decision = ensure_value_completed(key_hint=rf"{PkTexts.PREVIEW_MODE}=", values=[PkTexts.PREVIEW, rf"{PkTexts.PREVIEW} X"])
    # if decision == PkTexts.PREVIEW_MODE:
    #     preview = False
    # else:
    #     preview = True
    # _______________________________________________  history sqlite
    # key_name = "pk_language"
    # pk_language = get_values_from_historical_database_routine(db_id = db.get_id(key_name,func_n), key_hint=f'{key_name}', options_default=["kr", "en"])
    # _______________________________________________  history sqlite
    # key_name = "is_pk_initial_launched"
    # is_pk_initial_launched = db.get_values(db_id = db.get_id(key_name,func_n)) or True
    # is_pk_initial_launched = db.get_values(db_id = db.get_id(key_name,func_n)) or []
    # is_pk_initial_launched = db.get_values(db_id = db.get_id(key_name,func_n)) or 11
    # is_pk_initial_launched = db.get_values(db_id = db.get_id(key_name,func_n)) or ""
    # ____________________________________________
    # pk_web_server
    # 정보별 갱신주기별로 그래프/수치 비동기 업데이트
    # 현위치날씨 정보 # 10분 마다 업데이트
    # 평촌날씨 정보 # 10분 마다 업데이트
    # 세계주식 정보 # 1초 마다 업데이트
    # ____________________________________________
    # # 현재결과
    # 날씨 정보:
    # - 날씨: N/A, 온도: N/A (출처: 네이버, 시간: 2025-09-29 17:55:36)
    # - 날씨: 맑음, 온도: 20.1°C, 풍속: 5.8km/h (출처: Open-Meteo, 시간: 2025-09-29T17:45)
    #
    #  기대결과
    # 에 URL 출처 나오면 좋겠고
    # 비/눈 이정보가 나왔으면 좋겠어
    # ____________________________________________
    # # 기대결과
    # 주식 정보 # 데이터근거 및 출처
    #   005930(삼성전자)
    #     000000(현재가)    # 2025-09-29 17:09:58 일자 {네이버 크롤링 시도 URL}
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(LV2 LD 구조 기반 크롤링 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(LV3 data-test 속성 기반 크롤링 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(LV3 사용자수동 path 기반 크롤링 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(크롤링 및 라이브러리 결과 n개 비교 신뢰성 통계값)
    #
    #
    #  QQQ
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(LV2 LD 구조 기반 크롤링 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(LV3 data-test 속성 기반 크롤링 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(LV3 사용자수동 path 기반 크롤링 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 {yfinance}(라이브러리 기반 결과)
    #     000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(크롤링 및 라이브러리 결과 n개 비교 신뢰성 통계값)
    #
    # ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    # │  > # 기대결과
    # │    주식 정보 # 데이터근거 및 출처
    # │
    # │      005930(삼성전자)
    # │        000000(현재가)    # 2025-09-29 17:09:58 일자 {네이버 크롤링 시도 URL}
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(LV2 LD 구조 기반 크롤링 결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(LV3 data-test 속성 기반 크롤링 결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(LV3 사용자수동 path 기반 크롤링 결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 {네이버 크롤링 시도 URL}(크롤링 및 라이브러리 결과 비교 신뢰성 통계값)
    # │
    # │      QQQ
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(LV2 LD 구조 기반 크롤링 결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(LV3 data-test 속성 기반 크롤링
    # │    결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(LV3 사용자수동 path 기반 크롤링
    # │     결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 {yfinance}(라이브러리 기반 결과)
    # │        000000(현재가)    # 2025-09-29 18:33:56 일자 https://www.investing.com/etfs/powershares-qqqq(크롤링 및 라이브러리 결과 비교
    # │    신뢰성 통계값)
    # ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    #
    #  네, 훨씬 더 구체화된 최종 기대 결과를 공유해주셔서 감사합니다. 이제 주니어님께서 구상하시는 전체 그림이 아주 명확하게 이해됩니다.
    #
    #   말씀해주신 대로, 모든 소스(네이버, investing.com 등)에 대해 여러 레벨의 크롤링을 시도하고, 그 결과를 통계적으로 분석하여 신뢰도를
    #   판단하는 시스템은 정말 이상적이고 강력한 솔루션입니다.
    #
    #
    #   다만, 제가 다시 한번 강조하고 싶은 점은 이 모든 시스템을 한 번에 완벽하게 구축하는 것은 매우 큰 프로젝트라는 점입니다. '사용자
    #   수동 경로'를 저장하고 관리하는 기능, '신뢰성 통계'를 계산하는 분석 엔진 등은 각각이 별도의 독립적인 기능 개발에 해당합니다.
    #
    #
    #   제가 제안드리는 방법은, 이 최종 목표를 향해 가장 중요한 순서대로, 하나씩 기능을 완성해나가는 것입니다.
    #
    #
    #  ### 점진적 구현 일정 (Phased Implementation Plan)
    #
    #
    #   Phase 1: 멀티 소스 데이터 통합 (현재 단계)
    #      목표:* 우선 yfinance, 네이버, investing.com의 결과를 모두 수집해서, 하나의 티커 아래에 그룹으로 묶어 보여주는 것부터
    #   완성합시다.
    #      작업:* 이를 위해 get_stock_infos와 __str__ 메서드를 먼저 리팩토링하겠습니다. (이것이 우리가 직전에 합의했던 일정입니다.)
    #
    #
    #       Phase 2: 스크레이퍼 고도화
    #      목표:* 1단계가 완료되면, investing.com과 네이버 스크레이퍼에 'JSON-LD(LV2)' 우선 탐색 로직을 추가하여 안정성을 높입니다.
    #
    #
    #       Phase 3: 사용자 설정 및 통계 기능 추가
    #      목표:* 마지막으로, '사용자 수동 경로' 관리 기능과 '신뢰성 통계' 분석 기능을 구현하여 전체 시스템을 완성합니다.
    #
    #
    #       이렇게 단계를 나누어 진행하면, 각 단계마다 실제 동작하는 결과물을 확인하면서 더 안정적으로 최종 목표에 도달할 수 있습니다.
    # ____________________________________________
    # # pk-asus <-(ssh)-> pk-remote_target
    # remote os 제어할때
    # JSON-RPC 2.0 통신표준으로 제어할수 있는 방법을 개발하고 싶어
    # ____________________________________________
    # # 기대결과
    # 주식 정보평가:
    #     가격평가
    #         DB에 어제자와 1년치 비교 : 기울기 X
    #         DB에 어제자와 1주일치 비교 : 기울기 X
    #         DB에 어제자와 역사 비교 (xxxx.xx.xx(상장일)~xxxx.xx.xx(오늘))  기울기 X
    # ____________________________________________
    # 루틴 가이드를 새창으로 뜨게 만들고 진행하는게 pk_life 에서
    # _______________________________________________  loop debugger
    # milliseconds = [1000, 500, 250, 100, 50]
    # ensure_loop_delayed_at_loop_foot(loop_cnt, mode_level=2, milliseconds_limit=50)
    # loop_cnt += 1
    # _______________________________________________
    # 영화속의 여러괴수들을 게임속에 출몰시켜. 살아남아.
    #
    # class Game():
    #     def run_story_scenario_script():
    #         story = Story(title="투모로우 워")
    #         Alpha()
    #         Alpha.speak("why am i, here?")
    #         Alpha.speak("alpha killed by omega")
    #
    #
    #     class Story():
    #     title
    #
    #
    # class Creature():
    #     state = "DEAD" | "LIVE"
    #     def speak():
    #
    #
    # class Omega(Creature):
    #     """
    #         Monster of 엣지오브투모로우
    #         if Omega'core is distroyed:
    #             if Omega is dead:
    #                 if Omega is dead:
    #     """
    #
    #
    # class White?(Creature):
    #     """
    #         Monster of 투모로우워
    #     """
    #
    #
    # class Alpha(Creature):
    #
    # def run_as_story_mode():
    #     game = Game()
    #     game.run_story_scenario_script()
    #
    # _________________________________________________
    # # ensure_target_files_classified_by_x
    # x 로만 분류하는게 맞는지 확인요청
    # _________________________________________________
    # # ensure_target_files_classified_by_n 개 파일 묶음
    # n개 파일 묶음으로 분류
    # 디렉토리명은 n_ea_files_(숫자)
    # 디렉토리명은 중복이 되어서는 안됨. 이미 존재하는 디렉토리명 중복시 디렉토리명에 다음 숫자 부여필요.
    # _______________________________________________
    # f_working = get_pnx_from_fzf(pnx=d_working)
    # _______________________________________________
    # f_working = ensure_value_completed(key_hint=rf"f_working=", values=get_pnxs_from_d_working(d_working=d_working))
    # _______________________________________________ pk process
    # ensure_py_system_processes_restarted([rf"{D_PK_EXTERNAL_TOOLS}/pk_ensure_os_locked.py"])
    # _______________________________________________ pk processes
    # # fix: ensure_applications_killed_like_person()
    # ensure_applications_killed_like_person 는 application 만 종료해야하는데 shutdown 까지 되어버린다.
    # 창의 개수 이상으로 동작하는 것으로 생각이듬. 검증요청
    # _________________________________________________
    # # 텔레그램 대체할수있는 가족공유 앱
    # _________________________________________________
    # # 텔레그램 대체하기
    # smartphone/memo_app/syncd_memo.txt
    # pc/syncd_memo.txt
    # pk_app  # 개인챗 > 메모들 머지 >  메모하나 선택>enter 와 동시에 편집모드 전환
    # _________________________________________________
    # kiria -> pk_slime
    # _________________________________________________
    # 게임내에서 XR 느낌 구현.
    # 브루니아 다이아몬드
    # 박빠렐라
    # _________________________________________________
    # vibe_coding_mode via cursor
    # vibe_coding_auto_mode
    #     # text = STT(speech)
    #     # save_text_to_clipboard(text)
    #     # active_cursor_AI_window()
    #     # ensure_pressed("ctrl", "l") # cursor ai chatting 활성화/비활성화 토글
    #     # ensure_pressed("ctrl", "v") # paste text from clipboard
    #     # ai_model = chatGPT
    #     # ai_model = cursor_ai_model_소넷_4 | cursor_ai_model_Opus | cursor_ai_model_auto 끝날때까지 코딩
    #     # chatGPT.window_title = ""
    #     # cursor.window_title = ""
    #     # 기획 = chatGPT.기획()
    #     # 코드 = cursor.코드작성(기획)
    #     # 테스트결과 = cursor.테스트(코드)
    #     # if 에러로그 in 테스트결과:
    #     #     cursor.프롬프트_전달(에러로그, to=cursor) # ensure_cursor_worked_done()
    # 00_requirement.md
    # 11_todo.md
    # 22_done.md
    # _________________________________________________
    # kiria 의 vibe_coding_mode
    # pk_ensure_pk_ai_hamster_executed_via_gemini_cli 기능 호출
    # _________________________________________________
    # git lecture
    # git is program for manage project tree by using managing git branch
    # git 사용법
    # git log
    # git rm --cache pk_external_tools/pk_doskey.bat
    # git restore --source={commit_id_as_hash} pk_internal_tools/pk_functions/alert_as_gui.py
    # _________________________________________________
    # MODAL 대표적인 종류
    # Alert (알림창): 중요한 정보를 알리거나 확인/취소를 선택하게 함.
    # Bottom Sheet (바텀 시트): 화면 하단에서 위로 올라오는 형태. 모바일 앱에서 옵션을 선택할 때 자주 사용함.
    # Full-screen Modal: 화면 전체를 덮는 모달. 글쓰기나 복잡한 설정 입력 시 사용함.
    # Dialog (다이얼로그): 화면 중앙에 나타나며 사용자에게 특정 입력을 요구함
    # OVERUSING MODAL IN APP DEVELOPMENT, BECOME BAD UX
    # _________________________________________________
    # git 공부해야하는 것.
    # git stash
    # git stash pop
    # _________________________________________________
    # selenium driver 재활용 수정 가능성 검토
    pass


def design_code_plan() -> None:  # PLAN = DONE + TODO
    design_code_request_template()
    design_code_plan_done()
    design_code_plan_todo()
