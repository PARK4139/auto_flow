from functools import cache

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front


def _execute_target_file_action(target_path: str, choice, losslesscut_play_mode_option):
    """
    지정된 파일에 대해 수행할 작업을 사용자에게 묻고 실행합니다.
    """
    import logging
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_losslesscut import PkLosslesscut
    from pk_internal_tools.pk_functions.ensure_window_maximized_like_human import ensure_window_maximized_like_human
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    from pk_internal_tools.pk_objects.pk_potplayer import PkPotplayer
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    target = Path(target_path)
    if not target.exists():
        logging.error(f"대상을 찾을 수 없습니다: {target_path}")
        return

    if choice == "실행":
        logging.info(f"실행: {target}")
        ensure_pnx_opened_by_ext(target)
    elif choice == "부모열기":
        parent_dir = target.parent
        logging.info(f"부모열기: {parent_dir}")
        ensure_command_executed(f"explorer \"{parent_dir}\"")
    elif choice == "경로복사":
        import pyperclip
        pyperclip.copy(str(target))
        logging.info(f"경로가 클립보드에 복사되었습니다: {target}")
    elif choice == "Play with Losslesscut":
        from pk_internal_tools.pk_objects.pk_modes import PlayerSelectionMode
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        player = PkLosslesscut(selection_mode=losslesscut_play_mode_option)
        player.ensure_state_machine_executed(file_to_load=target)
    elif choice == "Play with Potplayer":
        # pk_option
        from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
        potplayer_path = F_POTPLAYER_EXE
        if not potplayer_path.exists():
            logging.error(f"PotPlayer 실행 파일을 찾을 수 없습니다: {potplayer_path}")
            return False
        logging.info(f"PotPlayer로 파일 열기: {target}")
        ensure_command_executed(f'"{potplayer_path}" "{target}"')
        player = PkPotplayer()
        title_character = player.idle_title
        for window_title in get_window_titles():
            if window_title.endswith(title_character):
                ensure_window_to_front(window_title)
                ensure_window_maximized_like_human()

    else:
        logging.info("작업이 취소되었습니다.")
        return False  # 루프 종료를 위해 False 반환
    return True  # 작업을 계속하기 위해 True 반환


from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@cache
def _get_losslesscut_play_mode_option(option_to_search):
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_modes import PlayerSelectionMode
    func_n = get_caller_name()
    losslesscut_play_mode_option = None
    if option_to_search == "Play with Losslesscut":
        losslesscut_play_mode_options = [member.value.lower() for member in PlayerSelectionMode]
        losslesscut_play_mode_option = ensure_value_completed(
            key_name=f"losslesscut_play_mode",  # key_name을 동적으로 생성
            func_n=func_n,
            guide_text="Losslesscut 재생 모드를 선택하세요:",
            options=losslesscut_play_mode_options,
        )
    return losslesscut_play_mode_option


