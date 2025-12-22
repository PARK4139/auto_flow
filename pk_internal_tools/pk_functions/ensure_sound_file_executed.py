from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext


def ensure_sound_file_executed():
    import logging
    from pk_internal_tools.pk_objects.pk_potplayer import PkPotplayer
    from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
    from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_objects.pk_directories import D_PK_SOUND

    if is_os_windows():
        ensure_pnx_opened_by_ext(D_PK_SOUND)
        player = PkPotplayer(d_working=D_PK_SOUND)
        player.ensure_state_machine_executed()

    elif is_os_linux():
        try:
            players = ['vlc', 'mpv', 'mplayer', 'ffplay']
            for player in players:
                try:
                    ensure_command_executed(cmd=f'{player} --help')
                    break
                except Exception as e:
                    continue
            else:
                logging.debug("️ 사용 가능한 오디오 플레이어를 찾을 수 없습니다.")
        except Exception as e:
            logging.debug(f"오디오 재생 실패: {e}")
        else:
            ensure_not_prepared_yet_guided()
