def get_colorful_text_working_with_stamp_enviromnet(func_n, ment=""):
    highlight_config_dict = {
        "blue": [
            rf"pk"
        ],
        "green": [
            func_n
        ],
        "white": [
            ment
        ],
    }
    return get_txt_highlighted(txt_whole=rf'({rf"pk"}) ({func_n}) {ment}',
                               config_highlight_dict=highlight_config_dict)