@ensure_seconds_measured
def ensure_target_file_found(
        d_working: str = None,
        file_type_option: str = None,
        display_format_option: str = None,
        file_name_pattern_option: str = None
):
    """
        TODO
    """
    import logging
    import traceback
    from pathlib import Path
    import re  # Added for regex filtering
    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python
    from pk_internal_tools.pk_functions.ensure_get_all_media_file_paths_from_db import ensure_get_all_media_file_paths_from_db
    from pk_internal_tools.pk_functions.ensure_media_files_db_updated_for_path import ensure_media_files_db_updated_for_path
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_file_extensions import PK_FILE_EXTENSIONS
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_pk_file_name_pattern_options_with_stamp import get_pk_file_name_pattern_options_with_stamp

    func_n = get_caller_name()
    initial_fzf_input_source = None
    fzf_effective_cwd: Path | None = None

    if d_working is None:
        current_pwd = get_pwd_in_python()
        options_to_search = [
            f"{current_pwd}(현재 경로)",
            "DB 기반 전체 경로"
        ]
        d_working = ensure_value_completed(
            key_name="검색할 범위를 선택하세요.",
            func_n=func_n,
            options=options_to_search,
            guide_text="검색할 범위를 선택하세요(선택 또는 직접경로입력 가능)"
        )

    if not d_working:
        logging.info("경로 선택이 취소되었습니다. 작업을 종료합니다.")
        return

    # pk_pattern 선택 (멀티셀렉트)
    if file_name_pattern_option is None:
        pk_file_name_pattern_options = get_pk_file_name_pattern_options_with_stamp()
        file_name_pattern_option = ensure_values_completed(
            key_name="적용할 파일 패턴을 선택하세요 (다중 선택 가능).",
            func_n=func_n,
            options=pk_file_name_pattern_options,
            guide_text="적용할 파일 패턴을 선택하세요 (Tab으로 선택, Enter로 완료):",
            history_reset=True,
        )

    if not file_name_pattern_option:
        logging.info("파일 패턴 선택이 취소되었습니다. 작업을 종료합니다.")
        return

    # 선택된 패턴 분류
    selected_file_name_parts = []
    selected_regex_patterns = []
    for pattern_str in file_name_pattern_option:
        if pattern_str.startswith("[PART]"):
            selected_file_name_parts.append(pattern_str.replace("[PART]", "").strip())
        elif pattern_str.startswith("[REGEX]"):
            selected_regex_patterns.append(pattern_str.replace("[REGEX]", "").strip())

    if file_type_option is None:
        file_type_options = ["모든파일", "비디오만", "이미지만", "문서만"]
        file_type_option = ensure_value_completed(
            key_name="검색할 파일 타입을 선택하세요",
            func_n=func_n,
            options=file_type_options,
            guide_text="검색할 파일 타입을 선택하세요"
        )

    if not file_type_option:
        logging.info("파일 타입 선택이 취소되었습니다. 작업을 종료합니다.")
        return

    allowed_extensions = None
    if file_type_option == "비디오만":
        allowed_extensions = list(PK_FILE_EXTENSIONS['videos'])
    elif file_type_option == "이미지만":
        allowed_extensions = list(PK_FILE_EXTENSIONS['images'])
    elif file_type_option == "문서만":
        allowed_extensions = list(PK_FILE_EXTENSIONS['documents'])

    if display_format_option is None:
        display_format_options = ["파일명만", "파일경로전체"]
        display_format_option = ensure_value_completed(
            key_name="출력 형태를 선택하세요.",
            func_n=func_n,
            options=display_format_options,
            guide_text="출력 형태를 선택하세요"
        )

    if not display_format_option:
        logging.info("출력 형태 선택이 취소되었습니다. 작업을 종료합니다.")
        return

    if d_working == "DB 기반 전체 경로":
        initial_fzf_input_source = "DB"
    else:
        user_path_str = str(d_working).replace("(현재 경로)", "").strip()
        user_path = Path(user_path_str)
        try:
            user_path = user_path.resolve()
        except Exception as e:
            logging.debug(f"경로 resolve 실패 (계속 진행): {e}")

        if user_path.exists() and user_path.is_dir():
            logging.info(f"'{user_path}' 경로의 DB를 최신화합니다.")
            ensure_media_files_db_updated_for_path(user_path)
            fzf_effective_cwd = user_path
            initial_fzf_input_source = "PATH"
        else:
            logging.error(f"유효하지 않은 디렉토리입니다: {user_path_str}")
            return

    original_fzf_effective_cwd = fzf_effective_cwd
    logging.debug(f"[초기화] original_fzf_effective_cwd={original_fzf_effective_cwd}, initial_fzf_input_source={initial_fzf_input_source}, allowed_extensions={'있음' if allowed_extensions else '없음(모든파일)'}")

    loop_count = 0
    while True:
        loop_count += 1
        try:
            logging.debug(f"[시작 #{loop_count}] fzf_effective_cwd={fzf_effective_cwd}, original_fzf_effective_cwd={original_fzf_effective_cwd}, initial_fzf_input_source={initial_fzf_input_source}")

            if initial_fzf_input_source == "PATH" and original_fzf_effective_cwd:
                fzf_effective_cwd = original_fzf_effective_cwd
                logging.debug(f"[시작 #{loop_count}] fzf_effective_cwd 복원됨: {fzf_effective_cwd}")

            file_options = []
            if initial_fzf_input_source == "DB":
                logging.debug(f"[{loop_count}] DB 기반 검색 모드 (매 루프마다 갱신)")
                all_paths_from_db = ensure_get_all_media_file_paths_from_db(
                    ignore_file_name_parts=selected_file_name_parts,
                    ignore_regex_patterns=selected_regex_patterns
                )
                if not all_paths_from_db:
                    logging.info("DB에서 검색할 파일 경로를 찾을 수 없습니다. 루프를 종료합니다.")
                    break

                if allowed_extensions:
                    allowed_extensions_lower = [ext.lower() for ext in allowed_extensions]
                    file_options = [p for p in all_paths_from_db if Path(p).suffix.lower() in allowed_extensions_lower]
                    logging.debug(f"[{loop_count}] DB에서 {len(all_paths_from_db)}개 파일 중 {len(file_options)}개 필터링됨")
                else:
                    file_options = all_paths_from_db
                    logging.debug(f"[{loop_count}] DB에서 {len(file_options)}개 파일 경로 로드됨 (필터링 없음)")
                fzf_effective_cwd = None
            elif initial_fzf_input_source == "PATH" and fzf_effective_cwd:
                logging.debug(f"[{loop_count}] 디렉토리 스캔 모드: {fzf_effective_cwd}")
                d_path = fzf_effective_cwd.resolve()
                if d_path.is_dir():
                    all_files = [str(f.resolve()) for f in d_path.rglob('*') if f.is_file()]

                    # Apply allowed_extensions filter first
                    if allowed_extensions:
                        allowed_extensions_lower = [ext.lower() for ext in allowed_extensions]
                        filtered_by_extensions = [f for f in all_files if Path(f).suffix.lower() in allowed_extensions_lower]
                    else:
                        filtered_by_extensions = all_files

                    # Apply pk_pattern filters
                    filtered_by_patterns = []
                    for file_path in filtered_by_extensions:
                        ignore = False
                        # Check file_name parts
                        for part in selected_file_name_parts:
                            if part.lower() in Path(file_path).name.lower():
                                ignore = True
                                break
                        if ignore:
                            continue

                        # Check regex patterns
                        for pattern in selected_regex_patterns:
                            if re.search(pattern, file_path):
                                ignore = True
                                break
                        if ignore:
                            continue

                        filtered_by_patterns.append(file_path)

                    file_options = filtered_by_patterns
                    logging.debug(f"[{loop_count}] 직접 스캔으로 {len(all_files)}개 파일 중 {len(file_options)}개 필터링됨 (확장자 및 패턴)")

                else:
                    logging.error(f"[루프 #{loop_count}] 유효하지 않은 디렉토리입니다: {fzf_effective_cwd}")
                    break
            else:
                logging.error(f"[루프 #{loop_count}] 파일 목록을 가져올 수 없습니다.")
                break

            if not file_options:
                logging.info("선택할 파일이 없습니다.")
                break

            options_to_display = []
            file_name_to_full_path = {}
            if display_format_option == "파일명만":
                for file_path in file_options:
                    file_name = Path(file_path).name
                    options_to_display.append(file_name)
                    if file_name not in file_name_to_full_path:
                        file_name_to_full_path[file_name] = []
                    file_name_to_full_path[file_name].append(file_path)
            else:
                options_to_display = file_options

            window_title_seg = get_nx(__file__)
            if not is_window_title_front(window_title=window_title_seg):
                window_title_fallback = rf"pk_ensure_target_video_files_played.py"
                logging.debug(f'{window_title_seg} not found, try to fallback title')
                ensure_window_to_front(window_title_seg=window_title_fallback)

            files_multi_selected = ensure_values_completed(
                key_name="파일선택",
                options=options_to_display,
                func_n=func_n,
                history_reset=True
            )

            if not files_multi_selected:
                logging.info("파일 선택이 취소되었습니다. 루프를 종료합니다.")
                break

            selected_files = []
            if display_format_option == "파일명만":
                for selected_name in files_multi_selected:
                    if selected_name in file_name_to_full_path:
                        selected_files.append(file_name_to_full_path[selected_name][0])
                    else:
                        logging.warning(f"선택된 파일명에 해당하는 경로를 찾을 수 없습니다: {selected_name}")
            else:
                selected_files = files_multi_selected

            logging.info(f"[{loop_count}] 선택된 파일 {len(selected_files)}개: {selected_files}")
            logging.debug(f"[{loop_count}] 파일 처리 전 상태 - fzf_effective_cwd={fzf_effective_cwd}, original_fzf_effective_cwd={original_fzf_effective_cwd}")

            key_name = f"target action"
            actions = ["실행", "부모열기", "경로복사", "Play with Losslesscut", "Play with Potplayer", "종료"]
            func_n = get_caller_name()
            d_working = ensure_value_completed(
                key_name=key_name,
                func_n=func_n,
                options=actions,
            )
            losslesscut_play_mode_option = _get_losslesscut_play_mode_option(d_working)

            should_break_main_loop = False
            for idx, file_path in enumerate(selected_files):
                if file_path:
                    logging.debug(f"[{loop_count}] 파일 처리 중 ({idx + 1}/{len(selected_files)}): {file_path}")
                    target_file_path = Path(file_path)
                    logging.debug(f"[{loop_count}] target_file_path={target_file_path}, exists={target_file_path.exists()}, is_file={target_file_path.is_file() if target_file_path.exists() else 'N/A'}")
                    result = _execute_target_file_action(target_path=str(target_file_path), choice=d_working, losslesscut_play_mode_option=losslesscut_play_mode_option)
                    logging.debug(f"[{loop_count}] 파일 처리 결과: {result}")
                    if not result:
                        should_break_main_loop = True
                        logging.debug(f"[{loop_count}] 종료 요청됨, 루프 탈출")
                        break
            logging.debug(f"[{loop_count}] 파일 처리 후 상태 - fzf_effective_cwd={fzf_effective_cwd}, original_fzf_effective_cwd={original_fzf_effective_cwd}, should_break_main_loop={should_break_main_loop}")
            if should_break_main_loop:
                logging.info("[루프 종료] 내부 메뉴에서 '종료'가 선택되었습니다. 메인 루프를 종료합니다.")
                break
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            break
