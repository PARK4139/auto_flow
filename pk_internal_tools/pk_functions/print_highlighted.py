def print_highlighted(txt_whole, highlight_config_dict):
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.get_txt_highlighted import get_txt_highlighted
    ensure_pk_colorama_initialized_once()
    print(get_txt_highlighted(txt_whole, highlight_config_dict))
