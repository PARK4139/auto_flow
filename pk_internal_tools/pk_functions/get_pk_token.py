from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_pk_token(f_token, text_plain):
    from pk_internal_tools.pk_objects.pk_urls import URL_GIT_HUB_pk_CACHE_SENSITIVE_GIT
    from pk_internal_tools.pk_functions.ensure_pnx_moved import ensure_pnx_moved
    from pk_internal_tools.pk_functions.ensure_pnx_removed import ensure_pnx_removed
    from pk_internal_tools.pk_functions.ensure_repo_cloned_via_git import ensure_repo_cloned_via_git
    from pk_internal_tools.pk_functions.get_text_decoded_from_token_file import get_text_decoded_from_token_file
    from pk_internal_tools.pk_functions.ensure_text_encrypted_to_token_file import ensure_text_encrypted_to_token_file
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden

    from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
    import logging
    from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import os

    from pk_internal_tools.pk_objects.pk_directories import d_pk_tokens
    f_master_key = d_pk_tokens / "pk_token_key.toml"

    if not is_pnx_existing(pnx=f_master_key):
        ensure_pnx_removed(D_PK_RECYCLE_BIN)
        ensure_repo_cloned_via_git(repo_url=URL_GIT_HUB_pk_CACHE_SENSITIVE_GIT, d_dst=D_PK_RECYCLE_BIN)
        f_master_key_cloned = os.path.join(D_PK_RECYCLE_BIN, "pk_token_key.toml")
        if not os.path.exists(f_master_key_cloned):
            raise FileNotFoundError(f"Cloned key file not found at: {f_master_key_cloned}")
        ensure_pnx_moved(pnx=f_master_key_cloned, d_dst=d_pk_tokens)

    ensure_text_encrypted_to_token_file(f_token=f_token, text_plain=text_plain, f_key=f_master_key)
    text_plain = get_text_decoded_from_token_file(f_token=f_token, f_key=f_master_key)

    if QC_MODE:
        logging.debug(f'''text_plain={text_plain} ''')

    return text_plain
