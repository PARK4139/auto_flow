from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_autorun_registered():
    """
            pk_doskey.bat 파일을 Windows CMD AutoRun에 등록합니다.
        """
    try:

        import subprocess
        import logging

        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
        from pk_internal_tools.pk_objects.pk_files import F_PK_DOSKEY_BAT

        if not F_PK_DOSKEY_BAT.exists():
            logging.error(f"bat 파일이 존재하지 않습니다: {F_PK_DOSKEY_BAT}")
            raise FileNotFoundError(f"bat 파일이 존재하지 않습니다: {F_PK_DOSKEY_BAT}")

        # 레지스트리 AutoRun 설정
        try:
            # AutoRun 등록 (REG_EXPAND_SZ 로 환경변수 확장 허용 + call 사용)
            autorun_value = rf'call "{F_PK_DOSKEY_BAT}"'
            subprocess.run([
                "reg", "add", r"HKCU\Software\Microsoft\Command Processor",
                "/v", "AutoRun", "/t", "REG_EXPAND_SZ", "/d", autorun_value, "/f"
            ], check=True, text=True, capture_output=True)
            logging.debug(f"AutoRun 등록:{autorun_value}")

            # 확인
            subprocess.run([
                "reg", "query", r"HKCU\Software\Microsoft\Command Processor", "/v", "AutoRun"
            ], check=True)
            logging.debug(f"AutoRun 설정완료")
        except Exception as e:
            logging.error(f"레지스트리 설정 실패: {e}")
            raise

        return True
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
