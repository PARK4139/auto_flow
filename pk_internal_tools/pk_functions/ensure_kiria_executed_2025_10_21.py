from pk_internal_tools.pk_functions.get_nx import get_nx


def ensure_kiria_executed_2025_10_21():
    import logging
    import random
    import traceback
    import nest_asyncio
    import asyncio
    import speech_recognition as sr

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
    from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.cmd_f_in_cmd_exe_like_human import cmd_f_in_cmd_exe_like_human
    from pk_internal_tools.pk_functions.download_youtube_thumbnails_from_youtube_channel_main_page_url import download_youtube_thumbnails_from_youtube_channel_main_page_url
    from pk_internal_tools.pk_functions.empty_recycle_bin import empty_recycle_bin
    from pk_internal_tools.pk_functions.ensure_sound_file_executed import ensure_sound_file_executed
    from pk_internal_tools.pk_functions.ensure_pnx_backed_up import ensure_pnx_backed_up
    from pk_internal_tools.pk_functions.ensure_power_saved_as_s4 import ensure_power_saved_as_s4
    from pk_internal_tools.pk_functions.ensure_py_system_processes_restarted import ensure_py_system_processes_restarted
    from pk_internal_tools.pk_functions.ensure_screen_saved import ensure_screen_saved
    from pk_internal_tools.pk_functions.ensure_todo_list_guided import ensure_todo_list_guided
    from pk_internal_tools.pk_functions.ensure_work_directory_created import ensure_work_directory_created
    from pk_internal_tools.pk_functions.get_comprehensive_weather_information_from_web import get_comprehensive_weather_information_from_web
    from pk_internal_tools.pk_functions.get_element_random import get_element_random
    from pk_internal_tools.pk_functions.get_weekday import get_weekday
    from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21
    from pk_internal_tools.pk_functions.is_mic_device_connected_2025_10_20 import is_mic_device_connected_2025_10_20
    from pk_internal_tools.pk_functions.make_version_new import make_version_new
    from pk_internal_tools.pk_functions.move_f_via_telegram_bot_v2 import move_f_via_telegram_bot_v2
    from pk_internal_tools.pk_functions.play_my_video_track import play_my_video_track
    from pk_internal_tools.pk_functions.run_up_and_down_game import run_up_and_down_game
    from pk_internal_tools.pk_functions.speak_today_info_as_korean import speak_today_info_as_korean
    from pk_internal_tools.pk_objects.pk_directories import D_ARCHIVED
    from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
    from pk_internal_tools.pk_functions.get_today_day_info import get_today_day_info

    if not is_internet_connected_2025_10_21():
        ensure_spoken(f'''internet is not connected. ''')
        return

    if not is_mic_device_connected_2025_10_20():
        ensure_spoken(f'''mic is disconnected. ''')
        return

    recognizer = sr.Recognizer()

    loop_cnt = 0

    text_from_google = None
    while 1:
        if loop_cnt == 0:
            # ice_breaking_texts = [
            #     "hello! i am kiria, i am ready to assist",
            #     "Hello! How can I assist you today?",
            # ]
            # ice_breaking_ment = get_element_random(working_list=ice_breaking_texts)
            # ensure_spoken(ice_breaking_ment)
            pass
        if loop_cnt % 11 == 0:
            # ice_breaking_texts = [
            #     "please. give a command.",
            #     "i am boring. give a command.",
            #     "i am boring. give a something.",
            #     get_today_day_info(),
            # ]
            # ice_breaking_ment = get_element_random(working_list=ice_breaking_texts)
            # ensure_spoken(ice_breaking_ment)
            pass
        loop_cnt += 1
        try:
            if text_from_google is None:
                with sr.Microphone() as source:
                    logging.debug("주변 소음 분석 중...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    logging.debug("듣고 있습니다. 말씀해주세요...")
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        logging.debug("음성 인식 중...")
                        text_from_google = recognizer.recognize_google(audio, language="ko")
                    except sr.UnknownValueError:
                        logging.debug("음성을 이해할 수 없습니다. 다시 듣습니다.")
                        continue
                    except sr.RequestError as e:
                        logging.debug(f"Google 서비스 요청 오류; {e}. 다시 듣습니다.")
                        continue
                    except sr.WaitTimeoutError:
                        logging.debug("듣기 시간 초과. 다시 듣습니다.")
                        continue
            text_from_google = text_from_google.replace(' ', '')
            logging.debug(f'text_from_google={text_from_google}')
            if any(keyword in text_from_google for keyword in ["테스트", "test"]):
                ensure_not_prepared_yet_guided()
            elif any(keyword in text_from_google for keyword in ["휴지통비워", "휴지통정리", "empty_trash_bin"]):
                empty_recycle_bin()
                ensure_spoken("I have emptied the trash bin")
            elif any(keyword in text_from_google for keyword in ["플레인", "플래인"]):
                ensure_spoken("yes. i am here")
            elif any(keyword in text_from_google for keyword in ["영어공부"]):
                ensure_spoken("What is the weather like?")
                ensure_slept(seconds=random.randint(a=200, b=500))
                ensure_spoken(
                    "I can't directly access weather information, but if you share your location, I can guide you!")
                ensure_slept(seconds=random.randint(a=200, b=500))
                ensure_spoken("Quit")
                ensure_slept(seconds=random.randint(a=200, b=500))
                ensure_spoken("Ending the conversation. Goodbye!")
            elif any(keyword in text_from_google for keyword in ["업무_d_생성", '업무_d_']):
                # ensure_directory_created_with_timestamp(d_nx=rf"생산관리", dst=rf"{D_PK_WORKING}")
                ensure_work_directory_created()
            elif any(keyword in text_from_google for keyword in ["sound interactive mode"]):
                # ensure_todo_list_guided(days=1)  # todo : add : 등록된 스케쥴시간확인
                logging.debug("Please give a cmd")
                # print_and_speak("시키실 일 없으신가요.", after_delay=1.0) #random
                with sr.Microphone() as source:
                    # recognizer.adjust_for_ambient_noise(source)
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # audio=recognizer.listen(source, time_limit=15, phrase_time_limit=10)
                    audio = recognizer.listen(source,
                                              phrase_time_limit=10)  # phrase_time_limit: Limit the maximum length of a phrase.
                    text_from_google = recognizer.recognize_google(audio, language="ko")
            elif any(keyword in text_from_google for keyword in ["버전자동업데이트", '버저닝']):
                make_version_new(via_f_txt=True)
            elif any(keyword in text_from_google for keyword in ["프로젝트백업", "백업", "백업해라"]):

                ensure_py_system_processes_restarted([rf"{d_pk_external_tools}/pk_kill_cmd_exe.py"])
            elif any(keyword in text_from_google for keyword in ["프로젝트백업", "백업", "백업해라"]):

                ensure_py_system_processes_restarted([rf"{d_pk_external_tools}/pk_back_up_project.py"])
            elif any(keyword in text_from_google for keyword in ["텔레그램으로 백업"]):

                f = ensure_pnx_backed_up(pnx_working=d_pk_root, d_dst=D_ARCHIVED)
                nest_asyncio.apply()
                # asyncio.run(send_f_via_telegram_bot(f)) #  --> limit discovered : 단일파일 50MB 이상은 전송 불가 --> send_f_via_telegram_bot_v2(f)
                # send_f_via_telegram_bot_v2(f) # -->  fail --> timeout
                asyncio.run(move_f_via_telegram_bot_v2(f))  # -->
                # change_os_mode_to_power_saving_mode_as_s4()
                return  # return is necceary code, 처리 안시키면 PC 부팅 시 최대절전모드로 무한 진입, 컴퓨터 전원 재연결해야 된다 -> keyword = '' and use continue -> 시도하면 아마될듯
                keyword = ''
                continue
            elif any(keyword in text_from_google for keyword in ["퇴근해", "자자"]):

                ensure_py_system_processes_restarted([rf"{d_pk_external_tools}/pk_자자.py"])
                keyword = ''
                continue
            elif any(keyword in text_from_google for keyword in ["트리정리"]):

                ensure_py_system_processes_restarted([rf"{d_pk_external_tools}/pk_ensure_tree_organized.py"])
                keyword = ''
                continue
            elif any(keyword in text_from_google for keyword in ["피케이"]):
                cmd_f_in_cmd_exe_like_human(cmd_prefix='python', f=rf"{d_pk_root}/ensure_pk_wrapper_starter_executed")
            elif any(keyword in text_from_google for keyword in ["할일", "스케쥴러", "스케쥴튜토리얼"]):
                ensure_todo_list_guided()
            elif any(keyword in text_from_google for keyword in ["토렌트", "토렌트다운로드"]):
                pass
            elif any(keyword in text_from_google for keyword in ["유튜브다운로드"]):
                pass
            elif any(keyword in text_from_google for keyword in ["youtube channel download", "유튜브채널다운로드"]):
                pass
            elif any(keyword in text_from_google for keyword in
                     ["ytctd", "youtube channel thumbnail download", "유튜브채널썸네일다운로드"]):
                youtube_channel_main_page_url = input('youtube_channel_main_page_url=')
                youtube_channel_main_page_url = youtube_channel_main_page_url.strip()
                download_youtube_thumbnails_from_youtube_channel_main_page_url(youtube_channel_main_page_url)
            elif any(keyword in text_from_google for keyword in ["오늘무슨날", "무슨날"]):
                ensure_spoken('today is christmas. happy christmas')
                ensure_spoken('today is newyear')
            elif any(keyword in text_from_google for keyword in ["오늘날짜", "날짜"]):
                speak_today_info_as_korean()
            elif any(keyword in text_from_google for keyword in ["요일", "오늘요일", "몇요일"]):
                ensure_spoken(f'{get_weekday()}')
            elif any(keyword in text_from_google for keyword in ["시간", "몇시야", "몇시"]):
                HH = get_pk_time_2025_10_20_1159('%H')
                mm = get_pk_time_2025_10_20_1159('%M')
                ensure_spoken(f'{int(HH)} hour {int(mm)} minutes')
            elif any(keyword in text_from_google for keyword in ["몇분이야", "몇분", "몇분"]):
                mm = get_pk_time_2025_10_20_1159('%M')
                ensure_spoken(f'{int(mm)} minutes')
            elif any(keyword in text_from_google for keyword in ["몇초야", "몇초"]):
                server_seconds = get_pk_time_2025_10_20_1159('%S')
                ensure_spoken(f'{server_seconds} seconds')
            elif any(keyword in text_from_google for keyword in ["날씨"]):
                ensure_spoken("Searching for weather...")
                get_comprehensive_weather_information_from_web()
            elif any(keyword in text_from_google for keyword in ["음악"]):
                ensure_sound_file_executed()
                ensure_spoken("Playing music...")
            elif any(keyword in text_from_google for keyword in ["게임", "미니게임"]):
                run_up_and_down_game()
                ensure_spoken("Playing mini game...")
            elif any(keyword in text_from_google for keyword in ["exit"]):
                raise
            elif any(keyword in text_from_google for keyword in ["비디오"]):
                play_my_video_track()
                ensure_spoken("Playing video...")
            elif any(keyword in text_from_google for keyword in ["최대절전모드", "powersave", "sleep"]):
                ensure_power_saved_as_s4()
                return  # return is necceary code, 처리 안시키면 PC 부팅 시 최대절전모드로 무한 진입, 컴퓨터 전원 재연결해야 된다.
            elif any(keyword in text_from_google for keyword in ["화면보호기", "화면보호"]):
                ensure_screen_saved()
            else:
                logging.debug(rf"it was Unknown command")  # woas
                ensure_spoken("그것은 이해할수 없습니다")
                text_from_google = None
        except:
            ensure_spoken(f'''{get_nx(__file__)} 코드 exec 중 오류가 발생했습니다" ''')
            logging.error(rf"traceback.format_exc()={traceback.format_exc()}")
            input("continue:enter")
            if not is_mic_device_connected_2025_10_20():
                logging.warning(f'''mic is disconnected. ''')
        ensure_slept(milliseconds=200)
