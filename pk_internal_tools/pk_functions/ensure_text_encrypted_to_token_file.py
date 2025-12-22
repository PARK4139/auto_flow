def ensure_text_encrypted_to_token_file(f_token, text_plain, f_key):
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    
    from pk_internal_tools.pk_functions.encrypt_token import encrypt_token
    from pk_internal_tools.pk_functions.ensure_pnx_removed import ensure_pnx_removed
    import logging
    from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
    from pk_internal_tools.pk_functions.get_pk_key_from_f import get_pk_key_from_f
    from pathlib import Path
    from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    f_token = Path(f_token)
    if f_token.exists() and len(get_str_from_f(f=f_token).strip()) == 0:
        ensure_pnx_removed(f_token)

    if not f_token.exists():
        ensure_pnx_made(pnx=f_token, mode='f')
        import toml
        data = encrypt_token(text_plain, get_pk_key_from_f(f=f_key))
        o = {"api": data}
        with open(f_token, "w", encoding="utf-8") as f_obj:
            toml.dump(o, f_obj)
        if QC_MODE:
            logging.debug(f'''token set. {f_token} ''')
    else:
        if QC_MODE:
            logging.debug(f'''len(get_list_from_f(f_token))={len(get_list_from_f(f_token))} ''')
        logging.debug(f'''token is already set {f_token} ''')


