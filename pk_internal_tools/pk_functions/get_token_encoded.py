from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_token_encoded(token_id):
    from pathlib import Path
    from pk_internal_tools.pk_functions.ensure_token_file_generated import ensure_token_file_generated
    from pathlib import Path
    from pk_internal_tools.pk_functions.get_str_from_file import get_str_from_file
    from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN
    import logging

    f_token = D_PK_RECYCLE_BIN / "tokens" / rf"{token_id}.pk_token"
    f_token = Path(f_token)

    # 토큰 파일 생성 보장
    ensure_token_file_generated(f=f_token, token_id=token_id)

    # 토큰 읽기
    token = get_str_from_file(pnx=f_token)

    # 디버깅 정보 출력
    logging.debug(f"token_id={token_id}, f_token={f_token}")
    logging.debug(f"raw_token='{token}'")

    # 토큰 정리 및 검증
    if token is None:
        logging.debug(f"ERROR: token is None for token_id={token_id}")
        return None

    token = token.replace("\n", "").strip()

    if not token:
        logging.debug(f"ERROR: token is empty for token_id={token_id}")
        return None

    logging.debug(f"SUCCESS: token='{token}' for token_id={token_id}")
    return token
