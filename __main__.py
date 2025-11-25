try:
    import sys
    import traceback
    from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept
    from pk_system.pk_sources.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

    from source.functions.ensure_wrapper_started import ensure_wrapper_started

    if __name__ == '__main__':
        try:
            while True:
                ensure_wrapper_started()
                ensure_slept(milliseconds=50)
        except KeyboardInterrupt:
            print("업무자동화 래퍼가 사용자에 의해 중지되었습니다.")
        except Exception:
            ensure_debug_loged_verbose(traceback)
            print("오류가 발생했습니다. 로그 파일을 확인해주세요.")

except ImportError as e:
    print(f"오류: pk_system 모듈을 가져오는 데 실패했습니다. 경로 설정을 확인해주세요.")
    print(f"sys.path: {sys.path}")
    print(f"Import Error: {e}")
    traceback.print_exc()
