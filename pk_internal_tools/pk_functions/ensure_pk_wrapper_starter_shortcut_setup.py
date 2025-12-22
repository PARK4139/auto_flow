"""
pk_system wrapper 자동 생성 및 설정 자동화 함수

이 함수는 다음 작업을 자동으로 수행합니다:
1. wrapper cmd 파일 생성/확인
2. 바로가기 생성
3. 작업표시줄 고정 안내
4. Win + 1 키 바인딩 설정

"""
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_wrapper_starter_shortcut_setup(
        create_shortcut: bool = True,
        run_powershell_script: bool = True,
        verbose: bool = True
) -> dict:
    import logging
    from pk_internal_tools.pk_objects.pk_files import F_PK_LAUNCHER_LNK
    from pk_internal_tools.pk_functions.get_p import get_p
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_windows_minimized import ensure_windows_minimized
    from pk_internal_tools.pk_functions.ensure_target_file_lnk_created import ensure_target_file_lnk_created
    result = {
        'wrapper_cmd_created': False,
        'wrapper_cmd_path': None,
        'shortcut_created': False,
        'f_shortcut_path': None,
        'powershell_script_run': False,
        'success': False
    }

    try:
        from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT, D_DESKTOP
        from pk_internal_tools.pk_objects.pk_files import F_ENSURE_pk_LNK_PINNED_PS1
        from pk_internal_tools.pk_functions.get_nx import get_nx

        wrapper_cmd_path = D_PK_ROOT / "run.cmd"
        f_shortcut_path = F_PK_LAUNCHER_LNK

        if verbose:
            logging.info("=" * 66)
            logging.info("# pk_system Wrapper 자동 설정 시작")
            logging.info("=" * 66)
            logging.info(f"# f_shortcut_path={get_p(f_shortcut_path)}")
            result['wrapper_cmd_created'] = True
            result['wrapper_cmd_path'] = str(wrapper_cmd_path)
            logging.info(f"기존 run.cmd 파일을 바로가기 대상으로 지정: {str(wrapper_cmd_path)}")

        # 바로가기 생성
        if create_shortcut:
            logging.info("# 바로가기 생성")
            try:
                # 기존 바로가기 파일이 있다면 삭제
                if f_shortcut_path.exists():
                    try:
                        f_shortcut_path.unlink()
                        logging.info(f"기존 바로가기 파일 삭제 완료: {f_shortcut_path}")
                    except Exception as e:
                        logging.warning(f"⚠️ 기존 바로가기 파일 삭제 실패: {f_shortcut_path} - {e}")
                # 타겟페스 설정
                if wrapper_cmd_path.exists():
                    # shell = win32com.client.Dispatch("WScript.Shell")
                    # shortcut = shell.CreateShortCut(str(f_shortcut_path))
                    # shortcut.Targetpath = str(wrapper_cmd_path)
                    # shortcut.WorkingDirectory = str(D_PK_ROOT)
                    # shortcut.save()
                    # result['shortcut_created'] = True
                    # result['f_shortcut_path'] = str(f_shortcut_path)
                    if verbose:
                        logging.info(f"shortcut.Targetpath={wrapper_cmd_path}")
                        logging.info(f"shortcut.WorkingDirectory={D_PK_ROOT}")
                else:
                    if verbose:
                        logging.warning(f"⚠️ wrapper_cmd_path does not exists: {wrapper_cmd_path}")

                if f_shortcut_path.exists():
                    logging.info(f"바로가기 생성 완료: {f_shortcut_path}")
                ensure_target_file_lnk_created(
                    target_file=wrapper_cmd_path,
                    shortcut_path=f_shortcut_path,
                    working_directory=D_PK_ROOT
                )
                if f_shortcut_path.exists():
                    logging.info(f"바로가2기 생성 완료: {f_shortcut_path}")
                # result['shortcut_created'] = True
                # result['f_shortcut_path'] = str(f_shortcut_path)
                if verbose:
                    logging.info(f"바로가기 생성 완료: {f_shortcut_path}")

            except Exception as e:
                logging.warning(f"⚠️ 바로가기 생성 실패: {e}")
                if verbose:
                    logging.warning(f"⚠️ 바로가기 생성 실패: {e}")

        # PowerShell 스크립트 실행 (작업표시줄 고정)
        if run_powershell_script and create_shortcut:
            if verbose:
                logging.info(f"{'_' * 66}")
                logging.info("# PowerShell 스크립트 실행 (작업표시줄 고정)")
            try:
                if F_ENSURE_pk_LNK_PINNED_PS1.exists():
                    # PowerShell 스크립트를 새 창에서 실행하고 유지
                    ps_cmd = f'start "" powershell -NoExit -ExecutionPolicy Bypass -File "{F_ENSURE_pk_LNK_PINNED_PS1}"'
                    ensure_command_executed(ps_cmd)
                    result['powershell_script_run'] = True
                    if verbose:
                        logging.info(f"PowerShell 스크립트 실행 완료: {F_ENSURE_pk_LNK_PINNED_PS1}")
                else:
                    if verbose:
                        logging.warning(f"⚠️ PowerShell 스크립트 파일을 찾을 수 없음: {F_ENSURE_pk_LNK_PINNED_PS1}")
            except Exception as e:
                logging.warning(f"⚠️ PowerShell 스크립트 실행 실패: {e}")
                if verbose:
                    logging.warning(f"⚠️ PowerShell 스크립트 실행 실패: {e}")
                    logging.warning(f"⚠️ 수동으로 실행하세요: powershell -ExecutionPolicy Bypass -File {F_ENSURE_pk_LNK_PINNED_PS1}")

        # QC_MODE 모드에서는 창을 최소화하지 않음 (디버깅 편의성)
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        if not QC_MODE:
            try:
                ensure_windows_minimized()
            except Exception as e:
                pass

        # 결과 요약
        result['success'] = (
                result['wrapper_cmd_created'] and
                (not create_shortcut or result['shortcut_created'])
        )

        if verbose:
            logging.info("" + "=" * 66)
            logging.info("# 설정 완료 요약")
            logging.info("=" * 66)
            logging.info(f"Wrapper CMD 생성: {'✅' if result['wrapper_cmd_created'] else '❌'}")
            if create_shortcut:
                logging.info(f"바로가기 생성: {'✅' if result['shortcut_created'] else '❌'}")
                logging.info(f"PowerShell 스크립트 실행: {'✅' if result['powershell_script_run'] else '❌'}")
            logging.info(f"전체 성공: {'✅' if result['success'] else '❌'}")

            if result['success']:
                logging.info("# 다음 단계:")
                logging.info("1. PowerShell 창에서 바로가기 생성이 완료되면")
                logging.info("2. 바탕화면의 'pk_launcher.lnk'를 작업표시줄에 드래그하거나")
                logging.info("3. 우클릭 → '작업 표시줄에 고정'을 선택하세요")
                logging.info("4. 작업표시줄 왼쪽에 고정하면 Win + 1 키로 빠르게 실행할 수 있습니다!")

        return result

    except Exception as e:
        logging.error(f"# pk_error\n{e}")
        if verbose:
            logging.error(f"# pk_error\n{e}")
        result['success'] = False
        return result
