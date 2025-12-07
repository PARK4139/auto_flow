from pk_internal_tools.pk_functions.backup_successful_cookies import ensure_youtube_cookies_created as actual_ensure_youtube_cookies_created
from pk_internal_tools.pk_functions.backup_successful_cookies import test_cookie_validation_v2 as test_cookie_validation

def ensure_youtube_cookies_created():
    import logging

    try:
        # 쿠키 관리 실행
        success = actual_ensure_youtube_cookies_created()

        if success:
            # 쿠키 유효성 테스트
            # test_result = test_cookie_validation()
            # if test_result:
            #     logging.debug("모든 쿠키 관리 작업이 성공적으로 완료되었습니다.")
            # else:
            #     logging.debug("️ 쿠키는 생성되었지만 유효성 테스트에 실패했습니다.")
            pass
        else:
            logging.debug("쿠키 관리에 실패했습니다.")
        # return test_result
        return True

    except Exception as e:
        import traceback
        logging.debug(f"예상치 못한 오류: {e}")
        traceback.print_exc()
